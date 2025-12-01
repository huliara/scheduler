from ddd.domain.shift import IShiftRepository, ShiftEntity, ShiftId

from ..remove_usecase import RemoveUseCase


class ShiftRemoveUseCase(RemoveUseCase[ShiftId,ShiftEntity,IShiftRepository]):
    pass