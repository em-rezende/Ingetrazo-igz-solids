# Submission bundle — IngeTrazo extension catalog

> **Status: GitHub published; catalogue submission prepared (NOT submitted).**
> The repository <https://github.com/em-rezende/Ingetrazo-igz-solids> is live
> (`main`, tag `v1.0.0`) and its **`igz_solids 1.0.0` Release** already serves
> the `igz_solids.zip` asset (sha256 verified). What remains is this submission
> — the entry and the screenshot below, and the pull request —, **deliberately
> not opened yet**, until the author authorises it.

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
  `igz_solids.zip`, which is **already published** (138 148 bytes, verified).
- The `sha256` in the entry must match that asset byte-for-byte:
  `200d0766db4aaa085ca43682ea0994961f4f234808fbbc0373964a1b76e8080f`.
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

## Plugin API compliance (`docs/plugins.md`)

The extension follows the requirements in
<https://github.com/ingelibre/ingetrazo/blob/main/docs/plugins.md>:

| `plugins.md` rule | How this extension meets it |
|---|---|
| A plugin is a `.py` file **or a package directory** | A package `igz_solids/` with `__init__.py`. |
| Every `Tool` subclass *defined in the file* gets an **Extensions** menu entry | Not used: the toolbar and the **Extensions ▸ Solids** submenu are registered in `setup(app)`. The one interactive `Tool` lives in a private submodule (`_core.py`, which the loader skips) and is activated by the extension itself. |
| **A broken plugin cannot break IngeTrazo** | `setup()` is defensive; the `tb_*` modules are imported one by one with `try/except`; risky calls are guarded. |
| Never rely on being importable as `plugins.name`, and **never assume the plugin directory is on `sys.path`** | Only relative imports inside the package (`importlib.import_module(".tb_x", __package__)`); nothing is added to `sys.path`. |
| **Modify the model only through the command layer** (undoable and dirty) | Every edit goes through `viewport.history.execute(InsertGroupCommand(group))`, followed by `viewport.notify_scene_changed()`. Each solid is built in its own mesh and inserted as a **group**, which also honours the warning not to touch `scene.mesh` while a group is being edited. |
| `setup(app)` receives the `ExtensionApp` (API v2) | Uses `app.window`, `app.viewport` and `app.add_menu("Solids")`; the toolbar is added to the main window. |

> The *one-shot* rule in `plugins.md` applies to `Tool` subclasses
> auto-registered by the loader from the plugin file. Here the buttons open a
> dialog; when **At the cursor (click)** is chosen the extension deliberately
> activates its own placement tool (with a live wireframe preview) so the user
> can drop solids — the same behaviour as a built-in tool button, not a rogue
> menu tool.

