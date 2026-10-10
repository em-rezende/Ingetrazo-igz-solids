# Submission bundle — IngeTrazo extension catalog

> **Status: prepared, NOT yet published.** The GitHub repository
> <https://github.com/em-rezende/Ingetrazo-igz-solids> and its `v1.0.0`
> Release still have to be created and pushed. Do that only when the author
> authorises the publication — the files here are ready for that moment.
> A local git repository is already initialised with the `origin` remote
> configured; nothing has been committed, tagged or pushed yet.

Copy these two things into the catalog repository
(<https://github.com/ingelibre/ingetrazo-extensions>):

| From here | To the catalog repository |
|---|---|
| `extensions/igz_solids.toml` | `extensions/igz_solids.toml` |
| `screenshots/igz_solids.png` | `screenshots/igz_solids.png` |

The screenshot shows the **Solids** toolbar, the Geodesic Sphere dialog and
some solids built with them (1201×750 px, ~68 KB) and must keep the file name
`igz_solids.png` — that is the name in the entry's `screenshot` field.

Then open the pull request (browser: *Add file ▸ Create new file* and
*Add file ▸ Upload files* → **Propose changes** → **Create pull request**)
and fill in the template checklist.

## Before you submit

- The `download` URL points at the **v1.0.0** GitHub Release asset
  `igz_solids.zip`, which **does not exist yet**: publish it first (see
  [`../PUBLISHING.md`](../PUBLISHING.md) and `packaging/publish_release.ps1`).
- The `sha256` in the entry must match that asset byte-for-byte:
  `efd46476a5e23d2dad455a7d272758535283e474b943dc8b864c602bc0d7567a`.
  Rebuild with `packaging/build_extension.ps1` (or `packaging/build_extension.py`)
  if the code changed, and paste the value it prints. (If it is wrong, the
  catalog's automatic check tells you the right one.)
- `version` is **1.0.0**.

## What the catalog's check demands

Every pull request runs `pytest -q tests` and `python tools/catalog.py check`.
Both refuse an entry that breaks any rule below (the offline tests catch all of
them except the download itself), so the lengths matter:

| Field | Rule |
|---|---|
| `name` | at most **60** characters per language |
| `summary` | at most **240** characters per language |
| `description` | optional, at most **2000** characters per language |
| `tags` | 1 to 4, from the catalog's fixed list |
| `license` | SPDX id of a free licence (here `GPL-3.0-or-later`) |
| `download` | `https://`, ending in `.py` or `.zip`, naming a tag or a commit — never a branch |
| `sha256` | the 64-character hash of exactly that file |
| `screenshot` | a file name in `screenshots/`, at most 600 KB, `.png`/`.jpg`/`.webp` |

The archive itself must hold **one** package folder with an `__init__.py` inside
(here `igz_solids/`), at most 5 MB on disk, and the code must expose a
top-level `setup(app)` function or a `Tool` subclass.

Full, step-by-step instructions are in [`../PUBLISHING.md`](../PUBLISHING.md).
