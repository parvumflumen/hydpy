# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring
# pylint: enable=missing-docstring

# import...
# ...from HydPy
from hydpy.core import sequencetools

# ...from hland
from hydpy.models.hland import hland_masks
from hydpy.models.hland import hland_sequences


class TMean(sequencetools.FluxSequence):
    """Mean subbasin temperature [°C]."""

    NDIM, NUMERIC = 0, False


class TC(hland_sequences.Flux1DSequence):
    """Corrected temperature [°C]."""

    NDIM, NUMERIC = 1, False
    mask = hland_masks.Complete()


class FracRain(hland_sequences.Flux1DSequence):
    """Fraction rainfall / total precipitation [-]."""

    NDIM, NUMERIC = 1, False
    mask = hland_masks.Complete()


class RfC(hland_sequences.Flux1DSequence):
    """Actual precipitation correction related to liquid precipitation [-]."""

    NDIM, NUMERIC = 1, False
    mask = hland_masks.Complete()


class SfC(hland_sequences.Flux1DSequence):
    """Actual precipitation correction related to frozen precipitation [-]."""

    NDIM, NUMERIC = 1, False
    mask = hland_masks.Complete()


class PC(hland_sequences.Flux1DSequence):
    """Corrected precipitation [mm]."""

    NDIM, NUMERIC = 1, False
    mask = hland_masks.Complete()


class EP(hland_sequences.Flux1DSequence):
    """Potential evaporation [mm]."""

    NDIM, NUMERIC = 1, False
    mask = hland_masks.NoGlacier()


class EPC(hland_sequences.Flux1DSequence):
    """Corrected potential evaporation [mm]."""

    NDIM, NUMERIC = 1, False
    mask = hland_masks.NoGlacier()


class EI(hland_sequences.Flux1DSequence):
    """Interception evaporation [mm]."""

    NDIM, NUMERIC = 1, False
    mask = hland_masks.Interception()


class TF(hland_sequences.Flux1DSequence):
    """Throughfall [mm]."""

    NDIM, NUMERIC = 1, False
    mask = hland_masks.Interception()


class GlMelt(hland_sequences.Flux1DSequence):
    """Glacier melt [mm]."""

    NDIM, NUMERIC = 1, False
    mask = hland_masks.Glacier()


class Melt(hland_sequences.Flux1DSequence):
    """Actual melting of frozen water stored in the snow layer [mm]."""

    NDIM, NUMERIC = 1, False
    mask = hland_masks.Snow()


class Refr(hland_sequences.Flux1DSequence):
    """Actual (re)freezing of liquid water stored in the snow layer [mm]."""

    NDIM, NUMERIC = 1, False
    mask = hland_masks.Snow()


class In_(hland_sequences.Flux1DSequence):
    """Snow module release/soil module inflow [mm]."""

    NDIM, NUMERIC = 1, False
    mask = hland_masks.Snow()


class R(hland_sequences.Flux1DSequence):
    """Effective soil response [mm].

    Note that PREVAH uses the abbreviation `DSUZ` instead of the HBV96 abbreviation `R`.
    """

    NDIM, NUMERIC = 1, False
    mask = hland_masks.Soil()


class EA(hland_sequences.Flux1DSequence):
    """Actual soil evaporation [mm]."""

    NDIM, NUMERIC = 1, False
    mask = hland_masks.Soil()


class CFPot(hland_sequences.Flux1DSequence):
    """Potential capillary flow [mm]."""

    NDIM, NUMERIC = 1, False
    mask = hland_masks.Soil()


class CF(hland_sequences.Flux1DSequence):
    """Actual capillary flow [mm]."""

    NDIM, NUMERIC = 1, False
    mask = hland_masks.Soil()


class ContriArea(sequencetools.FluxSequence):
    """Fraction of the "soil area" contributing to runoff generation [-]."""

    NDIM, NUMERIC = 0, False


class InUZ(sequencetools.FluxSequence):
    """Inflow to the upper zone layer [mm]."""

    NDIM, NUMERIC = 0, False


class Perc(sequencetools.FluxSequence):
    """Percolation from the upper to the lower zone layer [mm]."""

    NDIM, NUMERIC = 0, False


class DP(sequencetools.FluxSequence):
    """Deep percolation rate [mm].

    Note that PREVAH uses the abbreviation `Perc`, which is also the abbreviation used
    by HBV96.  However, |Perc| is 0-dimensional while |DP| is 1-dimensional, which is
    why we need to define separate sequence classes with different names.
    """

    NDIM, NUMERIC = 1, False
    mask = hland_masks.UpperZone()


class Q0(sequencetools.FluxSequence):
    """Outflow from the upper zone layer [mm]."""

    NDIM, NUMERIC = 0, False


class QVs1(sequencetools.FluxSequence):
    """Percolation from the surface flow reservoir [mm].

    Note that COSERO uses the abbreviation `QVS1ZON` instead.
    """

    NDIM, NUMERIC = 1, False
    mask = hland_masks.UpperZone()


class QAb1(sequencetools.FluxSequence):
    """Surface flow [mm].

    Note that COSERO uses the abbreviation `QAB1ZON` instead.
    """

    NDIM, NUMERIC = 1, False
    mask = hland_masks.UpperZone()


class QVs2(sequencetools.FluxSequence):
    """Percolation from the interflow reservoir [mm].

    Note that COSERO uses the abbreviation `QVS2ZON` instead.
    """

    NDIM, NUMERIC = 1, False
    mask = hland_masks.UpperZone()


class QAb2(sequencetools.FluxSequence):
    """Interflow [mm].

    Note that COSERO uses the abbreviation `QAB2ZON` instead.
    """

    NDIM, NUMERIC = 1, False
    mask = hland_masks.UpperZone()


class EL(sequencetools.FluxSequence):
    """Actual lake evaporation [mm]."""

    NDIM, NUMERIC = 1, False
    mask = hland_masks.ILake()


class Q1(sequencetools.FluxSequence):
    """Outflow from the lower zone layer [mm]."""

    NDIM, NUMERIC = 0, False


class RS(sequencetools.FluxSequence):
    """Surface runoff [mm]."""

    NDIM, NUMERIC = 1, False
    mask = hland_masks.UpperZone()


class RI(sequencetools.FluxSequence):
    """Interflow [mm]."""

    NDIM, NUMERIC = 1, False
    mask = hland_masks.UpperZone()


class GR1(sequencetools.FluxSequence):
    """Recharge into the fast response groundwater reservoir [mm]."""

    NDIM, NUMERIC = 1, False
    mask = hland_masks.UpperZone()


class RG1(sequencetools.FluxSequence):
    """Discharge from the fast response groundwater reservoir [mm]."""

    NDIM, NUMERIC = 1, False
    mask = hland_masks.UpperZone()


class GR2(sequencetools.FluxSequence):
    """Recharge into the first-order slow response groundwater reservoir [mm]."""

    NDIM, NUMERIC = 0, False


class RG2(sequencetools.FluxSequence):
    """Discharge from the first-order slow response groundwater reservoir [mm]."""

    NDIM, NUMERIC = 0, False


class GR3(sequencetools.FluxSequence):
    """Recharge into the second-order slow response groundwater reservoir [mm]."""

    NDIM, NUMERIC = 0, False


class RG3(sequencetools.FluxSequence):
    """Discharge from the second-order slow response groundwater reservoir [mm]."""

    NDIM, NUMERIC = 0, False


class InUH(sequencetools.FluxSequence):
    """Input of the triangle unit hydrograph  [mm]."""

    NDIM, NUMERIC = 0, False


class OutUH(sequencetools.FluxSequence):
    """Output of the triangle unit hydrograph  [mm]."""

    NDIM, NUMERIC = 0, False


class RO(sequencetools.FluxSequence):
    """Sum of all flow components [mm]."""

    NDIM, NUMERIC = 0, False


class RA(sequencetools.FluxSequence):
    """Actual abstraction from runoff [mm]."""

    NDIM, NUMERIC = 0, False


class RT(sequencetools.FluxSequence):
    """Total model outflow [mm]."""

    NDIM, NUMERIC = 0, False


class QT(sequencetools.FluxSequence):
    """Total model outflow [m³/s]."""

    NDIM, NUMERIC = 0, False
