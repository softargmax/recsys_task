import time

import numpy as np
import torch
from torch import nn

from . import config
from .basis import RELATIONS
from .train import matrix, signed_log

KERNEL_TEXT = {
    "r1": "last track", "r3": "last 3 tracks", "r10": "last 10 tracks",
    "t1h": "decay 1h", "t6h": "decay 6h", "t1d": "decay 1d", "t3d": "decay 3d",
    "t7d": "decay 7d", "t30d": "decay 30d", "t90d": "decay 90d", "all": "all history",
    "sess": "current session", "x1d": "last event, decay 1d", "x30d": "last event, decay 30d",
}
RELATION_TEXT = {"u": "any track", "ui": "same track", "ua": "same artist", "ual": "same album", "cf": "cf-similar tracks"}


def straight_through(hard, soft):
    return hard + soft - soft.detach()


def mean_entropy(p):
    return -(p * torch.log(p + 1e-9)).sum(-1).mean()


class Grammar(nn.Module):
    def __init__(self, n_count, n_rate, alphabet, init_scale=1.0):
        super().__init__()
        k = n_count + n_rate
        self.n_count = n_count
        self.alphabet = alphabet
        n_rel, n_atoms, n_kernels = alphabet.shape
        self.relation = nn.Parameter(init_scale * torch.randn(k, n_rel))
        self.kernel = nn.Parameter(init_scale * torch.randn(k, n_kernels))
        self.numerator = nn.Parameter(init_scale * torch.randn(k, n_atoms))
        self.denominator = nn.Parameter(init_scale * torch.randn(k, n_atoms))
        self.hard = False

    def weights(self):
        relation = torch.softmax(self.relation, -1)
        kernel = torch.softmax(self.kernel, -1)
        numerator = torch.sigmoid(self.numerator)
        extra = torch.sigmoid(self.denominator)
        if self.hard:
            relation = straight_through(nn.functional.one_hot(relation.argmax(-1), relation.shape[-1]).to(relation.dtype), relation)
            kernel = straight_through(nn.functional.one_hot(kernel.argmax(-1), kernel.shape[-1]).to(kernel.dtype), kernel)
            numerator = straight_through((numerator >= 0.5).to(numerator.dtype), numerator)
            extra = straight_through((extra >= 0.5).to(extra.dtype), extra)
        denominator = numerator + (1 - numerator) * extra
        return relation, kernel, numerator, denominator

    def forward(self, basis):
        relation, kernel, numerator, denominator = self.weights()
        mixed = torch.einsum("brem,kr,km->bke", basis, relation, kernel)
        top = (mixed * numerator).sum(-1)
        bottom = (mixed * denominator).sum(-1)
        counts = torch.log1p(top[:, :self.n_count].clamp(min=0))
        rates = (top[:, self.n_count:] + 0.5) / (bottom[:, self.n_count:].clamp(min=0) + 1)
        return torch.cat([counts, rates], 1)

    def entropy(self):
        relation, kernel, _, _ = self.weights()
        return mean_entropy(relation) + mean_entropy(kernel)


class GrammarModel(nn.Module):
    def __init__(self, n_count, n_rate, n_fixed, alphabet, hidden=128):
        super().__init__()
        self.grammar = Grammar(n_count, n_rate, alphabet)
        self.norm = nn.BatchNorm1d(n_count + n_rate)
        self.head = nn.Sequential(
            nn.Linear(n_count + n_rate + n_fixed, hidden), nn.ReLU(),
            nn.Linear(hidden, 64), nn.ReLU(),
            nn.Linear(64, 1),
        )

    def forward(self, basis, fixed):
        return self.head(torch.cat([self.norm(self.grammar(basis)), fixed], 1)).squeeze(1)


class Inputs:
    def __init__(self, fixed_cols, alphabet):
        self.fixed_cols = fixed_cols
        self.alphabet = alphabet

    def fit(self, df):
        raw = matrix(df, self.alphabet.columns()).reshape(-1, *self.alphabet.shape)
        self.scale = (np.abs(raw).sum(axis=2, keepdims=True).mean(axis=0) + 1e-3).astype(np.float32)
        del raw
        x = matrix(df, self.fixed_cols)
        self.median = np.nan_to_num(np.nanmedian(x, axis=0))
        x = signed_log(np.where(np.isnan(x), self.median, x))
        self.mean, self.std = x.mean(0), x.std(0) + 1e-6
        return self

    def fixed(self, df):
        x = matrix(df, self.fixed_cols)
        x = signed_log(np.where(np.isnan(x), self.median, x))
        return torch.from_numpy(((x - self.mean) / self.std).astype(np.float32))

    def basis(self, df):
        x = matrix(df, self.alphabet.columns()).reshape(-1, *self.alphabet.shape)
        x /= self.scale
        return torch.from_numpy(x)


def batches(n, size, shuffle, generator=None):
    order = torch.randperm(n, generator=generator) if shuffle else torch.arange(n)
    for start in range(0, n, size):
        yield order[start:start + size]


@torch.no_grad()
def run_model(model, basis, fixed, device, size=32768):
    model.eval()
    logits, feats = [], []
    for idx in batches(len(basis), size, shuffle=False):
        b, f = basis[idx].to(device), fixed[idx].to(device)
        feats.append(model.grammar(b).cpu())
        logits.append(model(b, f).cpu())
    return torch.sigmoid(torch.cat(logits)).numpy(), torch.cat(feats).numpy()


def logloss(y, p):
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def fit_grammar(train, val, fixed_cols, n_count, n_rate, device, alphabet, epochs=8, batch=8192, lr=3e-3, grammar_lr=5e-2,
                entropy_weight=1e-2, patience=2, seed=config.SEED, hard_from=None, hard_lr_factor=0.1):
    torch.manual_seed(seed)
    generator = torch.Generator().manual_seed(seed)
    inputs = Inputs(fixed_cols, alphabet).fit(train)
    tr_basis, tr_fixed = inputs.basis(train), inputs.fixed(train)
    tr_y = torch.from_numpy(train["label"].to_numpy().astype(np.float32))
    va_basis, va_fixed = inputs.basis(val), inputs.fixed(val)
    va_y = val["label"].to_numpy()

    model = GrammarModel(n_count, n_rate, len(fixed_cols), alphabet).to(device)
    grammar_params = list(model.grammar.parameters())
    other_params = [p for name, p in model.named_parameters() if not name.startswith("grammar.")]
    optimizer = torch.optim.AdamW([
        {"params": grammar_params, "lr": grammar_lr, "weight_decay": 0.0},
        {"params": other_params, "lr": lr, "weight_decay": 1e-5},
    ])
    loss_fn = nn.BCEWithLogitsLoss()
    best, best_state, bad, history = float("inf"), None, 0, []
    started = time.time()
    for epoch in range(epochs):
        if hard_from is not None and epoch == hard_from:
            model.grammar.hard = True
            optimizer.param_groups[0]["lr"] = grammar_lr * hard_lr_factor
            best, best_state, bad = float("inf"), None, 0
        model.train()
        for idx in batches(len(tr_y), batch, shuffle=True, generator=generator):
            b, f, y = tr_basis[idx].to(device), tr_fixed[idx].to(device), tr_y[idx].to(device)
            loss = loss_fn(model(b, f), y) + entropy_weight * model.grammar.entropy()
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        val_pred, _ = run_model(model, va_basis, va_fixed, device)
        val_loss = logloss(va_y, val_pred)
        history.append({"epoch": epoch, "val_logloss": val_loss, "seconds": round(time.time() - started, 1)})
        print(f"grammar k={n_count + n_rate} epoch {epoch}: val logloss {val_loss:.4f}, {time.time() - started:.0f}s")
        if val_loss < best - 1e-5:
            best, bad = val_loss, 0
            best_state = {k: v.detach().clone() for k, v in model.state_dict().items()}
        elif hard_from is None or epoch >= hard_from:
            bad += 1
            if bad >= patience:
                break
    assert best_state is not None, "grammar training diverged"
    model.load_state_dict(best_state)
    return model, inputs, history


def save_grammar(path, model, inputs):
    torch.save({
        "state": model.state_dict(),
        "n_count": model.grammar.n_count,
        "hard": model.grammar.hard,
        "n_rate": model.grammar.relation.shape[0] - model.grammar.n_count,
        "alphabet": inputs.alphabet.name,
        "fixed_cols": inputs.fixed_cols,
        "scale": inputs.scale,
        "median": inputs.median,
        "mean": inputs.mean,
        "std": inputs.std,
    }, path)


def transform(model, inputs, df, device):
    return run_model(model, inputs.basis(df), inputs.fixed(df), device)


def describe(model, min_weight=0.1):
    relation, kernel, numerator, denominator = (w.detach().cpu().numpy() for w in model.grammar.weights())
    atoms, kernels = model.grammar.alphabet.atoms, model.grammar.alphabet.kernels
    rows = []
    for k in range(relation.shape[0]):
        kind = "count" if k < model.grammar.n_count else "rate"
        rel = sorted(((RELATIONS[i], float(w)) for i, w in enumerate(relation[k]) if w >= min_weight), key=lambda x: -x[1])
        ker = sorted(((kernels[i], float(w)) for i, w in enumerate(kernel[k]) if w >= min_weight), key=lambda x: -x[1])
        num = [atoms[i] for i, w in enumerate(numerator[k]) if w >= 0.5]
        den = [atoms[i] for i, w in enumerate(denominator[k]) if w >= 0.5]
        what = " + ".join(num) or "nothing"
        if kind == "rate":
            what = f"({what}) / ({' + '.join(den) or 'nothing'})"
        text = (
            f"{kind}: {what} over "
            + " + ".join(f"{w:.2f} {RELATION_TEXT[r]}" for r, w in rel)
            + ", kernel "
            + " + ".join(f"{w:.2f} {KERNEL_TEXT[m]}" for m, w in ker)
        )
        rows.append({
            "feature": k, "kind": kind, "text": text,
            "relation": dict(zip(RELATIONS, relation[k].round(4).tolist())),
            "kernel": dict(zip(kernels, kernel[k].round(4).tolist())),
            "numerator": dict(zip(atoms, numerator[k].round(4).tolist())),
            "denominator": dict(zip(atoms, denominator[k].round(4).tolist())),
        })
    return rows
