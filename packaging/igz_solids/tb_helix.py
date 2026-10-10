# SPDX-License-Identifier: GPL-3.0-or-later
"""Solid helix (tubular spring).

A circular tube swept along a helix.  Each section is oriented with the
Frenet–Serret frame of the path, so the ring never twists.
"""
from __future__ import annotations

import math

from ._core import TWO_PI, V


SPEC = {
    "name": "Helix",
    "icon": "tb_helix",
    "tip": "Solid helix (spring): a tube swept along a helix.",
    "fields": [
        {"key": "helix_radius", "label": "Helix radius", "type": "float",
         "default": 1.0, "min": 0.001, "decimals": 3, "step": 0.1},
        {"key": "tube_radius", "label": "Tube radius", "type": "float",
         "default": 0.25, "min": 0.001, "decimals": 3, "step": 0.05},
        {"key": "height", "label": "Total height", "type": "float",
         "default": 2.0, "min": 0.001, "decimals": 3, "step": 0.1},
        {"key": "turns", "label": "Turns", "type": "float",
         "default": 2.0, "min": 0.1, "decimals": 2, "step": 0.5},
        {"key": "helix_segments", "label": "Segments per turn", "type": "int",
         "default": 24, "min": 6, "max": 512},
        {"key": "tube_segments", "label": "Tube segments", "type": "int",
         "default": 12, "min": 4, "max": 512},
    ],
}


def build(params, origin):
    helix_radius = max(1e-4, float(params.get("helix_radius", 1.0)))
    tube_radius = max(1e-4, float(params.get("tube_radius", 0.15)))
    if tube_radius >= helix_radius:
        tube_radius = helix_radius * 0.4
    height = float(params.get("height", 1.0))
    turns = max(0.1, float(params.get("turns", 1.0)))
    segs_helix = max(6, int(params.get("helix_segments", 24)))
    segs_tube = max(4, int(params.get("tube_segments", 12)))

    total = max(4, int(round(turns * segs_helix)))
    pitch = height / (turns * TWO_PI)

    grid = []
    for i in range(total + 1):
        angle = (i / segs_helix) * TWO_PI
        centre = V(origin.x() + helix_radius * math.cos(angle),
                   origin.y() + helix_radius * math.sin(angle),
                   origin.z() + (i / total) * height)
        tangent = V(-helix_radius * math.sin(angle),
                    helix_radius * math.cos(angle), pitch).normalized()
        normal = V(-math.cos(angle), -math.sin(angle), 0.0).normalized()
        binormal = V.crossProduct(tangent, normal).normalized()

        ring = []
        for j in range(segs_tube):
            section = TWO_PI * j / segs_tube
            ring.append(centre
                        + normal * (math.cos(section) * tube_radius)
                        + binormal * (math.sin(section) * tube_radius))
        grid.append(ring)

    faces = []
    for i in range(total):
        for j in range(segs_tube):
            j2 = (j + 1) % segs_tube
            faces.append([grid[i][j], grid[i][j2],
                          grid[i + 1][j2], grid[i + 1][j]])

    first_index = len(faces)
    faces.append(list(reversed(grid[0])))
    last_index = len(faces)
    faces.append(list(grid[total]))

    return faces, [first_index, last_index], True
