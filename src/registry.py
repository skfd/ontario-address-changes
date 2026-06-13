"""Dataset registry: load and validate per-city configs from datasets/*.toml."""

import os
import tomllib
from dataclasses import dataclass, field

DATASETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets")

_REQUIRED = ("slug", "provider", "data_url", "access", "format")
_VALID_ACCESS = ("arcgis", "static")
_VALID_FORMAT = ("geojson", "shapefile")
_VALID_CLASSES = ("place_name", "status", "boundary")


@dataclass
class Dataset:
    slug: str
    provider: str
    data_url: str
    access: str
    format: str
    license_name: str = ""
    osm_compatible: str = ""
    source_crs: str = ""  # e.g. "EPSG:2952"; reproject to WGS84 when coords are out of lon/lat range
    key_field: str = ""
    synth_fields: list = field(default_factory=lambda: ["full"])
    fields: dict = field(default_factory=dict)
    ignore_fields: list = field(default_factory=list)  # source props excluded from change detection
    classes: dict = field(default_factory=dict)  # change class -> source props (see _VALID_CLASSES)

    @property
    def data_dir(self):
        root = os.path.dirname(DATASETS_DIR)
        return os.path.join(root, "data", self.slug)

    @property
    def db_path(self):
        return os.path.join(self.data_dir, f"{self.slug}.db")


def _parse(path):
    with open(path, "rb") as f:
        raw = tomllib.load(f)

    missing = [k for k in _REQUIRED if not raw.get(k)]
    if missing:
        raise ValueError(f"{os.path.basename(path)}: missing required keys: {missing}")
    if raw["access"] not in _VALID_ACCESS:
        raise ValueError(f"{path}: access must be one of {_VALID_ACCESS}")
    if raw["format"] not in _VALID_FORMAT:
        raise ValueError(f"{path}: format must be one of {_VALID_FORMAT}")
    classes = raw.get("classes", {})
    bad = [k for k in classes if k not in _VALID_CLASSES]
    if bad:
        raise ValueError(f"{path}: unknown classes {bad}; valid: {_VALID_CLASSES}")

    identity = raw.get("identity", {})
    return Dataset(
        slug=raw["slug"],
        provider=raw["provider"],
        data_url=raw["data_url"],
        access=raw["access"],
        format=raw["format"],
        license_name=raw.get("license_name", ""),
        osm_compatible=raw.get("osm_compatible", ""),
        source_crs=raw.get("source_crs", ""),
        key_field=identity.get("key_field", ""),
        synth_fields=identity.get("synth_fields", ["full"]),
        fields=raw.get("fields", {}),
        ignore_fields=raw.get("ignore_fields", []),
        classes=classes,
    )


def load_all():
    """Return all datasets sorted by slug."""
    out = []
    for name in sorted(os.listdir(DATASETS_DIR)):
        if name.endswith(".toml"):
            out.append(_parse(os.path.join(DATASETS_DIR, name)))
    return out


def load(slug):
    """Load a single dataset by slug."""
    path = os.path.join(DATASETS_DIR, f"{slug}.toml")
    if not os.path.exists(path):
        raise ValueError(f"No dataset config for slug '{slug}' ({path})")
    return _parse(path)
