# SPDX-License-Identifier: GPL-3.0-or-later
"""Parametric box and wedge.

A base rectangle plus an extrusion, or a triangular wedge rising from one
edge.
"""
from __future__ import annotations

from ._core import V


SPEC = {
    "name": "Box",
    "icon": "tb_box",
    "tip": "Parametric box (X × Y × Z) or a triangular wedge.",
    "fields": [
        {"key": "width", "label": "Width (X)", "type": "float",
         "default": 1.0, "min": 0.001, "decimals": 3, "step": 0.1},
        {"key": "length", "label": "Length (Y)", "type": "float",
         "default": 1.0, "min": 0.001, "decimals": 3, "step": 0.1},
        {"key": "height", "label": "Height (Z)", "type": "float",
         "default": 2.0, "min": 0.001, "decimals": 3, "step": 0.1},
        {"key": "shape", "label": "Type", "type": "choice",
         "choices": [{"value": "box", "label": "Box"},
                     {"value": "wedge", "label": "Wedge"}],
         "default": "box"},
    ],
}

ACTIONS = [
    {"name": "Box", "icon": "tb_box", "params": {"shape": "box"}},
    {"name": "Wedge", "icon": "tb_wedge", "params": {"shape": "wedge"}},
]


def build(params, origin):
    """Return ``(faces, cap_indices, smooth)`` for the box/wedge.

    The origin is the base corner (p1); X runs along ``largura``, Y along
    ``comprimento`` and the solid grows towards +Z.
    """
    w = max(1e-4, float(params.get("width", 1.0)))
    length = max(1e-4, float(params.get("length", 1.0)))
    height = max(1e-4, float(params.get("height", 1.0)))

    p1 = V(origin.x(), origin.y(), origin.z())
    p2 = p1 + V(w, 0.0, 0.0)
    p3 = p1 + V(w, length, 0.0)
    p4 = p1 + V(0.0, length, 0.0)

    def up(point):
        return point + V(0.0, 0.0, height)

    if params.get("shape") == "wedge":
        # Triangular prism: bottom, the vertical wall at y=0, the slope
        # down to the far edge, and the two triangular flanks.
        faces = [
            [p1, p4, p3, p2],
            [p1, p2, up(p2), up(p1)],
            [up(p1), up(p2), p3, p4],
            [p1, up(p1), p4],
            [p2, p3, up(p2)],
        ]
    else:
        faces = [
            [p1, p4, p3, p2],
            [up(p1), up(p2), up(p3), up(p4)],
            [p1, p2, up(p2), up(p1)],
            [p2, p3, up(p3), up(p2)],
            [p3, p4, up(p4), up(p3)],
            [p4, p1, up(p1), up(p4)],
        ]

    # Every face is flat: crisp edges throughout.
    caps = list(range(len(faces)))
    return faces, caps, False
