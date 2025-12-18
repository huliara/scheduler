from abc import abstractmethod

import models.models as models
from ddd.core.i_repository import IRepository
from ddd.domain.user.user_value_object import UserId

from .group_entity import GroupEntity, MemberEntity
from .group_value_object import GroupId


class IGroupRepository(IRepository[GroupEntity,GroupId]):
    @abstractmethod
    def find_by_user(self, id:UserId)->list[GroupEntity]:
        pass
    @abstractmethod
    def _refresh_to_entity(self,model:"models.Group")->GroupEntity:
        pass
    @abstractmethod
    def get_all_members(id:GroupId)->list[MemberEntity]:
        pass