from app.ddd.domain.shift import IShiftRepository, Shift, ShiftId

from ..get_usecase import GetUseCase


class ShiftGetUseCase(GetUseCase[ShiftId,Shift,IShiftRepository]):
    pass