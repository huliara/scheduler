from ddd.domain.shift import IShiftRepository, ShiftEntity
from ddd.service.usecases.getall_usecase import GetAllUseCase

class ShiftGetAllUseCase(GetAllUseCase[ShiftEntity,IShiftRepository]):
    pass