# SPDX-License-Identifier: GPL-3.0-or-later
"""Parametric capsule.

Port of ``tb_capsule.rb`` (ArkZ ``CapsulaTool``): a cylindrical body
capped by two hemispheres of the same radius.  The click point is the
south pole; the body rises towards +Z.
"""
from __future__ import annotations

import math

from ._core import V, circle_points


SPEC = {
    "name": "Capsule",
    "icon": "tb_capsule",
    "tip": "Capsule: a cylinder with spherical caps at both ends.",
    "fields": [
        {"key": "radius", "label": "Radius", "type": "float",
         "default": 0.5, "min": 0.001, "decimals": 3, "step": 0.1},
        {"key": "body_height", "label": "Body height", "type": "float",
         "default": 1.5, "min": 0.0, "decimals": 3, "step": 0.1},
        {"key": "h_segments", "label": "Horizontal segments", "type": "int",
         "default": 24, "min": 4, "max": 512},
        {"key": "v_segments", "label": "Segments per cap", "type": "int",
         "default": 8, "min": 2, "max": 512},
    ],
}


def _profile(radius, body, segs_v):
    """``(rho, z)`` points of the meridian, from the south to the north pole."""
    points = []
    for i in range(segs_v + 1):
        theta = -math.pi / 2.0 + (math.pi / 2.0) * i / segs_v
        points.append((radius * math.cos(theta),
                       radius + radius * math.sin(theta)))
    points.append((radius, radius + body))
    for i in range(1, segs_v + 1):
        theta = (math.pi / 2.0) * i / segs_v
        points.append((radius * math.cos(theta),
                       radius + body + radius * math.sin(theta)))
    # Drop repeats (a zero body length duplicates the equator ring).
    clean = [points[0]]
    for point in points[1:]:
        if (abs(point[0] - clean[-1][0]) < 1e-9
                and abs(point[1] - clean[-1][1]) < 1e-9):
            continue
        clean.append(point)
    return clean


def build(params, origin):
    radius = max(1e-4, float(params.get("radius", 0.5)))
    body = max(0.0, float(params.get("body_height", 0.0)))
    segs_h = max(4, int(params.get("h_segments", 24)))
    segs_v = max(2, int(params.get("v_segments", 8)))

    rings = []
    for rho, z in _profile(radius, body, segs_v):
        if rho < 1e-9:
            rings.append([V(origin.x(), origin.y(), origin.z() + z)])
        else:
            rings.append(circle_points(origin, rho, segs_h, z))

    faces = []
    for i in range(len(rings) - 1):
        lower, upper = rings[i], rings[i + 1]
        if len(lower) == 1:
            for j in range(segs_h):
                j2 = (j + 1) % segs_h
                faces.append([lower[0], upper[j2], upper[j]])
        elif len(upper) == 1:
            for j in range(segs_h):
                j2 = (j + 1) % segs_h
                faces.append([lower[j], lower[j2], upper[0]])
        else:
            for j in range(segs_h):
                j2 = (j + 1) % segs_h
                faces.append([lower[j], lower[j2], upper[j2], upper[j]])

    return faces, (), True
