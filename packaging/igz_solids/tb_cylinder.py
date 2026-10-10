# SPDX-License-Identifier: GPL-3.0-or-later
"""Parametric cylinder and tube.

Port of ``tb_cylinder.rb`` (ArkZ ``CilindroTuboTool``): a circular
profile extruded to a solid cylinder, or a hollow tube when an inner
radius is given.
"""
from __future__ import annotations

from ._core import V, circle_points


SPEC = {
    "name": "Cylinder",
    "icon": "tb_cylinder",
    "tip": "Circular cylinder, or a hollow tube (with an inner radius).",
    "fields": [
        {"key": "shape", "label": "Type", "type": "choice",
         "choices": [{"value": "cylinder", "label": "Cylinder"},
                     {"value": "tube", "label": "Tube"}],
         "default": "cylinder"},
        {"key": "outer_radius", "label": "Outer radius", "type": "float",
         "default": 0.5, "min": 0.001, "decimals": 3, "step": 0.1},
        {"key": "inner_radius", "label": "Inner radius (tube)", "type": "float",
         "default": 0.25, "min": 0.0, "decimals": 3, "step": 0.1},
        {"key": "segments", "label": "Segments", "type": "int",
         "default": 24, "min": 6, "max": 512},
        {"key": "height", "label": "Height", "type": "float",
         "default": 2.0, "min": 0.001, "decimals": 3, "step": 0.1},
    ],
}

ACTIONS = [
    {"name": "Cylinder", "icon": "tb_cylinder", "params": {"shape": "cylinder"}},
    {"name": "Tube", "icon": "tb_tube", "params": {"shape": "tube"}},
]


def build(params, origin):
    radius = max(1e-4, float(params.get("outer_radius", 1.0)))
    height = max(1e-4, float(params.get("height", 1.0)))
    segments = max(6, int(params.get("segments", 24)))
    is_tube = params.get("shape") == "tube"

    outer0 = circle_points(origin, radius, segments, 0.0)
    outer1 = circle_points(origin, radius, segments, height)

    faces = []
    if is_tube:
        inner_radius = float(params.get("inner_radius", radius * 0.7))
        if inner_radius <= 0.0 or inner_radius >= radius:
            inner_radius = radius * 0.7
        inner0 = circle_points(origin, inner_radius, segments, 0.0)
        inner1 = circle_points(origin, inner_radius, segments, height)

        for i in range(segments):
            j = (i + 1) % segments
            faces.append([outer0[i], outer0[j], outer1[j], outer1[i]])
        for i in range(segments):
            j = (i + 1) % segments
            faces.append([inner0[i], inner1[i], inner1[j], inner0[j]])

        cap_start = len(faces)
        for i in range(segments):
            j = (i + 1) % segments
            faces.append([outer1[i], outer1[j], inner1[j], inner1[i]])
        for i in range(segments):
            j = (i + 1) % segments
            faces.append([outer0[i], inner0[i], inner0[j], outer0[j]])

        caps = list(range(cap_start, len(faces)))
        return faces, caps, True

    for i in range(segments):
        j = (i + 1) % segments
        faces.append([outer0[i], outer0[j], outer1[j], outer1[i]])

    bottom_index = len(faces)
    faces.append(list(reversed(outer0)))
    top_index = len(faces)
    faces.append(list(outer1))

    return faces, [bottom_index, top_index], True
