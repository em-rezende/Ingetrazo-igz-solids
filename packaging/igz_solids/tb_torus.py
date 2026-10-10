# SPDX-License-Identifier: GPL-3.0-or-later
"""Parametric torus.

Port of ``tb_torus.rb`` (ArkZ ``TorusTool``): a circular spine of radius
``major_radius`` swept by a circular section of radius ``minor_radius``.
The torus is placed flat on the click plane (its axis along +Z).
"""
from __future__ import annotations

import math

from ._core import TWO_PI, V


SPEC = {
    "name": "Torus",
    "icon": "tb_torus",
    "tip": "Torus (ring) from a major radius and a section radius.",
    "fields": [
        {"key": "major_radius", "label": "Major radius (ring)", "type": "float",
         "default": 0,75, "min": 0.001, "decimals": 3, "step": 0.1},
        {"key": "minor_radius", "label": "Minor radius (section)", "type": "float",
         "default": 0.5, "min": 0.001, "decimals": 3, "step": 0.05},
        {"key": "major_segments", "label": "Ring segments", "type": "int",
         "default": 24, "min": 6, "max": 512},
        {"key": "minor_segments", "label": "Section segments", "type": "int",
         "default": 16, "min": 3, "max": 512},
    ],
}


def build(params, origin):
    major = max(1e-4, float(params.get("major_radius", 1.0)))
    minor = max(1e-4, float(params.get("minor_radius", 0.25)))
    if minor >= major:
        minor = major * 0.2
    segs_major = max(6, int(params.get("major_segments", 24)))
    segs_minor = max(3, int(params.get("minor_segments", 16)))

    grid = []
    for i in range(segs_major):
        angle = TWO_PI * i / segs_major
        cos_a, sin_a = math.cos(angle), math.sin(angle)
        ring = []
        for j in range(segs_minor):
            section = TWO_PI * j / segs_minor
            rho = major + minor * math.cos(section)
            ring.append(V(origin.x() + rho * cos_a,
                          origin.y() + rho * sin_a,
                          origin.z() + minor * math.sin(section)))
        grid.append(ring)

    faces = []
    for i in range(segs_major):
        i2 = (i + 1) % segs_major
        for j in range(segs_minor):
            j2 = (j + 1) % segs_minor
            faces.append([grid[i][j], grid[i2][j], grid[i2][j2], grid[i][j2]])

    return faces, (), True
