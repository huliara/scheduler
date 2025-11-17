from app.ddd.domain.shift import IShiftRepository, Shift, ShiftId

from ..remove_usecase import RemoveUseCase


class TaskRemoveUseCase(RemoveUseCase[ShiftId,Shift,IShiftRepository]):
    pass