"""This module defines submodel interfaces for sharing (model) states."""
# import...
# ...from hydpy
from hydpy.core import modeltools
from hydpy.core.typingtools import *


class IntercModel_V1(modeltools.SubmodelInterface):
    """Pure getter interface for using main models as sub-submodels or simple dummy
    models as submodels for querying the amount of intercepted water."""

    typeid: ClassVar[Literal[1]] = 1

    @modeltools.abstractmodelmethod
    def get_interceptedwater(self, k: int) -> float:
        """Get the selected zone's amount of intercepted water in mm."""


class SoilWaterModel_V1(modeltools.SubmodelInterface):
    """Pure getter interface for using main models as sub-submodels or simple dummy
    models as submodels for querying the soil water content."""

    typeid: ClassVar[Literal[1]] = 1

    @modeltools.abstractmodelmethod
    def get_soilwater(self, k: int) -> float:
        """Get the selected zone's soil water content in mm."""


class SnowCoverModel_V1(modeltools.SubmodelInterface):
    """Pure getter interface for using main models as sub-submodels or simple dummy
    models as submodels for querying the snow cover degree."""

    typeid: ClassVar[Literal[1]] = 1

    @modeltools.abstractmodelmethod
    def get_snowcover(self, k: int) -> float:
        """Get the selected zone's snow cover degree as a fraction."""


class SnowyCanopyModel_V1(modeltools.SubmodelInterface):
    """Pure getter interface for using main models as sub-submodels or simple dummy
    models as submodels for querying the snow cover degree in the canopies of tree-like
    vegetation."""

    typeid: ClassVar[Literal[1]] = 1

    @modeltools.abstractmodelmethod
    def get_snowycanopy(self, k: int) -> float:
        """Get the selected zone's snow cover degree in the canopies of tree-like
        vegetation (or |numpy.nan| if the zone's vegetation is not tree-like)."""


class SnowAlbedoModel_V1(modeltools.SubmodelInterface):
    """Pure getter interface for using main models as sub-submodels or simple dummy
    models as submodels for querying the current snow albedo."""

    typeid: ClassVar[Literal[1]] = 1

    @modeltools.abstractmodelmethod
    def get_snowalbedo(self, k: int) -> float:
        """Get the selected zone's snow albedo as a fraction.

        For snow-free zones, |SnowAlbedoModel_V1.get_snowalbedo| should return
        |numpy.nan|.
        """