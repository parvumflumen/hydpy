# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
# pylint: enable=missing-docstring

from hydpy.core import sequencetools


class P(sequencetools.InputSequence):
    """Precipitation [mm]."""
    NDIM, NUMERIC = 0, False


class T(sequencetools.InputSequence):
    """Daily mean air temperature [°C]."""
    NDIM, NUMERIC = 0, False

class TMin(sequencetools.InputSequence):
    """Daily minimum air temperature [°C]."""
    NDIM, NUMERIC = 0, False

class TMax(sequencetools.InputSequence):
    """Daily maximum air temperature [°C]."""
    NDIM, NUMERIC = 0, False


class E(sequencetools.InputSequence):
    """Potential Evapotranspiration (PE) [mm]."""
    NDIM, NUMERIC = 0, False
