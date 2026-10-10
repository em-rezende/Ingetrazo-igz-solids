# SPDX-License-Identifier: GPL-3.0-or-later
"""Sphere, domus (hemisphere) and spherical wedge.

A UV sphere built from latitude rings, a northern hemisphere with a flat
base, or a slice of the sphere up to a chosen angle.
"""
from __future__ import annotations

import math

from ._core import TWO_PI, V


SPEC = {
    "name": "Sphere",
    "icon": "tb_sphere",
    "tip": "Full sphere, domus (hemisphere) or spherical wedge.",
    "fields": [
        {"key": "shape", "label": "Type", "type": "choice",
         "choices": [{"value": "sphere", "label": "Full sphere"},
                     {"value": "domus", "label": "Domus (hemisphere)"},
                     {"value": "segment", "label": "Wedge (segment)"}],
         "default": "sphere"},
        {"key": "radius", "label": "Radius", "type": "float",
         "default": 1.0, "min": 0.001, "decimals": 3, "step": 0.1},
        {"key": "h_segments", "label": "Horizontal segments", "type": "int",
         "default": 24, "min": 4, "max": 512},
        {"key": "v_segments", "label": "Vertical segments", "type": "int",
         "default": 12, "min": 2, "max": 512},
        {"key": "angle", "label": "Wedge angle", "type": "float",
         "default": 45.0, "min": 1.0, "max": 360.0, "decimals": 1, "step": 5.0},
    ],
}

ACTIONS = [
    {"name": "Sphere", "icon": "tb_sphere", "params": {"shape": "sphere"}},
    {"name": "Domus", "icon": "tb_domus", "params": {"shape": "domus"}},
    {"name": "Wedge", "icon": "tb_segment", "params": {"shape": "segment"}},
]


def _ring(origin, radius, theta, phis):
    cos_t = math.cos(theta)
    z = origin.z() + radius * math.sin(theta)
    if abs(cos_t) < 1e-9:                       # a pole: a single point
        return [V(origin.x(), origin.y(), z)]
    rho = radius * cos_t
    return [V(origin.x() + rho * math.cos(phi),
              origin.y() + rho * math.sin(phi), z) for phi in phis]


def _weave(faces, rings, n_phi, closed):
    span = range(n_phi) if closed else range(n_phi - 1)
    for i in range(len(rings) - 1):
        lower, upper = rings[i], rings[i + 1]
        if len(lower) == 1:
            for j in span:
                faces.append([lower[0], upper[(j + 1) % n_phi], upper[j]])
        elif len(upper) == 1:
            for j in span:
                faces.append([lower[j], lower[(j + 1) % n_phi], upper[0]])
        else:
            for j in span:
                j2 = (j + 1) % n_phi
                faces.append([lower[j], lower[j2], upper[j2], upper[j]])


def build(params, origin):
    kind = params.get("shape", "sphere")
    radius = max(1e-4, float(params.get("radius", 1.0)))
    segs_h = max(4, int(params.get("h_segments", 24)))
    segs_v = max(2, int(params.get("v_segments", 12)))

    faces = []
    caps = []

    if kind == "domus":
        phis = [TWO_PI * j / segs_h for j in range(segs_h)]
        thetas = [(math.pi / 2.0) * i / segs_v for i in range(segs_v + 1)]
        rings = [_ring(origin, radius, theta, phis) for theta in thetas]
        _weave(faces, rings, segs_h, closed=True)
        caps = [len(faces)]
        faces.append(list(reversed(rings[0])))  # flat base at the equator
        return faces, caps, True

    max_phi = TWO_PI
    if kind == "segment":
        max_phi = math.radians(
            max(1.0, min(360.0, float(params.get("angle", 45.0)))))
    closed = max_phi >= TWO_PI - 1e-6
    count = segs_h if closed else segs_h + 1
    phis = [max_phi * j / segs_h for j in range(count)]
    thetas = [-math.pi / 2.0 + math.pi * i / segs_v
              for i in range(segs_v + 1)]
    rings = [_ring(origin, radius, theta, phis) for theta in thetas]
    _weave(faces, rings, count, closed=closed)

    if not closed:
        # Two flat meridian faces close the slice: from pole to pole at
        # phi = 0 and phi = max, back through the centre.
        first = [ring[0] for ring in rings] + [origin]
        last = [ring[-1] for ring in rings] + [origin]
        first_index = len(faces)
        faces.append(first)
        last_index = len(faces)
        faces.append(list(reversed(last)))
        caps = [first_index, last_index]

    return faces, caps, True
