import argparse
from pathlib import Path

from huggingface_hub import hf_hub_download

REPO = "yandex/yambda"
FILES = [
    "flat/{size}/multi_event.parquet",
    "artist_item_mapping.parquet",
    "album_item_mapping.parquet",
]
EMBEDDINGS = "embeddings.parquet"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--size", default="50m", choices=["50m", "500m", "5b"])
    parser.add_argument("--out", default=str(Path(__file__).resolve().parents[1] / "data" / "yambda"))
    parser.add_argument("--with-embeddings", action="store_true")
    args = parser.parse_args()

    files = [f.format(size=args.size) for f in FILES]
    if args.with_embeddings:
        files.append(EMBEDDINGS)

    for name in files:
        path = hf_hub_download(REPO, name, repo_type="dataset", local_dir=args.out)
        size_mb = Path(path).stat().st_size / 2**20
        print(f"{name} -> {path} ({size_mb:.1f} MiB)")


if __name__ == "__main__":
    main()
