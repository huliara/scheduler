from ddd.domain.shift import IShiftRepository, ShiftEntity, ShiftId

from ..get_usecase import GetUseCase


class ShiftGetUseCase(GetUseCase[ShiftId,ShiftEntity,IShiftRepository]):
    pass