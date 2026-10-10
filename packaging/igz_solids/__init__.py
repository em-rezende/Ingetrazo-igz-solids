# SPDX-License-Identifier: GPL-3.0-or-later
"""igz_solids — parametric solids for IngeTrazo.

A toolbar extension that creates parametric solids: box and wedge, capsule,
cylinder and tube, sphere / domus / spherical wedge, cone and pyramid (with
optional truncation), geodesic sphere (including a football), solid helix,
prism and torus.

Each ``tb_*`` module (listed in ``tb_list.txt``) exposes:

* ``SPEC`` — the dialog metadata (name, icon, tooltip and fields);
* ``build(params, origin)`` — the pure geometry, returning
  ``(faces, cap_indices, smooth)`` for :func:`_core.add_solid`.

The shared infrastructure — the parameter dialog, the cursor-placement
tool, the undoable mesh commit and the toolbar wiring — lives in the
private :mod:`._core` submodule.  It is kept out of this file on purpose:
IngeTrazo's loader instantiates every ``Tool`` subclass **defined here**
with no arguments, so the placement tool must be defined elsewhere.
"""
from __future__ import annotations

from ._core import setup

__all__ = ["setup"]
