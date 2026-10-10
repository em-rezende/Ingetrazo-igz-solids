# SPDX-License-Identifier: GPL-3.0-or-later
"""Cone, pyramid and truncated cone/pyramid.

Port of ``tb_frustrum.rb`` (ArkZ ``FrustrumTool``): a base polygon joined
to a top polygon (a trunc), or to a single apex when the top radius is
zero.  A cone is a many-sided shape with smooth walls; a pyramid keeps its
facets crisp.
"""
from __future__ import annotations

from ._core import V, circle_points


SPEC = {
    "name": "Cone / Pyramid",
    "icon": "tb_cone",
    "tip": "Cone (≥12 sides, smooth) or faceted pyramid, with optional truncation.",
    "fields": [
        {"key": "shape", "label": "Type", "type": "choice",
         "choices": [{"value": "cone", "label": "Cone"},
                     {"value": "pyramid", "label": "Pyramid"}],
         "default": "cone"},
        {"key": "base_radius", "label": "Base radius", "type": "float",
         "default": 1.0, "min": 0.001, "decimals": 3, "step": 0.1},
        {"key": "top_radius", "label": "Top radius (0 = apex)", "type": "float",
         "default": 0.0, "min": 0.0, "decimals": 3, "step": 0.1},
        {"key": "height", "label": "Height", "type": "float",
         "default": 2.0, "min": 0.001, "decimals": 3, "step": 0.1},
        {"key": "sides", "label": "Sides", "type": "int",
         "default": 24, "min": 3, "max": 512,
         # Choosing the Type presets the sides, so a Cone (24) and a Pyramid
         # (4) each come out right when the pulldown changes in the dialog —
         # the geometry is the same polygon; the type only picks the count
         # and whether the walls are smoothed.
         "follows": {"key": "shape",
                     "values": {"cone": 24, "pyramid": 4}}},
    ],
}

ACTIONS = [
    {"name": "Cone", "icon": "tb_cone",
     "params": {"shape": "cone", "sides": 24}},
    {"name": "Pyramid", "icon": "tb_pyramid",
     "params": {"shape": "pyramid", "sides": 4}},
]


def build(params, origin):
    radius_base = max(1e-4, float(params.get("base_radius", 1.0)))
    radius_top = max(0.0, float(params.get("top_radius", 0.0)))
    height = float(params.get("height", 1.0))
    sides = max(3, int(params.get("sides", 24)))
    is_cone = params.get("shape", "cone") == "cone"

    base = circle_points(origin, radius_base, sides, 0.0)
    faces = []

    if radius_top > 1e-6:
        top = circle_points(origin, radius_top, sides, height)
        for i in range(sides):
            j = (i + 1) % sides
            faces.append([base[i], base[j], top[j], top[i]])
        base_index = len(faces)
        faces.append(list(reversed(base)))
        top_index = len(faces)
        faces.append(list(top))
        caps = [base_index, top_index]
    else:
        apex = V(origin.x(), origin.y(), origin.z() + height)
        for i in range(sides):
            j = (i + 1) % sides
            faces.append([base[i], base[j], apex])
        base_index = len(faces)
        faces.append(list(reversed(base)))
        caps = [base_index]

    return faces, caps, is_cone
