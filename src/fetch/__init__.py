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


def fetch(ds, force=False):
    from addressvault import Archived
    v = _vault(ds)
    v.pull(ds.slug, force=force)
    try:
        path = v.path(ds.slug, "latest")
    except Archived:  # latest is an unchanged day pointing at a cold canonical
        v.thaw(ds.slug, v.snapshot(ds.slug, "latest").date)
        path = v.path(ds.slug, "latest")
    with open(path, encoding="utf-8") as f:
        features = json.load(f).get("features", [])
    return path, features
