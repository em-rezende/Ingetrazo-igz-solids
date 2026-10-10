# SPDX-License-Identifier: GPL-3.0-or-later
"""Geodesic sphere.

A tetrahedron, an octahedron or an icosahedron whose faces are recursively
subdivided (frequency) and projected onto a sphere of the given radius, plus
a football (the truncated icosahedron).
"""
from __future__ import annotations

import math

from ._core import V


SQRT2 = math.sqrt(2.0)
SQRT3 = math.sqrt(3.0)
TETRA_Q = SQRT2 / 3.0
TETRA_R = 1.0 / 3.0
TETRA_S = SQRT2 / SQRT3
TETRA_T = 2.0 * SQRT2 / 3.0
GOLDEN_MEAN = (math.sqrt(5.0) + 1.0) / 2.0

SPEC = {
    "name": "Geodesic Sphere",
    "icon": "tb_geodesic",
    "tip": "Geodesic sphere: a subdivided tetrahedron, octahedron or icosahedron.",
    "fields": [
        {"key": "base", "label": "Base geometry", "type": "choice",
         "choices": [{"value": "tetra", "label": "Tetrahedron"},
                     {"value": "octa", "label": "Octahedron"},
                     {"value": "icosa", "label": "Icosahedron"},
                     {"value": "football", "label": "Football (soccer ball)"}],
         "default": "icosa"},
        {"key": "radius", "label": "Radius", "type": "float",
         "default": 1.0, "min": 0.001, "decimals": 3, "step": 0.1},
        {"key": "frequency", "label": "Frequency (subdivisions)", "type": "int",
         "default": 2, "min": 0, "max": 4},
        {"key": "finish", "label": "Finish", "type": "choice",
         "choices": [{"value": "flat", "label": "Don't smooth"},
                     {"value": "smooth", "label": "Smooth"}],
         "default": "flat"},
    ],
}

_POINTS = {
    "tetra": {
        "a": (-TETRA_S, -TETRA_Q, -TETRA_R),
        "b": (TETRA_S, -TETRA_Q, -TETRA_R),
        "c": (0.0, TETRA_T, -TETRA_R),
        "d": (0.0, 0.0, 1.0),
    },
    "octa": {
        "a": (0.0, 0.0, 1.0), "b": (1.0, 0.0, 0.0), "c": (0.0, -1.0, 0.0),
        "d": (-1.0, 0.0, 0.0), "e": (0.0, 1.0, 0.0), "f": (0.0, 0.0, -1.0),
    },
    "icosa": {
        "a": (1.0, GOLDEN_MEAN, 0.0), "b": (1.0, -GOLDEN_MEAN, 0.0),
        "c": (-1.0, -GOLDEN_MEAN, 0.0), "d": (-1.0, GOLDEN_MEAN, 0.0),
        "e": (GOLDEN_MEAN, 0.0, 1.0), "f": (-GOLDEN_MEAN, 0.0, 1.0),
        "g": (-GOLDEN_MEAN, 0.0, -1.0), "h": (GOLDEN_MEAN, 0.0, -1.0),
        "i": (0.0, 1.0, GOLDEN_MEAN), "j": (0.0, 1.0, -GOLDEN_MEAN),
        "k": (0.0, -1.0, -GOLDEN_MEAN), "l": (0.0, -1.0, GOLDEN_MEAN),
    },
}

_FACES = {
    "tetra": ["acb", "abd", "adc", "dbc"],
    "octa": ["cba", "dca", "eda", "bea", "def", "ebf", "bcf", "cdf"],
    "icosa": ["iea", "iad", "idf", "ifl", "ile", "eha", "ajd", "dgf",
              "fcl", "lbe", "ebh", "ahj", "djg", "fgc", "lcb", "khb",
              "kjh", "kgj", "kcg", "kbc"],
}


def _base_triangles(name):
    points = _POINTS[name]
    out = []
    for face in _FACES[name]:
        out.append(tuple(V(*points[letter]) for letter in face))
    return out


# --- Football: the truncated icosahedron --------------------------------
#
# Built by truncating the icosahedron: every vertex becomes a pentagon
# through the 2/3 points of its five edges (12 pentagons) and every
# triangular face becomes a hexagon through the edge thirds (20
# hexagons) — 60 vertices, 90 edges, 32 faces, Euler = 2.

def _icosa_neighbours():
    """Letter → set of adjacent letters, from the icosahedron faces."""
    neighbours: dict = {}
    for face in _FACES["icosa"]:
        a, b, c = face
        for x, y in ((a, b), (b, c), (c, a)):
            neighbours.setdefault(x, set()).add(y)
            neighbours.setdefault(y, set()).add(x)
    return neighbours


def _ordered_neighbours(letter, neighbours, points):
    """The neighbours of ``letter`` in circular order around it."""
    vertex = V(*points[letter])
    axis = vertex.normalized()
    tangent = []
    for other in neighbours[letter]:
        n = V(*points[other])
        tangent.append((other, n - axis * V.dotProduct(n, axis)))
    ref = tangent[0][1].normalized()
    side = V.crossProduct(axis, ref)

    def angle(item):
        t = item[1]
        return math.atan2(V.dotProduct(t, side), V.dotProduct(t, ref))

    tangent.sort(key=angle)
    return [other for other, _t in tangent]


def _football_polygons():
    """The 12 pentagons and 20 hexagons of a truncated icosahedron, with
    every vertex projected onto the unit sphere."""
    points = _POINTS["icosa"]
    vectors = {letter: V(*points[letter]) for letter in points}
    neighbours = _icosa_neighbours()

    polygons = []
    # Pentagons: one per icosahedron vertex, through the 2/3 points of
    # its incident edges, in circular order.
    for letter in vectors:
        apex = vectors[letter]
        ring = [((apex * 2.0 + vectors[n]) * (1.0 / 3.0)).normalized()
                for n in _ordered_neighbours(letter, neighbours, points)]
        polygons.append(ring)

    # Hexagons: one per icosahedron face, through the edge thirds.
    for face in _FACES["icosa"]:
        a, b, c = (vectors[t] for t in face)
        hexagon = [
            (a * 2.0 + b) * (1.0 / 3.0), (a + b * 2.0) * (1.0 / 3.0),
            (b * 2.0 + c) * (1.0 / 3.0), (b + c * 2.0) * (1.0 / 3.0),
            (c * 2.0 + a) * (1.0 / 3.0), (c + a * 2.0) * (1.0 / 3.0),
        ]
        polygons.append([v.normalized() for v in hexagon])

    return polygons


def _expand(face, frequency, out):
    if frequency < 1:
        out.append(face)
        return
    a, b, c = face
    ab = (a + b) * 0.5
    ac = (a + c) * 0.5
    bc = (b + c) * 0.5
    for sub in ((a, ab, ac), (b, bc, ab), (c, ac, bc), (ab, bc, ac)):
        _expand(sub, frequency - 1, out)


def build(params, origin):
    primitive = params.get("base", "icosa")
    radius = max(1e-4, float(params.get("radius", 1.0)))
    frequency = max(0, min(4, int(params.get("frequency", 2))))
    smooth = params.get("finish") == "smooth"

    if primitive == "football":
        # The football is exactly the truncated icosahedron: its 12
        # pentagons and 20 hexagons are what read as the classic ball.
        # The "Frequency" field does not apply here — it subdivides the
        # triangular primitives only.
        faces = [[origin + vertex * radius for vertex in polygon]
                 for polygon in _football_polygons()]
        return faces, (), smooth

    if primitive not in _POINTS:
        primitive = "icosa"
    raw = []
    for face in _base_triangles(primitive):
        _expand(face, frequency, raw)

    faces = []
    for triangle in raw:
        loop = []
        for vertex in triangle:
            length = vertex.length()
            factor = (radius / length) if length > 0.0 else radius
            loop.append(origin + vertex * factor)
        faces.append(loop)

    return faces, (), smooth
