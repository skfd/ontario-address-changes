"""Fetch dispatch: route a dataset to its access-specific fetcher.

Each fetcher returns (filepath, features) where filepath is the saved snapshot
on disk and features is a list of GeoJSON Feature dicts in EPSG:4326.
"""


def fetch(ds, force=False):
    if ds.access == "arcgis":
        from src.fetch import arcgis
        return arcgis.fetch(ds, force=force)
    if ds.access == "static":
        from src.fetch import static
        return static.fetch(ds, force=force)
    raise ValueError(f"Unknown access protocol: {ds.access}")
