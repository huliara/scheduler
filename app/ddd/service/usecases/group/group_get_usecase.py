from ddd.domain.group import GroupEntity, GroupId, IGroupRepository

from ..get_usecase import GetUseCase


class GroupGetUseCase(GetUseCase[GroupId,GroupEntity,IGroupRepository]):
    pass