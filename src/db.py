"""Per-dataset SQLite store: generalized Slowly-Changing-Dimension Type-2.

Each dataset gets its own DB at <data>/<slug>/<slug>.db. An address row is valid
for snapshots [min_snapshot_id, max_snapshot_id]. A record is "unchanged" when the
same identity_key reappears with the same payload_hash; otherwise it's new/modified.
"""

import hashlib
import os
import sqlite3
from datetime import datetime

from src import normalize

_STAGING_COLS = ["identity_key", "number", "street", "unit", "full",
                 "longitude", "latitude", "props", "payload_hash"]


def _connect(ds):
    os.makedirs(ds.data_dir, exist_ok=True)
    conn = sqlite3.connect(ds.db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.row_factory = sqlite3.Row
    return conn


def init_db(ds):
    conn = _connect(ds)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS snapshots (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            downloaded  TEXT NOT NULL,
            row_count   INTEGER NOT NULL,
            filename    TEXT NOT NULL,
            content_hash TEXT,
            remote_last_modified TEXT,
            remote_content_length INTEGER,
            skipped     INTEGER DEFAULT 0
        );

        CREATE TABLE IF NOT EXISTS addresses (
            min_snapshot_id  INTEGER NOT NULL REFERENCES snapshots(id),
            max_snapshot_id  INTEGER NOT NULL REFERENCES snapshots(id),
            identity_key     TEXT NOT NULL,
            number           TEXT,
            street           TEXT,
            unit             TEXT,
            full             TEXT,
            longitude        REAL,
            latitude         REAL,
            props            TEXT,
            payload_hash     TEXT,
            PRIMARY KEY (identity_key, min_snapshot_id)
        );

        CREATE INDEX IF NOT EXISTS idx_addr_active ON addresses(max_snapshot_id);
        CREATE INDEX IF NOT EXISTS idx_addr_key_max ON addresses(identity_key, max_snapshot_id);
    """)
    conn.commit()
    return conn


def _last_snapshot(conn):
    return conn.execute(
        "SELECT * FROM snapshots WHERE skipped = 0 ORDER BY id DESC LIMIT 1"
    ).fetchone()


def _records(ds, features):
    """Normalize features and dedupe by identity_key (keep first)."""
    seen = set()
    out = []
    dups = 0
    for feat in features:
        rec = normalize.canonical(ds, feat)
        if rec is None:
            continue
        if rec["identity_key"] in seen:
            dups += 1
            continue
        seen.add(rec["identity_key"])
        out.append(rec)
    if dups:
        print(f"  note: {dups:,} duplicate identity_key rows dropped")
    return out


def _content_hash(records):
    h = hashlib.sha1()
    for line in sorted(f"{r['identity_key']}|{r['payload_hash']}" for r in records):
        h.update(line.encode("utf-8"))
        h.update(b"\n")
    return h.hexdigest()


def import_snapshot(ds, filepath, features, headers=None):
    """Import normalized features as a new snapshot using SCD-2 delta logic."""
    conn = init_db(ds)
    headers = headers or {}
    filename = os.path.basename(filepath)

    if conn.execute("SELECT 1 FROM snapshots WHERE filename = ?", (filename,)).fetchone():
        print(f"  already imported: {filename}")
        conn.close()
        return

    records = _records(ds, features)
    row_count = len(records)
    if row_count == 0:
        conn.close()
        raise ValueError("0 usable rows (no geometry / no identity) — aborting")

    content_hash = _content_hash(records)
    prev = _last_snapshot(conn)

    if prev and prev["content_hash"] == content_hash:
        print(f"  no changes since snapshot {prev['id']} (content hash match) — recording skip")
        conn.execute(
            "INSERT INTO snapshots (downloaded, row_count, filename, content_hash, skipped) "
            "VALUES (?, ?, ?, ?, 1)",
            (datetime.now().isoformat(), row_count, filename, content_hash))
        conn.commit()
        conn.close()
        return

    cur = conn.execute(
        "INSERT INTO snapshots (downloaded, row_count, filename, content_hash, "
        "remote_last_modified, remote_content_length) VALUES (?, ?, ?, ?, ?, ?)",
        (datetime.now().isoformat(), row_count, filename, content_hash,
         headers.get("Last-Modified"), headers.get("Content-Length")))
    curr_id = cur.lastrowid
    prev_id = prev["id"] if prev else None

    conn.execute("DROP TABLE IF EXISTS staging")
    conn.execute("""
        CREATE TEMPORARY TABLE staging (
            identity_key TEXT, number TEXT, street TEXT, unit TEXT, full TEXT,
            longitude REAL, latitude REAL, props TEXT, payload_hash TEXT)
    """)
    conn.executemany(
        f"INSERT INTO staging ({', '.join(_STAGING_COLS)}) "
        f"VALUES ({', '.join('?' * len(_STAGING_COLS))})",
        [tuple(r[c] for c in _STAGING_COLS) for r in records])
    conn.execute("CREATE INDEX idx_staging_key ON staging(identity_key)")

    cols = ", ".join(_STAGING_COLS)
    if prev_id is None:
        conn.execute(
            f"INSERT INTO addresses (min_snapshot_id, max_snapshot_id, {cols}) "
            f"SELECT ?, ?, {cols} FROM staging", (curr_id, curr_id))
        added = row_count
        modified = 0
    else:
        # unchanged: same identity_key AND same payload_hash -> extend validity
        conn.execute("""
            UPDATE addresses SET max_snapshot_id = ?
            WHERE max_snapshot_id = ? AND EXISTS (
                SELECT 1 FROM staging s
                WHERE s.identity_key = addresses.identity_key
                  AND s.payload_hash = addresses.payload_hash)
        """, (curr_id, prev_id))

        # new + modified: staging keys not already advanced to curr_id
        ins = conn.execute(f"""
            INSERT INTO addresses (min_snapshot_id, max_snapshot_id, {cols})
            SELECT ?, ?, {cols} FROM staging s
            WHERE s.identity_key NOT IN (
                SELECT identity_key FROM addresses WHERE max_snapshot_id = ?)
        """, (curr_id, curr_id, curr_id))
        inserted = ins.rowcount

        # of those inserted, how many are modifications (key existed at prev)?
        modified = conn.execute("""
            SELECT COUNT(*) FROM addresses a
            WHERE a.min_snapshot_id = ? AND EXISTS (
                SELECT 1 FROM addresses p
                WHERE p.identity_key = a.identity_key AND p.max_snapshot_id = ?)
        """, (curr_id, prev_id)).fetchone()[0]
        added = inserted - modified

    conn.execute("DROP TABLE staging")
    conn.commit()
    conn.close()
    print(f"  snapshot {curr_id}: {row_count:,} rows  (+{added:,} new, ~{modified:,} modified)")
    return curr_id


def get_snapshots(ds):
    conn = init_db(ds)
    rows = conn.execute("SELECT * FROM snapshots ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def latest_snapshot_id(conn):
    row = conn.execute(
        "SELECT MAX(id) FROM snapshots WHERE skipped = 0").fetchone()[0]
    return row


def active_points(ds):
    """(lon, lat) for every active row of the latest non-skipped snapshot."""
    conn = init_db(ds)
    sid = latest_snapshot_id(conn)
    if sid is None:
        conn.close()
        return []
    rows = conn.execute(
        "SELECT longitude, latitude FROM addresses "
        "WHERE min_snapshot_id <= ? AND max_snapshot_id >= ? "
        "AND longitude IS NOT NULL AND latitude IS NOT NULL",
        (sid, sid)).fetchall()
    conn.close()
    return [(r["longitude"], r["latitude"]) for r in rows]
