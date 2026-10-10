# SPDX-License-Identifier: GPL-3.0-or-later
"""Regular N-sided prism.

Port of ``tb_prism.rb`` (ArkZ ``PrismaTool``): a regular polygon extruded
to a prism.  With 12 sides or more it behaves as a faceted cylinder and
its wall seams are smoothed, exactly as in the Ruby original.
"""
from __future__ import annotations

from ._core import V, circle_points


SPEC = {
    "name": "Prism",
    "icon": "tb_prism",
    "tip": "Regular prism from an N-sided polygon (≥12 sides reads round).",
    "fields": [
        {"key": "radius", "label": "Base radius", "type": "float",
         "default": 1.0, "min": 0.001, "decimals": 3, "step": 0.1},
        {"key": "height", "label": "Height", "type": "float",
         "default": 2.0, "min": 0.001, "decimals": 3, "step": 0.1},
        {"key": "sides", "label": "Sides", "type": "int",
         "default": 6, "min": 3, "max": 512},
    ],
}


def build(params, origin):
    radius = max(1e-4, float(params.get("radius", 1.0)))
    height = max(1e-4, float(params.get("height", 1.0)))
    sides = max(3, int(params.get("sides", 6)))

    base = circle_points(origin, radius, sides, 0.0)
    top = [point + V(0.0, 0.0, height) for point in base]

    faces = []
    for i in range(sides):
        j = (i + 1) % sides
        faces.append([base[i], base[j], top[j], top[i]])

    bottom_index = len(faces)
    faces.append(list(reversed(base)))
    top_index = len(faces)
    faces.append(list(top))

    caps = [bottom_index, top_index]
    smooth = sides >= 12
    return faces, caps, smooth
