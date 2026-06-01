from pathlib import Path
from mcaddon import BaseModel, Manifest
import shutil
import zipfile
import pytest
import requests_cache
import os

session = requests_cache.CachedSession()

CHUNK_SIZE = 8192


class BedrockSamples(BaseModel):
    rp: Path
    bp: Path


def get_top_dir(path: Path) -> Path:
    subdirs = [d for d in path.iterdir() if d.is_dir()]
    if not subdirs:
        raise RuntimeError("No extracted subdir found")
    return subdirs[0]


def download_bedrock_samples(root: Path, resource: Path, behavior: Path) -> None:
    zip_path = root / "vanilla.zip"

    # download
    resp = session.get(
        "https://github.com/Mojang/bedrock-samples/archive/main.zip", stream=True
    )
    resp.raise_for_status()
    with open(zip_path, "wb") as f:
        for chunk in resp.iter_content(CHUNK_SIZE):
            f.write(chunk)

    # extract
    extract_dir = root / "vanilla"
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_dir)

    # find the top-level folder created by GitHub
    base = get_top_dir(extract_dir)

    # move if present
    for name, dest in [
        ("resource_pack", resource / "vanilla"),
        ("behavior_pack", behavior / "vanilla"),
    ]:
        src = base / name
        if src.exists():
            shutil.move(str(src), str(dest))
        else:
            dest.mkdir()


def download_minecraft_samples(root: Path, resource: Path, behavior: Path) -> None:
    zip_path = root / "minecraft.zip"

    # download
    resp = session.get(
        "https://github.com/microsoft/minecraft-samples/archive/main.zip", stream=True
    )
    resp.raise_for_status()
    with open(zip_path, "wb") as f:
        for chunk in resp.iter_content(CHUNK_SIZE):
            f.write(chunk)

    # extract
    extract_dir = root / "minecraft"
    extract_dir.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "r") as z:
        z.extractall(extract_dir)

    # find the top-level folder created by GitHub
    base = get_top_dir(extract_dir)

    # move if present
    bp_count = 0
    rp_count = 0

    for root_dir, _, files in os.walk(base):
        if "manifest.json" in files:
            manifest_fp = Path(root_dir) / "manifest.json"
            # for manifest_fp in base.glob("**/manifest.json"):
            pack_dir = manifest_fp.parent

            # Check pack type from manifest
            sel = behavior
            count = 0
            pack_type = Manifest.guess_pack_type(manifest_fp)
            if pack_type == "resource_pack":
                sel = resource
                rp_count += 1
                count = rp_count
            else:
                bp_count += 1
                count = bp_count
            shutil.move(
                str(pack_dir), str(sel / Path(pack_dir.name + "_" + str(count)))
            )


@pytest.fixture(scope="session")
def bedrock_samples(tmp_path_factory):
    """
    Download test files.
    """
    root = tmp_path_factory.mktemp("bedrock_samples")
    resource = root / "resource_packs"
    behavior = root / "behavior_packs"

    download_bedrock_samples(root, resource, behavior)
    download_minecraft_samples(root, resource, behavior)

    return BedrockSamples(rp=Path(resource), bp=Path(behavior))
