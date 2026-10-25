import numpy as np

from . import config

H = config.HOUR
D = config.DAY
RELATIONS = ["u", "ui", "ua", "ual", "cf"]
ATOMS = ["rec_lp", "rec_skip", "org_lp", "org_skip", "ratio", "novel_lp", "novel_skip"]
ROW_KERNELS = {"r1": 1, "r3": 3, "r10": 10}
TIME_KERNELS = {"t1h": H, "t6h": 6 * H, "t1d": D, "t3d": 3 * D, "t7d": 7 * D, "t30d": 30 * D, "t90d": 90 * D}
RECENCY_KERNELS = {"x1d": D, "x30d": 30 * D}
KERNELS = list(ROW_KERNELS) + ["sess"] + list(TIME_KERNELS) + ["all"] + list(RECENCY_KERNELS)
CF_HISTORY = 64
CF_BATCH = 5000


class Alphabet:
    def __init__(self, name, atoms, kernels):
        self.name = name
        self.atoms = list(atoms)
        self.kernels = list(kernels)

    @property
    def shape(self):
        return len(RELATIONS), len(self.atoms), len(self.kernels)

    def columns(self):
        return [basis_name(r, a, k) for r in RELATIONS for a in self.atoms for k in self.kernels]


ALPHABETS = {
    "base": Alphabet("base", ATOMS[:4], list(ROW_KERNELS) + list(TIME_KERNELS) + ["all"]),
    "rich": Alphabet("rich", ATOMS, KERNELS),
}


def basis_name(relation, atom, kernel):
    return f"b_{relation}_{atom}_{kernel}"


def basis_columns():
    return ALPHABETS["rich"].columns()


def atom_values(h):
    skip = 1.0 - h.lp
    return {
        "rec_lp": h.rec * h.lp,
        "rec_skip": h.rec * skip,
        "org_lp": h.org * h.lp,
        "org_skip": h.org * skip,
        "ratio": np.clip(h.ratio, 0, 100) / 100,
        "novel_lp": h.new_artist * h.lp,
        "novel_skip": h.new_artist * skip,
    }


def relation_basis(name, relation, atoms, session_from):
    out = {}
    for kernel, k in ROW_KERNELS.items():
        for atom, values in atoms.items():
            out[basis_name(name, atom, kernel)] = relation.row_sum(values, k)
    for atom, values in atoms.items():
        out[basis_name(name, atom, "sess")] = relation.since_row(values, session_from)
    for kernel, tau in TIME_KERNELS.items():
        sums = relation.decayed_sums(atoms, tau)
        for atom, values in sums.items():
            out[basis_name(name, atom, kernel)] = values
    for atom, values in atoms.items():
        out[basis_name(name, atom, "all")] = relation.window_sum(values, "all")
    for kernel, tau in RECENCY_KERNELS.items():
        for atom, values in atoms.items():
            out[basis_name(name, atom, kernel)] = relation.last_decayed(values, tau)
    return {k: np.nan_to_num(v, nan=0.0).astype(np.float32) for k, v in out.items()}


def cf_basis(cf, h, atoms):
    o, ref = h.objects, h.ref
    n_obj = len(o)
    item_row = cf.item_rows(h.item)
    target = item_row[o]
    atom_matrix = np.stack([atoms[a] for a in ATOMS], axis=1)
    out = {basis_name("cf", a, k): np.zeros(n_obj, dtype=np.float32) for a in ATOMS for k in KERNELS}
    offsets = np.arange(1, CF_HISTORY + 1)
    for b in range(0, n_obj, CF_BATCH):
        sl = slice(b, b + CF_BATCH)
        ob, tb = o[sl], target[sl]
        hist = ob[:, None] - offsets[None, :]
        inside = hist >= h.user_start[ob - 1][:, None]
        in_session = hist >= h.session_start[ob - 1][:, None]
        hist = np.where(inside, hist, 0)
        h_row = np.where(inside, item_row[hist], -1)
        valid = (h_row >= 0) & (tb >= 0)[:, None]
        sims = np.einsum("bkd,bd->bk", cf.item_unit[np.maximum(h_row, 0)], cf.item_unit[np.maximum(tb, 0)])
        sims = np.where(valid, sims, 0.0)
        weighted = sims[:, :, None] * atom_matrix[hist] * inside[:, :, None]
        age = np.where(inside, ref[sl][:, None] - h.ts[hist], 0).astype(np.float64)
        parts = {kernel: weighted[:, :k].sum(1) for kernel, k in ROW_KERNELS.items()}
        parts["sess"] = (weighted * in_session[:, :, None]).sum(1)
        for kernel, tau in TIME_KERNELS.items():
            parts[kernel] = (weighted * np.exp(-age / tau)[:, :, None]).sum(1)
        parts["all"] = weighted.sum(1)
        for kernel, part in parts.items():
            for j, a in enumerate(ATOMS):
                out[basis_name("cf", a, kernel)][sl] = part[:, j]
    return out


def degenerate_columns():
    return {basis_name(r, a, k) for r in ["u", "cf"] for a in ATOMS for k in RECENCY_KERNELS}


def basis_features(h, rel, cf):
    atoms = atom_values(h)
    session_from = h.session_start[h.objects - 1]
    out = {}
    for name in ["u", "ui", "ua", "ual"]:
        out.update(relation_basis(name, rel[name], atoms, session_from))
    out.update(cf_basis(cf, h, atoms))
    return {c: out[c] for c in basis_columns()}
