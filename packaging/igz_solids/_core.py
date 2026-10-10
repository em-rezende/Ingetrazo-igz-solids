# SPDX-License-Identifier: GPL-3.0-or-later
"""igz_solids — shared infrastructure.

Private helper of the ``igz_solids`` extension.  It is intentionally
underscore-prefixed so IngeTrazo's plugin loader ignores it as a plugin
candidate (``core.extensions._candidates`` skips names starting with ``_``).

Everything the ``tb_*`` modules need lives here:

* :func:`circle_points` — a ring of points on a horizontal plane;
* :func:`add_solid` — commit a watertight solid as ONE undo step, with
  correct outward winding and optional soft (smoothed) seams;
* :class:`ParamDialog` — the generic parameter dialog built from a module's
  ``SPEC``;
* :class:`SolidPlacementTool` — click-to-place with a live wireframe preview;
* :func:`run_tool` / :func:`setup` — the toolbar and Extensions-menu wiring.

The placement ``Tool`` subclass MUST live in this submodule, never in
``__init__.py``: the loader instantiates every ``Tool`` subclass *defined in
the plugin module* with no arguments, and one requiring parameters would make
the whole plugin load fail.
"""
from __future__ import annotations

import importlib
import json
import math
import os
import traceback

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QIcon, QPalette, QVector3D
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLabel,
    QSpinBox,
    QToolBar,
    QVBoxLayout,
)

from tools.base import Tool


TWO_PI = 2.0 * math.pi
V = QVector3D

_HERE = os.path.dirname(os.path.abspath(__file__))
_ICONS_DIR = os.path.join(_HERE, "icons")
_I18N_DIR = os.path.join(_HERE, "i18n")
_LIST_FILE = os.path.join(_HERE, "tb_list.txt")


# ---------------------------------------------------------------------------
# Translation
#
# IngeTrazo's ``core.i18n`` keeps English as the *source* language, so the
# strings passed to :func:`tr` here are English and the per-language maps
# (``i18n/es.json``, ``i18n/pt-BR.json``, ``i18n/it.json``) are flat
# ``{english: translation}`` files shipped with the plugin.  The plugin
# catalog is consulted first, then the application's own catalog (a shared
# string such as «Solids» still translates), then the English source.
# ---------------------------------------------------------------------------
_SOURCE_LANG = "en"
_catalog: dict = {}
_catalog_cache: dict = {}
_active_lang = None


def _plugin_lang() -> str:
    """The language IngeTrazo is running in (``"en"`` when unavailable)."""
    try:
        from core.i18n import current_language
        return current_language() or _SOURCE_LANG
    except Exception:
        return _SOURCE_LANG


def _load_catalog(lang: str) -> dict:
    if lang in _catalog_cache:
        return _catalog_cache[lang]
    catalog: dict = {}
    try:
        with open(os.path.join(_I18N_DIR, lang + ".json"),
                  "r", encoding="utf-8") as handle:
            data = json.load(handle)
        catalog = {str(k): str(v) for k, v in data.items()
                   if not str(k).startswith("_")}
    except Exception:
        catalog = {}
    _catalog_cache[lang] = catalog
    return catalog


def tr(text: str, **kwargs) -> str:
    """Translate an English source string; interpolate ``kwargs``."""
    global _catalog, _active_lang
    lang = _plugin_lang()
    if lang != _active_lang:
        _active_lang = lang
        _catalog = {} if lang == _SOURCE_LANG else _load_catalog(lang)
    out = _catalog.get(text)
    if out is None:
        try:
            from core.i18n import tr as app_tr
            out = app_tr(text)
        except Exception:
            out = text
    if kwargs:
        try:
            out = out.format(**kwargs)
        except (KeyError, IndexError, ValueError):
            out = text.format(**kwargs)
    return out


#: Placement options: stable tokens (compared in :func:`run_tool`) plus the
#: English label shown in the dialog.
PLACE_CURSOR = "cursor"
PLACE_ORIGIN = "origin"
PLACE_LABELS = ((PLACE_CURSOR, "At the cursor (click)"),
                (PLACE_ORIGIN, "At the origin (0, 0, 0)"))


# ---------------------------------------------------------------------------
# Icons
# ---------------------------------------------------------------------------

#: IngeTrazo's default theme is dark and the ``_light`` files carry the
#: bright artwork drawn for it.  Set to False to follow the opposite
#: convention (``_light`` = the variant for a light theme), which is what
#: the ``igz_roundcorner`` sample does.
LIGHT_ICONS_FOR_DARK_THEME = True


def load_icon(base_name: str, window) -> QIcon:
    """Themed toolbar icon read from ``icons/``.

    Picks ``<base_name>_light.svg`` or ``<base_name>.svg`` from the window
    palette (see :data:`LIGHT_ICONS_FOR_DARK_THEME`), falling back to the
    other file when the chosen one is missing.
    """
    if not base_name or not os.path.isdir(_ICONS_DIR):
        return QIcon()
    if base_name.endswith(".svg"):
        base_name = base_name[:-4]

    is_dark = True
    try:
        if window is not None:
            background = window.palette().color(QPalette.Window)
            is_dark = background.lightness() < 128
    except Exception:
        pass

    want_light = is_dark if LIGHT_ICONS_FOR_DARK_THEME else not is_dark
    candidates = ([base_name + "_light.svg", base_name + ".svg"] if want_light
                  else [base_name + ".svg", base_name + "_light.svg"])
    for name in candidates:
        path = os.path.join(_ICONS_DIR, name)
        if os.path.isfile(path):
            return QIcon(path)
    return QIcon()


# ---------------------------------------------------------------------------
# Geometry helpers
# ---------------------------------------------------------------------------

def circle_points(origin, radius: float, segments: int, z: float = 0.0):
    """A closed ring of ``segments`` points, CCW seen from +Z, at height ``z``
    above ``origin``'s plane (world +Z)."""
    n = max(3, int(segments))
    return [
        V(origin.x() + radius * math.cos(TWO_PI * i / n),
          origin.y() + radius * math.sin(TWO_PI * i / n),
          origin.z() + z)
        for i in range(n)
    ]


def solid_segments(faces):
    """``[(a, b), ...]`` wireframe edges of a list of vertex loops."""
    segs = []
    for loop in faces:
        n = len(loop)
        for i in range(n):
            a, b = loop[i], loop[(i + 1) % n]
            if (a - b).lengthSquared() > 1e-12:
                segs.append((a, b))
    return segs


def add_solid(viewport, faces, caps=(), smooth: bool = False, name=None):
    """Create a watertight solid as its OWN GROUP, in one undo step.

    ``faces`` is a list of vertex loops (``QVector3D``, metres); ``caps`` are
    the indices of the *flat* faces (lids/annuli) whose rims must stay sharp;
    ``smooth`` softens every other two-sided seam so a curved surface reads as
    one continuous face instead of a set of facets.

    The solid is built in a fresh :class:`~core.mesh.Mesh` and inserted with
    :class:`~core.history.InsertGroupCommand`, so its vertices never weld to
    whatever was already drawn: the whole solid selects, moves and edits as
    one object.  Returns the new ``Group``.
    """
    from core.group import Group
    from core.history import InsertGroupCommand
    from core.mesh import Mesh
    from core.orient import orient_outward

    mesh = Mesh()
    for loop in faces:
        mesh.add_face(loop)
    # The orientation pass only flips a mesh it can prove is closed, and the
    # solid's own mesh is exactly that — independent of the rest of the model.
    try:
        orient_outward(mesh)
    except Exception:
        traceback.print_exc()

    if smooth:
        cap_indices = set(int(c) for c in caps)
        cap_faces = {mesh.faces[i] for i in cap_indices if i < len(mesh.faces)}
        for edge in mesh.edges:
            if (len(edge.faces) == 2
                    and not any(f in cap_faces for f in edge.faces)):
                edge.soft = True

    group = Group(mesh=mesh, name=name or tr("Solid"))
    viewport.history.execute(InsertGroupCommand(group))
    notify = getattr(viewport, "notify_scene_changed", None)
    if callable(notify):
        notify()
    else:
        viewport.update()
    return group


# ---------------------------------------------------------------------------
# Parameter dialog
# ---------------------------------------------------------------------------

class ParamDialog(QDialog):
    """Generic dialog driven by a module's ``SPEC`` "fields" list.

    Field types: ``float`` (length in metres), ``int`` (count) and ``choice``
    (pulldown).  A shared "Positioning" pulldown adds the cursor/origin
    choice to every solid.

    A field may carry ``"follows": {"key": <source>, "values": {...}}`` so that
    changing that source pulldown presets this field — e.g. the Cone/Pyramid
    *Type* sets *Sides* to 24 or 4.
    """

    def __init__(self, spec: dict, parent=None, defaults: dict | None = None) -> None:
        super().__init__(parent)
        self.setWindowTitle(tr(spec.get("name", "Solid")))
        self.setMinimumWidth(360)
        self._widgets: dict = {}
        self._followers: list = []
        defaults = defaults or {}

        outer = QVBoxLayout(self)
        tip = spec.get("tip")
        if tip:
            label = QLabel(tr(tip))
            label.setWordWrap(True)
            outer.addWidget(label)

        form = QFormLayout()
        for field in spec.get("fields", []):
            effective = dict(field)
            if field["key"] in defaults:
                effective["default"] = defaults[field["key"]]
            widget = self._make_field(effective)
            self._widgets[field["key"]] = widget
            form.addRow(QLabel(tr(field.get("label", field["key"]))), widget)
            follow = field.get("follows")
            if follow:
                self._followers.append(
                    (str(follow.get("key")), dict(follow.get("values", {})),
                     field["key"]))
        self._place = QComboBox()
        for token, label in PLACE_LABELS:
            self._place.addItem(tr(label), token)
        form.addRow(QLabel(tr("Positioning")), self._place)
        outer.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        outer.addWidget(buttons)

        self._connect_followers()

    def _connect_followers(self) -> None:
        """Wire each ``follows`` link: a change in the source pulldown sets
        the dependent field to the mapped value (a Cone resets Sides to 24,
        a Pyramid to 4, and so on)."""
        for source_key, _mapping, _target_key in self._followers:
            source = self._widgets.get(source_key)
            if isinstance(source, QComboBox):
                source.currentIndexChanged.connect(
                    lambda _index, key=source_key: self._apply_follow(key))

    def _apply_follow(self, source_key: str) -> None:
        for source, mapping, target_key in self._followers:
            if source != source_key:
                continue
            widget = self._widgets.get(source_key)
            target = self._widgets.get(target_key)
            if widget is None or target is None:
                continue
            value = widget.currentData()
            if value in mapping:
                self._set_value(target, mapping[value])

    @staticmethod
    def _set_value(widget, value) -> None:
        if isinstance(widget, QComboBox):
            index = widget.findData(value)
            if index >= 0:
                widget.setCurrentIndex(index)
        elif isinstance(widget, QSpinBox):
            widget.setValue(int(round(float(value))))
        else:
            widget.setValue(float(value))

    def _make_field(self, field: dict):
        kind = field.get("type", "float")
        if kind == "choice":
            widget = QComboBox()
            for option in field.get("choices", []):
                if isinstance(option, dict):
                    widget.addItem(tr(option.get("label", option.get("value", ""))),
                                   option.get("value"))
                else:
                    widget.addItem(tr(option), option)
            default = field.get("default")
            index = widget.findData(default)
            if index >= 0:
                widget.setCurrentIndex(index)
            return widget
        if kind == "int":
            widget = QSpinBox()
            widget.setRange(int(field.get("min", 0)),
                            int(field.get("max", 100000)))
            widget.setValue(int(field.get("default", 1)))
            return widget
        widget = QDoubleSpinBox()
        widget.setDecimals(int(field.get("decimals", 3)))
        widget.setRange(float(field.get("min", 0.001)),
                        float(field.get("max", 100000.0)))
        widget.setSingleStep(float(field.get("step", 0.1)))
        widget.setValue(float(field.get("default", 1.0)))
        widget.setSuffix(" m")
        return widget

    def values(self) -> dict:
        out: dict = {}
        for key, widget in self._widgets.items():
            if isinstance(widget, QComboBox):
                out[key] = widget.currentData()
            else:
                out[key] = widget.value()
        out["_place"] = self._place.currentData()
        return out


# ---------------------------------------------------------------------------
# Interactive placement
# ---------------------------------------------------------------------------

class SolidPlacementTool(Tool):
    """Follows the cursor with the solid's wireframe; a click drops it."""

    name = "Posicionar sólido"
    uses_snap = True

    def __init__(self, spec: dict, params: dict, builder,
                 name: str | None = None) -> None:
        self.spec = spec
        self.params = params
        self.builder = builder
        self._name_hint = name
        self._base = None
        self._origin = None

    def _name(self) -> str:
        return self._name_hint or tr(self.spec.get("name", "Solid"))

    def on_activate(self, viewport) -> None:
        try:
            viewport.flash_status(
                tr("{name}: click to place  •  Esc exits",
                   name=self._name()), 3500)
        except Exception:
            pass

    def on_deactivate(self, viewport) -> None:
        self._origin = None

    def _base_segments(self):
        if self._base is None:
            faces, _caps, _smooth = self.builder(self.params, V(0.0, 0.0, 0.0))
            self._base = solid_segments(faces)
        return self._base

    def on_hover(self, ctx) -> None:
        self._origin = QVector3D(ctx.world)

    def on_click(self, ctx) -> None:
        origin = QVector3D(ctx.world)
        faces, caps, smooth = self.builder(self.params, origin)
        add_solid(ctx.viewport, faces, caps=caps, smooth=smooth,
                  name=self._name())
        self._origin = origin
        try:
            ctx.viewport.flash_status(
                tr("{name}: solid created.", name=self._name()), 2000)
        except Exception:
            pass

    def on_cancel(self, viewport) -> None:
        self._origin = None

    def rubber_band_lines(self):
        if self._origin is None:
            return []
        offset = self._origin
        return [(a + offset, b + offset) for a, b in self._base_segments()]

    def status_clause(self) -> str:
        return tr("click  place  •  Esc  exit")


# ---------------------------------------------------------------------------
# Plugin wiring
# ---------------------------------------------------------------------------

def read_tb_list():
    """Module names listed in ``tb_list.txt`` (``#`` comments, blanks skipped)."""
    names = []
    try:
        with open(_LIST_FILE, "r", encoding="utf-8") as handle:
            for line in handle:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                names.append(line)
    except Exception:
        traceback.print_exc()
    return names


def load_modules():
    """Import every ``tb_*`` module listed in ``tb_list.txt``."""
    modules = []
    for name in read_tb_list():
        try:
            modules.append(importlib.import_module("." + name, __package__))
        except Exception:
            traceback.print_exc()
    return modules


def run_tool(app, module, defaults: dict | None = None,
             action_name: str | None = None) -> None:
    """Open a solid's dialog, then create it on the cursor or at the origin.

    ``defaults`` preselects fields (used by a module's ``ACTIONS`` so each
    toolbar button starts from its own shape); ``action_name`` is the
    button's label, used to name the group it creates."""
    spec = getattr(module, "SPEC", None)
    builder = getattr(module, "build", None)
    if not isinstance(spec, dict) or not callable(builder):
        return
    dialog = ParamDialog(spec, app.window, defaults)
    if dialog.exec() != QDialog.Accepted:
        return
    params = dialog.values()
    place = params.pop("_place", PLACE_CURSOR)
    name = tr(action_name or spec.get("name", "Solid"))
    viewport = app.viewport
    if place == PLACE_ORIGIN:
        faces, caps, smooth = builder(params, V(0.0, 0.0, 0.0))
        add_solid(viewport, faces, caps=caps, smooth=smooth, name=name)
        try:
            viewport.flash_status(
                tr("{name}: created at the origin.", name=name), 2500)
        except Exception:
            pass
        return
    viewport.set_active_tool(SolidPlacementTool(spec, params, builder, name))


def module_actions(module):
    """The toolbar entries a module exposes.

    A module may define ``ACTIONS`` — a list of ``{"name", "icon",
    "params"}`` — so a single file feeds several buttons (Caixa and Cunha
    from ``tb_box``, Cilindro and Tubo from ``tb_cylinder``…).  Without it,
    the module's ``SPEC`` gives one button.
    """
    spec = getattr(module, "SPEC", {}) or {}
    actions = getattr(module, "ACTIONS", None)
    if not actions:
        return [{
            "name": spec.get("name", "Sólido"),
            "icon": spec.get("icon", ""),
            "params": {},
        }]
    out = []
    for entry in actions:
        out.append({
            "name": entry.get("name", spec.get("name", "Sólido")),
            "icon": entry.get("icon", spec.get("icon", "")),
            "params": dict(entry.get("params", {})),
        })
    return out


def setup(app) -> None:
    """Add the «Solids» toolbar and its Extensions submenu."""
    window = app.window
    modules = load_modules()
    if not modules:
        return

    toolbar = QToolBar(tr("Solids"), window)
    toolbar.setObjectName("igz_solids")
    toolbar.setWindowTitle(tr("Solids"))

    submenu = None
    add_menu = getattr(app, "add_menu", None)
    if callable(add_menu):
        try:
            submenu = add_menu(tr("Solids"))
        except Exception:
            submenu = None

    for module in modules:
        spec = getattr(module, "SPEC", {}) or {}
        tip = tr(spec.get("tip", ""))
        for entry in module_actions(module):
            icon = load_icon(entry["icon"], window)
            action = QAction(icon, tr(entry["name"]), window)
            if tip:
                action.setToolTip(tip)
                action.setStatusTip(tip)
            action.triggered.connect(
                lambda _checked=False, m=module, p=entry["params"],
                n=entry["name"]: run_tool(app, m, p, n))
            toolbar.addAction(action)
            if submenu is not None:
                submenu.addAction(action)

    add_toolbar = getattr(window, "addToolBar", None)
    if callable(add_toolbar):
        add_toolbar(Qt.TopToolBarArea, toolbar)
