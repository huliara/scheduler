from app.ddd.domain.group import GroupEntity, GroupId, IGroupRepository

from ..remove_usecase import RemoveUseCase


class GroupRemoveUseCase(RemoveUseCase[GroupId,GroupEntity,IGroupRepository]):
    pass