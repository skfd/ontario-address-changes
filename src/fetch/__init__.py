"""Fetch dispatch -> address-vault.

The tracker no longer pulls city sites directly. ``fetch`` pulls the dataset's
latest snapshot through address-vault (the central tiered store) and returns the
same ``(filepath, features)`` contract the importer and diff expect: the saved
GeoJSON path plus its features parsed into memory (EPSG:4326). The dataset's
data-source keys are byte-compatible with the vault's Source, so it is seeded
straight from the dataset config.

Requires ADDRESSVAULT_DIR to point at the vault folder.
"""

import json


def _vault(ds):
    from addressvault import Source, Vault
    v = Vault()  # uses ADDRESSVAULT_DIR
    v.add_source(Source(
        slug=ds.slug, provider=ds.provider, data_url=ds.data_url,
        access=ds.access, format=ds.format, source_crs=ds.source_crs,
        fields=ds.fields, license_name=ds.license_name,
    ))
    return v


def fetch_path(ds, force=False):
    """Pull (or reuse) the latest snapshot and return its hot path, unparsed.
    Lets callers check "already imported" by filename before paying for a
    full parse of the (possibly ~590 MB) GeoJSON."""
    from addressvault import Archived
    v = _vault(ds)
    # wait=True: coalesce onto an in-flight pull of this slug rather than erroring
    # or starting a duplicate download.
    v.pull(ds.slug, force=force, wait=True)
    try:
        return v.path(ds.slug, "latest")
    except Archived:  # latest is an unchanged day pointing at a cold canonical
        v.thaw(ds.slug, v.snapshot(ds.slug, "latest").date, wait=True)
        return v.path(ds.slug, "latest")


def load_features(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f).get("features", [])


def fetch(ds, force=False):
    path = fetch_path(ds, force=force)
    return path, load_features(path)
