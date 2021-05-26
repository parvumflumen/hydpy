# -*- coding: utf-8 -*-
# pylint: disable=line-too-long, wildcard-import, unused-wildcard-import
"""Version 2 of HydPy-Dam.

Application model |dam_v002| is a simplification of |dam_v001|.  While most
functionalities are identical, |dam_v002| does not calculate |RequiredRemoteRelease| on
its own but picks this information from the simulation results of another model.

The following explanations focus on this difference.  For further information on using
|dam_v002|, please read the documentation on model |dam_v001|.

Integration tests
=================

.. how_to_understand_integration_tests::

Each of the following examples repeats one example demonstrating a specific
functionality of application model |dam_v001|.  To achieve comparability, we define
identical parameter values, initial conditions, and input time series.  The sequence
|RequiredRemoteRelease| requires special care.  |dam_v001| calculates its values based
on other information but |dam_v002| expects externally calculated values for it.
Hence, we use the tabulated results of the selected |dam_v001| examples as the input
data of the node object `demand`, which passes this information to |dam_v002| during
simulation.  The limited precision of the copy-pasted |RequiredRemoteRelease| values
causes some tiny deviations between the results of both models.

The following time- and space-related setup is identical to the one of |dam_v001|,
except we do not need to add other models to construct meaningful examples:

>>> from hydpy import pub
>>> pub.timegrids = "01.01.2000", "21.01.2000",  "1d"
>>> from hydpy import Node
>>> inflow = Node("inflow")
>>> outflow = Node("outflow")
>>> demand = Node("demand", variable="D")
>>> from hydpy import Element
>>> dam = Element("dam", inlets=inflow, outlets=outflow, receivers=demand)
>>> from hydpy.models.dam_v002 import *
>>> parameterstep("1d")
>>> dam.model = model

We prepare an identical |IntegrationTest| object:

>>> from hydpy import IntegrationTest
>>> test = IntegrationTest(dam)
>>> test.dateformat = "%d.%m."
>>> test.plotting_options.axis1 = fluxes.inflow, fluxes.outflow
>>> test.plotting_options.axis2 = states.watervolume

As initial conditions, |dam_v002| requires logged values for the required remote release
instead of logged values for the total remote discharge and its outflow.  Following the
above reasoning, we copy-paste the first value of the "requiredremoterelease"
column that is identical for all drought-related calculations performed by |dam_v001|:

>>> test.inits=((states.watervolume, 0.0),
...             (logs.loggedadjustedevaporation, 0.0),
...             (logs.loggedrequiredremoterelease, 0.005))

Apart from the unnecessary "natural" discharge of the subcatchment underneath the dam,
we define identical (for now, constant) input time series:

>>> inflow.sequences.sim.series = 1.0
>>> inputs.precipitation.series = 0.0
>>> inputs.evaporation.series = 0.0

|dam_v002| implements fewer parameters than |dam_v001|.  Besides that, all parameter
settings are identical:

>>> watervolume2waterlevel(weights_input=1.0, weights_output=0.25,
...                        intercepts_hidden=0.0, intercepts_output=0.0,
...                        activation=0)
>>> waterlevel2flooddischarge(ann(weights_input=0.0, weights_output=0.0,
...                               intercepts_hidden=0.0, intercepts_output=0.0))
>>> catchmentarea(86.4)
>>> neardischargeminimumthreshold(0.2)
>>> neardischargeminimumtolerance(0.2)
>>> waterlevelminimumthreshold(0.0)
>>> waterlevelminimumtolerance(0.0)
>>> restricttargetedrelease(True)
>>> surfacearea(1.44)
>>> correctionprecipitation(1.2)
>>> correctionevaporation(1.2)
>>> weightevaporation(0.8)
>>> thresholdevaporation(0.0)
>>> toleranceevaporation(0.001)

.. _dam_v002_smooth_near_minimum:

smooth near minimum
___________________

This example repeats the :ref:`dam_v001_smooth_near_minimum` example of application
model |dam_v001|.  We use the values of |RequiredRemoteRelease| calculated by
|dam_v001|, as explained above:

>>> demand.sequences.sim.series = [
...     0.008588, 0.010053, 0.013858, 0.027322, 0.064075, 0.235523, 0.470414,
...     0.735001, 0.891263, 0.696325, 0.349797, 0.105231, 0.111928, 0.240436,
...     0.229369, 0.058622, 0.016958, 0.008447, 0.004155, 0.0]

Note that the first tabulated value (0.005 m³/s) serves as an initial condition, and we
have to assign the following nineteen values to the time series of the `demand` node.
The last value of the node's time series is of no importance.  We arbitrarily set it to
0.0 m³/s.

The test results confirm that both models behave identically under low flow conditions
for a "near" and a "remote" need for water supply:

.. integration-test::

    >>> test("dam_v002_smooth_near_minimum")
    |   date | precipitation | evaporation | adjustedprecipitation | adjustedevaporation | actualevaporation | inflow | requiredremoterelease | requiredrelease | targetedrelease | actualrelease | flooddischarge |  outflow | watervolume |   demand | inflow |  outflow |
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    | 01.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |                 0.005 |        0.210526 |        0.210526 |      0.201754 |            0.0 | 0.201754 |    0.068968 | 0.008588 |    1.0 | 0.201754 |
    | 02.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.008588 |         0.21092 |         0.21092 |       0.21092 |            0.0 |  0.21092 |    0.137145 | 0.010053 |    1.0 |  0.21092 |
    | 03.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.010053 |        0.211084 |        0.211084 |      0.211084 |            0.0 | 0.211084 |    0.205307 | 0.013858 |    1.0 | 0.211084 |
    | 04.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.013858 |        0.211523 |        0.211523 |      0.211523 |            0.0 | 0.211523 |    0.273432 | 0.027322 |    1.0 | 0.211523 |
    | 05.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.027322 |        0.213209 |        0.213209 |      0.213209 |            0.0 | 0.213209 |     0.34141 | 0.064075 |    1.0 | 0.213209 |
    | 06.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.064075 |        0.219043 |        0.219043 |      0.219043 |            0.0 | 0.219043 |    0.408885 | 0.235523 |    1.0 | 0.219043 |
    | 07.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.235523 |        0.283419 |        0.283419 |      0.283419 |            0.0 | 0.283419 |    0.470798 | 0.470414 |    1.0 | 0.283419 |
    | 08.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.470414 |        0.475211 |        0.475211 |      0.475211 |            0.0 | 0.475211 |    0.516139 | 0.735001 |    1.0 | 0.475211 |
    | 09.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.735001 |         0.73528 |         0.73528 |       0.73528 |            0.0 |  0.73528 |    0.539011 | 0.891263 |    1.0 |  0.73528 |
    | 10.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.891263 |        0.891314 |        0.891314 |      0.891314 |            0.0 | 0.891314 |    0.548402 | 0.696325 |    1.0 | 0.891314 |
    | 11.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.696325 |         0.69675 |         0.69675 |       0.69675 |            0.0 |  0.69675 |    0.574602 | 0.349797 |    1.0 |  0.69675 |
    | 12.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.349797 |        0.366407 |        0.366407 |      0.366407 |            0.0 | 0.366407 |    0.629345 | 0.105231 |    1.0 | 0.366407 |
    | 13.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.105231 |        0.228241 |        0.228241 |      0.228241 |            0.0 | 0.228241 |    0.696025 | 0.111928 |    1.0 | 0.228241 |
    | 14.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.111928 |        0.230054 |        0.230054 |      0.230054 |            0.0 | 0.230054 |    0.762548 | 0.240436 |    1.0 | 0.230054 |
    | 15.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.240436 |        0.286374 |        0.286374 |      0.286374 |            0.0 | 0.286374 |    0.824205 | 0.229369 |    1.0 | 0.286374 |
    | 16.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.229369 |        0.279807 |        0.279807 |      0.279807 |            0.0 | 0.279807 |     0.88643 | 0.058622 |    1.0 | 0.279807 |
    | 17.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.058622 |         0.21805 |         0.21805 |       0.21805 |            0.0 |  0.21805 |    0.953991 | 0.016958 |    1.0 |  0.21805 |
    | 18.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.016958 |        0.211893 |        0.211893 |      0.211893 |            0.0 | 0.211893 |    1.022083 | 0.008447 |    1.0 | 0.211893 |
    | 19.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.008447 |        0.210904 |        0.210904 |      0.210904 |            0.0 | 0.210904 |    1.090261 | 0.004155 |    1.0 | 0.210904 |
    | 20.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.004155 |        0.210435 |        0.210435 |      0.210435 |            0.0 | 0.210435 |    1.158479 |      0.0 |    1.0 | 0.210435 |

.. _dam_v002_restriction_enabled:

restriction enabled
___________________

This example repeats the :ref:`dam_v001_restriction_enabled` example of application
model |dam_v001|.  We update the time series of the inflow and the required remote
release accordingly:

>>> inflow.sequences.sim.series[10:] = 0.1
>>> demand.sequences.sim.series = [
...     0.008746, 0.010632, 0.015099, 0.03006, 0.068641, 0.242578, 0.474285,
...     0.784512, 0.95036, 0.35, 0.034564, 0.299482, 0.585979, 0.557422,
...     0.229369, 0.142578, 0.068641, 0.029844, 0.012348, 0.0]
>>> neardischargeminimumtolerance(0.0)

The recalculation confirms that the restriction on releasing water when there is little
inflow works as explained for model |dam_v001|:

.. integration-test::

    >>> test("dam_v002_restriction_enabled")
    |   date | precipitation | evaporation | adjustedprecipitation | adjustedevaporation | actualevaporation | inflow | requiredremoterelease | requiredrelease | targetedrelease | actualrelease | flooddischarge |  outflow | watervolume |   demand | inflow |  outflow |
    ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    | 01.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |                 0.005 |             0.2 |             0.2 |      0.191667 |            0.0 | 0.191667 |     0.06984 | 0.008746 |    1.0 | 0.191667 |
    | 02.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.008746 |             0.2 |             0.2 |           0.2 |            0.0 |      0.2 |     0.13896 | 0.010632 |    1.0 |      0.2 |
    | 03.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.010632 |             0.2 |             0.2 |           0.2 |            0.0 |      0.2 |     0.20808 | 0.015099 |    1.0 |      0.2 |
    | 04.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.015099 |             0.2 |             0.2 |           0.2 |            0.0 |      0.2 |      0.2772 |  0.03006 |    1.0 |      0.2 |
    | 05.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |               0.03006 |             0.2 |             0.2 |           0.2 |            0.0 |      0.2 |     0.34632 | 0.068641 |    1.0 |      0.2 |
    | 06.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.068641 |             0.2 |             0.2 |           0.2 |            0.0 |      0.2 |     0.41544 | 0.242578 |    1.0 |      0.2 |
    | 07.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.242578 |        0.242578 |        0.242578 |      0.242578 |            0.0 | 0.242578 |    0.480881 | 0.474285 |    1.0 | 0.242578 |
    | 08.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.474285 |        0.474285 |        0.474285 |      0.474285 |            0.0 | 0.474285 |    0.526303 | 0.784512 |    1.0 | 0.474285 |
    | 09.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |              0.784512 |        0.784512 |        0.784512 |      0.784512 |            0.0 | 0.784512 |    0.544921 |  0.95036 |    1.0 | 0.784512 |
    | 10.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |               0.95036 |         0.95036 |         0.95036 |       0.95036 |            0.0 |  0.95036 |     0.54921 |     0.35 |    1.0 |  0.95036 |
    | 11.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.1 |                  0.35 |            0.35 |             0.1 |           0.1 |            0.0 |      0.1 |     0.54921 | 0.034564 |    0.1 |      0.1 |
    | 12.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.1 |              0.034564 |             0.2 |             0.1 |           0.1 |            0.0 |      0.1 |     0.54921 | 0.299482 |    0.1 |      0.1 |
    | 13.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.1 |              0.299482 |        0.299482 |             0.1 |           0.1 |            0.0 |      0.1 |     0.54921 | 0.585979 |    0.1 |      0.1 |
    | 14.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.1 |              0.585979 |        0.585979 |             0.1 |           0.1 |            0.0 |      0.1 |     0.54921 | 0.557422 |    0.1 |      0.1 |
    | 15.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.1 |              0.557422 |        0.557422 |             0.1 |           0.1 |            0.0 |      0.1 |     0.54921 | 0.229369 |    0.1 |      0.1 |
    | 16.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.1 |              0.229369 |        0.229369 |             0.1 |           0.1 |            0.0 |      0.1 |     0.54921 | 0.142578 |    0.1 |      0.1 |
    | 17.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.1 |              0.142578 |             0.2 |             0.1 |           0.1 |            0.0 |      0.1 |     0.54921 | 0.068641 |    0.1 |      0.1 |
    | 18.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.1 |              0.068641 |             0.2 |             0.1 |           0.1 |            0.0 |      0.1 |     0.54921 | 0.029844 |    0.1 |      0.1 |
    | 19.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.1 |              0.029844 |             0.2 |             0.1 |           0.1 |            0.0 |      0.1 |     0.54921 | 0.012348 |    0.1 |      0.1 |
    | 20.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.1 |              0.012348 |             0.2 |             0.1 |           0.1 |            0.0 |      0.1 |     0.54921 |      0.0 |    0.1 |      0.1 |

.. _dam_v002_smooth_stage_minimum:

smooth stage minimum
____________________

This example repeats the :ref:`dam_v001_smooth_stage_minimum` example of application
model |dam_v001|.  We update parameters |NearDischargeMinimumThreshold|,
|WaterLevelMinimumThreshold|, and |WaterLevelMinimumTolerance|, as well as the time
series of the inflow and the required remote release, accordingly:

>>> inflow.sequences.sim.series = numpy.linspace(0.2, 0.0, 20)
>>> neardischargeminimumthreshold(0.0)
>>> waterlevelminimumthreshold(0.005)
>>> waterlevelminimumtolerance(0.01)
>>> demand.sequences.sim.series = [
...     0.01232, 0.029323, 0.064084, 0.120198, 0.247367, 0.45567, 0.608464,
...     0.537314, 0.629775, 0.744091, 0.82219, 0.841916, 0.701812, 0.533258,
...     0.351863, 0.185207, 0.107697, 0.055458, 0.025948, 0.0]

|dam_v002| deals with limited water available as already known from |dam_v001|:

.. integration-test::

    >>> test("dam_v002_smooth_stage_minimum")
    |   date | precipitation | evaporation | adjustedprecipitation | adjustedevaporation | actualevaporation |   inflow | requiredremoterelease | requiredrelease | targetedrelease | actualrelease | flooddischarge |  outflow | watervolume |   demand |   inflow |  outflow |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    | 01.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |      0.2 |                 0.005 |           0.005 |           0.005 |      0.001282 |            0.0 | 0.001282 |    0.017169 |  0.01232 |      0.2 | 0.001282 |
    | 02.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 | 0.189474 |               0.01232 |         0.01232 |         0.01232 |      0.007624 |            0.0 | 0.007624 |    0.032881 | 0.029323 | 0.189474 | 0.007624 |
    | 03.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 | 0.178947 |              0.029323 |        0.029323 |        0.029323 |      0.025921 |            0.0 | 0.025921 |    0.046103 | 0.064084 | 0.178947 | 0.025921 |
    | 04.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 | 0.168421 |              0.064084 |        0.064084 |        0.064084 |      0.062021 |            0.0 | 0.062021 |    0.055296 | 0.120198 | 0.168421 | 0.062021 |
    | 05.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 | 0.157895 |              0.120198 |        0.120198 |        0.120198 |      0.118479 |            0.0 | 0.118479 |    0.058701 | 0.247367 | 0.157895 | 0.118479 |
    | 06.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 | 0.147368 |              0.247367 |        0.247367 |        0.247367 |      0.242243 |            0.0 | 0.242243 |    0.050504 |  0.45567 | 0.147368 | 0.242243 |
    | 07.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 | 0.136842 |               0.45567 |         0.45567 |         0.45567 |      0.397328 |            0.0 | 0.397328 |    0.027998 | 0.608464 | 0.136842 | 0.397328 |
    | 08.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 | 0.126316 |              0.608464 |        0.608464 |        0.608464 |      0.290762 |            0.0 | 0.290762 |     0.01379 | 0.537314 | 0.126316 | 0.290762 |
    | 09.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 | 0.115789 |              0.537314 |        0.537314 |        0.537314 |      0.154283 |            0.0 | 0.154283 |    0.010464 | 0.629775 | 0.115789 | 0.154283 |
    | 10.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 | 0.105263 |              0.629775 |        0.629775 |        0.629775 |      0.138519 |            0.0 | 0.138519 |    0.007591 | 0.744091 | 0.105263 | 0.138519 |
    | 11.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 | 0.094737 |              0.744091 |        0.744091 |        0.744091 |      0.126207 |            0.0 | 0.126207 |    0.004871 |  0.82219 | 0.094737 | 0.126207 |
    | 12.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 | 0.084211 |               0.82219 |         0.82219 |         0.82219 |      0.109723 |            0.0 | 0.109723 |    0.002667 | 0.841916 | 0.084211 | 0.109723 |
    | 13.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 | 0.073684 |              0.841916 |        0.841916 |        0.841916 |      0.092645 |            0.0 | 0.092645 |    0.001029 | 0.701812 | 0.073684 | 0.092645 |
    | 14.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 | 0.063158 |              0.701812 |        0.701812 |        0.701812 |      0.068806 |            0.0 | 0.068806 |    0.000541 | 0.533258 | 0.063158 | 0.068806 |
    | 15.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 | 0.052632 |              0.533258 |        0.533258 |        0.533258 |      0.051779 |            0.0 | 0.051779 |    0.000615 | 0.351863 | 0.052632 | 0.051779 |
    | 16.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 | 0.042105 |              0.351863 |        0.351863 |        0.351863 |      0.035499 |            0.0 | 0.035499 |    0.001185 | 0.185207 | 0.042105 | 0.035499 |
    | 17.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 | 0.031579 |              0.185207 |        0.185207 |        0.185207 |       0.02024 |            0.0 |  0.02024 |    0.002165 | 0.107697 | 0.031579 |  0.02024 |
    | 18.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 | 0.021053 |              0.107697 |        0.107697 |        0.107697 |      0.012785 |            0.0 | 0.012785 |    0.002879 | 0.055458 | 0.021053 | 0.012785 |
    | 19.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 | 0.010526 |              0.055458 |        0.055458 |        0.055458 |      0.006918 |            0.0 | 0.006918 |    0.003191 | 0.025948 | 0.010526 | 0.006918 |
    | 20.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |      0.0 |              0.025948 |        0.025948 |        0.012974 |      0.001631 |            0.0 | 0.001631 |     0.00305 |      0.0 |      0.0 | 0.001631 |

.. _dam_v002_evaporation:

evaporation
___________

This example repeats the :ref:`dam_v001_evaporation` example of application model
|dam_v001|.  We update the time series of potential evaporation and the required remote
release accordingly:

>>> inputs.evaporation.series = 10 * [1.0] + 10 * [5.0]
>>> demand.sequences.sim.series = [
...     0.012321, 0.029352, 0.064305, 0.120897, 0.248435, 0.453671, 0.585089,
...     0.550583, 0.694398, 0.784979, 0.81852, 0.840207, 0.72592, 0.575373,
...     0.386003, 0.198088, 0.113577, 0.05798, 0.026921, 0.0]

|dam_v002| uses the given evaporation values as discussed for |dam_v001|:

.. integration-test::

    >>> test("dam_v002_evaporation")
    |   date | precipitation | evaporation | adjustedprecipitation | adjustedevaporation | actualevaporation |   inflow | requiredremoterelease | requiredrelease | targetedrelease | actualrelease | flooddischarge |  outflow | watervolume |   demand |   inflow |  outflow |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    | 01.01. |           0.0 |         1.0 |                   0.0 |               0.016 |             0.012 |      0.2 |                 0.005 |           0.005 |           0.005 |      0.001234 |            0.0 | 0.001234 |    0.016137 | 0.012321 |      0.2 | 0.001234 |
    | 02.01. |           0.0 |         1.0 |                   0.0 |              0.0192 |            0.0192 | 0.189474 |              0.012321 |        0.012321 |        0.012321 |       0.00714 |            0.0 |  0.00714 |    0.030231 | 0.029352 | 0.189474 |  0.00714 |
    | 03.01. |           0.0 |         1.0 |                   0.0 |             0.01984 |           0.01984 | 0.178947 |              0.029352 |        0.029352 |        0.029352 |      0.024809 |            0.0 | 0.024809 |    0.041835 | 0.064305 | 0.178947 | 0.024809 |
    | 04.01. |           0.0 |         1.0 |                   0.0 |            0.019968 |          0.019968 | 0.168421 |              0.064305 |        0.064305 |        0.064305 |      0.060838 |            0.0 | 0.060838 |    0.049405 | 0.120897 | 0.168421 | 0.060838 |
    | 05.01. |           0.0 |         1.0 |                   0.0 |            0.019994 |          0.019994 | 0.157895 |              0.120897 |        0.120897 |        0.120897 |      0.117273 |            0.0 | 0.117273 |    0.051187 | 0.248435 | 0.157895 | 0.117273 |
    | 06.01. |           0.0 |         1.0 |                   0.0 |            0.019999 |          0.019999 | 0.147368 |              0.248435 |        0.248435 |        0.248435 |      0.235187 |            0.0 | 0.235187 |    0.041871 | 0.453671 | 0.147368 | 0.235187 |
    | 07.01. |           0.0 |         1.0 |                   0.0 |                0.02 |              0.02 | 0.136842 |              0.453671 |        0.453671 |        0.453671 |      0.343976 |            0.0 | 0.343976 |    0.022247 | 0.585089 | 0.136842 | 0.343976 |
    | 08.01. |           0.0 |         1.0 |                   0.0 |                0.02 |              0.02 | 0.126316 |              0.585089 |        0.585089 |        0.585089 |      0.225783 |            0.0 | 0.225783 |    0.011925 | 0.550583 | 0.126316 | 0.225783 |
    | 09.01. |           0.0 |         1.0 |                   0.0 |                0.02 |              0.02 | 0.115789 |              0.550583 |        0.550583 |        0.550583 |      0.134548 |            0.0 | 0.134548 |    0.008576 | 0.694398 | 0.115789 | 0.134548 |
    | 10.01. |           0.0 |         1.0 |                   0.0 |                0.02 |          0.019988 | 0.105263 |              0.694398 |        0.694398 |        0.694398 |      0.124783 |            0.0 | 0.124783 |    0.005163 | 0.784979 | 0.105263 | 0.124783 |
    | 11.01. |           0.0 |         5.0 |                   0.0 |               0.084 |          0.063974 | 0.094737 |              0.784979 |        0.784979 |        0.784979 |       0.08761 |            0.0 |  0.08761 |    0.000251 |  0.81852 | 0.094737 |  0.08761 |
    | 12.01. |           0.0 |         5.0 |                   0.0 |              0.0968 |          0.032045 | 0.084211 |               0.81852 |         0.81852 |         0.81852 |      0.069957 |            0.0 | 0.069957 |   -0.001286 | 0.840207 | 0.084211 | 0.069957 |
    | 13.01. |           0.0 |         5.0 |                   0.0 |             0.09936 |          0.012511 | 0.073684 |              0.840207 |        0.840207 |        0.840207 |      0.063591 |            0.0 | 0.063591 |   -0.001495 |  0.72592 | 0.073684 | 0.063591 |
    | 14.01. |           0.0 |         5.0 |                   0.0 |            0.099872 |          0.011118 | 0.063158 |               0.72592 |         0.72592 |         0.72592 |      0.054477 |            0.0 | 0.054477 |   -0.001705 | 0.575373 | 0.063158 | 0.054477 |
    | 15.01. |           0.0 |         5.0 |                   0.0 |            0.099974 |          0.010651 | 0.052632 |              0.575373 |        0.575373 |        0.575373 |      0.043191 |            0.0 | 0.043191 |    -0.00181 | 0.386003 | 0.052632 | 0.043191 |
    | 16.01. |           0.0 |         5.0 |                   0.0 |            0.099995 |          0.012092 | 0.042105 |              0.386003 |        0.386003 |        0.386003 |      0.029384 |            0.0 | 0.029384 |   -0.001756 | 0.198088 | 0.042105 | 0.029384 |
    | 17.01. |           0.0 |         5.0 |                   0.0 |            0.099999 |          0.014695 | 0.031579 |              0.198088 |        0.198088 |        0.198088 |      0.015375 |            0.0 | 0.015375 |   -0.001625 | 0.113577 | 0.031579 | 0.015375 |
    | 18.01. |           0.0 |         5.0 |                   0.0 |                 0.1 |          0.012793 | 0.021053 |              0.113577 |        0.113577 |        0.113577 |      0.008699 |            0.0 | 0.008699 |   -0.001663 |  0.05798 | 0.021053 | 0.008699 |
    | 19.01. |           0.0 |         5.0 |                   0.0 |                 0.1 |          0.009947 | 0.010526 |               0.05798 |         0.05798 |         0.05798 |       0.00431 |            0.0 |  0.00431 |   -0.001985 | 0.026921 | 0.010526 |  0.00431 |
    | 20.01. |           0.0 |         5.0 |                   0.0 |                 0.1 |          0.006415 |      0.0 |              0.026921 |        0.026921 |        0.013461 |      0.000952 |            0.0 | 0.000952 |   -0.002622 |      0.0 |      0.0 | 0.000952 |

>>> inputs.evaporation.series = 0.0

.. _dam_v002_flood_retention:

flood retention
_______________

This example repeats the :ref:`dam_v001_flood_retention` example of application model
|dam_v001|.  We use the same parameter and input time series configuration:

>>> neardischargeminimumthreshold(0.0)
>>> neardischargeminimumtolerance(0.0)
>>> waterlevelminimumthreshold(0.0)
>>> waterlevelminimumtolerance(0.0)
>>> waterlevel2flooddischarge(ann(weights_input=1.0, weights_output=2.5,
...                               intercepts_hidden=0.0, intercepts_output=0.0,
...                               activation=0))
>>> neardischargeminimumthreshold(0.0)
>>> inputs.precipitation.series = [0.0, 50.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
...                                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
>>> inflow.sequences.sim.series = [0.0, 0.0, 5.0, 9.0, 8.0, 5.0, 3.0, 2.0, 1.0, 0.0,
...                                0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
>>> demand.sequences.sim.series = 0.0
>>> test.inits.loggedrequiredremoterelease = 0.0

The recalculation results confirm the equality of both models for high flow conditions:

.. integration-test::

    >>> test("dam_v002_flood_retention")
    |   date | precipitation | evaporation | adjustedprecipitation | adjustedevaporation | actualevaporation | inflow | requiredremoterelease | requiredrelease | targetedrelease | actualrelease | flooddischarge |  outflow | watervolume | demand | inflow |  outflow |
    ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    | 01.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.0 |                   0.0 |             0.0 |             0.0 |           0.0 |            0.0 |      0.0 |         0.0 |    0.0 |    0.0 |      0.0 |
    | 02.01. |          50.0 |         0.0 |                   1.0 |                 0.0 |               0.0 |    0.0 |                   0.0 |             0.0 |             0.0 |           0.0 |       0.026514 | 0.026514 |    0.084109 |    0.0 |    0.0 | 0.026514 |
    | 03.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    5.0 |                   0.0 |             0.0 |             0.0 |           0.0 |       0.183744 | 0.183744 |    0.500234 |    0.0 |    5.0 | 0.183744 |
    | 04.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    9.0 |                   0.0 |             0.0 |             0.0 |           0.0 |       0.542983 | 0.542983 |     1.23092 |    0.0 |    9.0 | 0.542983 |
    | 05.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    8.0 |                   0.0 |             0.0 |             0.0 |           0.0 |       0.961039 | 0.961039 |    1.839086 |    0.0 |    8.0 | 0.961039 |
    | 06.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    5.0 |                   0.0 |             0.0 |             0.0 |           0.0 |       1.251523 | 1.251523 |    2.162955 |    0.0 |    5.0 | 1.251523 |
    | 07.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    3.0 |                   0.0 |             0.0 |             0.0 |           0.0 |       1.395546 | 1.395546 |    2.301579 |    0.0 |    3.0 | 1.395546 |
    | 08.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    2.0 |                   0.0 |             0.0 |             0.0 |           0.0 |       1.453375 | 1.453375 |    2.348808 |    0.0 |    2.0 | 1.453375 |
    | 09.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    1.0 |                   0.0 |             0.0 |             0.0 |           0.0 |       1.455596 | 1.455596 |    2.309444 |    0.0 |    1.0 | 1.455596 |
    | 10.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.0 |                   0.0 |             0.0 |             0.0 |           0.0 |       1.405132 | 1.405132 |    2.188041 |    0.0 |    0.0 | 1.405132 |
    | 11.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.0 |                   0.0 |             0.0 |             0.0 |           0.0 |       1.331267 | 1.331267 |    2.073019 |    0.0 |    0.0 | 1.331267 |
    | 12.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.0 |                   0.0 |             0.0 |             0.0 |           0.0 |       1.261285 | 1.261285 |    1.964044 |    0.0 |    0.0 | 1.261285 |
    | 13.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.0 |                   0.0 |             0.0 |             0.0 |           0.0 |       1.194981 | 1.194981 |    1.860798 |    0.0 |    0.0 | 1.194981 |
    | 14.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.0 |                   0.0 |             0.0 |             0.0 |           0.0 |       1.132163 | 1.132163 |    1.762979 |    0.0 |    0.0 | 1.132163 |
    | 15.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.0 |                   0.0 |             0.0 |             0.0 |           0.0 |       1.072647 | 1.072647 |    1.670302 |    0.0 |    0.0 | 1.072647 |
    | 16.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.0 |                   0.0 |             0.0 |             0.0 |           0.0 |        1.01626 |  1.01626 |    1.582498 |    0.0 |    0.0 |  1.01626 |
    | 17.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.0 |                   0.0 |             0.0 |             0.0 |           0.0 |       0.962837 | 0.962837 |    1.499308 |    0.0 |    0.0 | 0.962837 |
    | 18.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.0 |                   0.0 |             0.0 |             0.0 |           0.0 |       0.912222 | 0.912222 |    1.420492 |    0.0 |    0.0 | 0.912222 |
    | 19.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.0 |                   0.0 |             0.0 |             0.0 |           0.0 |       0.864268 | 0.864268 |     1.34582 |    0.0 |    0.0 | 0.864268 |
    | 20.01. |           0.0 |         0.0 |                   0.0 |                 0.0 |               0.0 |    0.0 |                   0.0 |             0.0 |             0.0 |           0.0 |       0.818835 | 0.818835 |    1.275072 |    0.0 |    0.0 | 0.818835 |
"""

# import...
# ...from HydPy
from hydpy.exe.modelimports import *
from hydpy.core import modeltools
from hydpy.auxs.anntools import ann  # pylint: disable=unused-import

# ...from dam
from hydpy.models.dam import dam_model
from hydpy.models.dam import dam_solver


class Model(modeltools.ELSModel):
    """Version 2 of HydPy-Dam."""

    SOLVERPARAMETERS = (
        dam_solver.AbsErrorMax,
        dam_solver.RelErrorMax,
        dam_solver.RelDTMin,
        dam_solver.RelDTMax,
    )
    SOLVERSEQUENCES = ()
    INLET_METHODS = (
        dam_model.Calc_AdjustedEvaporation_V1,
        dam_model.Pic_Inflow_V1,
        dam_model.Calc_RequiredRemoteRelease_V2,
        dam_model.Calc_RequiredRelease_V1,
        dam_model.Calc_TargetedRelease_V1,
    )
    RECEIVER_METHODS = (dam_model.Pic_LoggedRequiredRemoteRelease_V1,)
    ADD_METHODS = ()
    PART_ODE_METHODS = (
        dam_model.Calc_AdjustedPrecipitation_V1,
        dam_model.Pic_Inflow_V1,
        dam_model.Calc_WaterLevel_V1,
        dam_model.Calc_ActualEvaporation_V1,
        dam_model.Calc_ActualRelease_V1,
        dam_model.Calc_FloodDischarge_V1,
        dam_model.Calc_Outflow_V1,
    )
    FULL_ODE_METHODS = (dam_model.Update_WaterVolume_V1,)
    OUTLET_METHODS = (dam_model.Pass_Outflow_V1,)
    SENDER_METHODS = ()
    SUBMODELS = ()


tester = Tester()
cythonizer = Cythonizer()
cythonizer.finalise()
