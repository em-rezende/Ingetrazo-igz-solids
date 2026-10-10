#!/usr/bin/env python3
# =========================================================================
# Copyright (C) 2026 Ezequiel M. Rezende
# License: GPL-3.0-or-later (same as IngeTrazo)
# =========================================================================
# Build the distributable ``igz_solids.zip`` for the IngeTrazo extension
# catalog (https://github.com/ingelibre/ingetrazo-extensions).
#
# The catalog installs ONE file per entry: a .py file, or a .zip holding a
# single folder with an __init__.py (see TEMPLATE.toml in that repository).
# This extension uses the zip form because it ships several modules, a
# ``tb_list.txt``, an ``i18n/`` folder and a folder of SVG icons.
#
# The archive is built deterministically on purpose: fixed timestamps,
# sorted entries and a fixed create-system, so its SHA-256 changes ONLY
# when the content changes. That is what lets the catalog fingerprint
# (``sha256`` in ``extensions/igz_solids.toml``) be verified and reproduced.
#
# The single top-level folder is assembled from ``packaging/igz_solids/``
# (the code, LICENSE and THIRD-PARTY.md) plus the two READMEs and the
# ``icons/`` folder at the repository root.
#
# Usage:
#     python packaging/build_extension.py
#
# Output:
#     dist/igz_solids.zip
#     dist/igz_solids.zip.sha256   (the value to paste in the catalog entry)
# =========================================================================
from __future__ import annotations

import hashlib
import os
import re
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DIST = os.path.join(ROOT, "dist")

#: Single top-level folder inside the zip (required by the catalog); it is
#: what IngeTrazo unpacks into <plugins>/, so the installed path becomes
#: <plugins>/igz_solids/.
PACKAGE = "igz_solids"
ZIP_NAME = f"{PACKAGE}.zip"

#: The package source folder that becomes the single top-level folder in
#: the zip (its whole tree travels).
PACKAGE_SRC = os.path.join(HERE, PACKAGE)

#: Documentation pulled from the repository root (kept next to the code).
ROOT_DOCS = ["README.md", "README_ptBR.md"]

#: Icons folder in the repository root, flattened into <package>/icons/.
ICONS_DIR = os.path.join(ROOT, "icons")

#: Fixed timestamp so the archive is byte-for-byte reproducible.
FIXED_DATE = (2026, 1, 1, 0, 0, 0)


def read_version() -> str:
    """Read the version from README.md, so it never drifts."""
    try:
        with open(os.path.join(ROOT, "README.md"), encoding="utf-8") as fh:
            match = re.search(r"\*\*Version:\*\*\s*(\S+)", fh.read())
            if match:
                return match.group(1)
    except OSError:
        pass
    return "0.0.0"


def _read(path: str) -> bytes:
    with open(path, "rb") as fh:
        return fh.read()


def collect_entries() -> list[tuple[str, bytes]]:
    """Return ``(arcname, data)`` for every file, sorted by name."""
    entries: list[tuple[str, bytes]] = []

    for base, dirs, files in os.walk(PACKAGE_SRC):
        dirs[:] = sorted(d for d in dirs if d != "__pycache__")
        for name in sorted(files):
            if name.endswith((".pyc", ".pyo")):
                continue
            src = os.path.join(base, name)
            rel = os.path.relpath(src, PACKAGE_SRC).replace(os.sep, "/")
            entries.append((f"{PACKAGE}/{rel}", _read(src)))

    for name in ROOT_DOCS:
        path = os.path.join(ROOT, name)
        if os.path.isfile(path):
            entries.append((f"{PACKAGE}/{name}", _read(path)))

    if os.path.isdir(ICONS_DIR):
        for name in sorted(os.listdir(ICONS_DIR)):
            path = os.path.join(ICONS_DIR, name)
            if os.path.isfile(path) and name.lower().endswith(".svg"):
                entries.append((f"{PACKAGE}/icons/{name}", _read(path)))

    # De-duplicate by archive name (root docs may already live in the package).
    seen: dict[str, bytes] = {}
    for arcname, data in entries:
        seen[arcname] = data
    return sorted(seen.items(), key=lambda item: item[0])


def build() -> str:
    os.makedirs(DIST, exist_ok=True)
    out_zip = os.path.join(DIST, ZIP_NAME)

    with zipfile.ZipFile(out_zip, "w") as zf:
        for arcname, data in collect_entries():
            info = zipfile.ZipInfo(arcname, date_time=FIXED_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3          # 3 = Unix: stable across OSes
            info.external_attr = 0o644 << 16
            zf.writestr(info, data)

    digest = hashlib.sha256(_read(out_zip)).hexdigest()

    with open(out_zip + ".sha256", "w", encoding="ascii") as fh:
        fh.write(f"{digest}  {ZIP_NAME}\n")

    return digest


def main() -> None:
    version = read_version()
    digest = build()
    print(f"igz_solids {version}")
    print(f"  dist/{ZIP_NAME}")
    print(f"  sha256 = \"{digest}\"")
    print("")
    print("  Paste that sha256 into extensions/igz_solids.toml and upload")
    print(f"  dist/{ZIP_NAME} to the GitHub Release of the tag in `download`.")


if __name__ == "__main__":
    main()
