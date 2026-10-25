from itertools import combinations

from .basis import ALPHABETS, ATOMS, KERNELS, RECENCY_KERNELS, Alphabet

CHANNELS = {
    "ratio": (["ratio"], []),
    "novel": (["novel_lp", "novel_skip"], []),
    "sess": ([], ["sess"]),
    "recency": ([], list(RECENCY_KERNELS)),
}


def alphabet_with(channels, name):
    drop_atoms = {a for c in CHANNELS if c not in channels for a in CHANNELS[c][0]}
    drop_kernels = {k for c in CHANNELS if c not in channels for k in CHANNELS[c][1]}
    return Alphabet(name, [a for a in ATOMS if a not in drop_atoms], [k for k in KERNELS if k not in drop_kernels])


def ablation_alphabets():
    out = {"rich": alphabet_with(tuple(CHANNELS), "rich"), "base": alphabet_with((), "base")}
    for c in CHANNELS:
        out[f"rich-{c}"] = alphabet_with(tuple(x for x in CHANNELS if x != c), f"rich-{c}")
        out[f"base+{c}"] = alphabet_with((c,), f"base+{c}")
    for name in ["rich", "base"]:
        assert out[name].columns() == ALPHABETS[name].columns()
    return out
