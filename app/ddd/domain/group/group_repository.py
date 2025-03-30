from abc import abstractmethod

from app.ddd.core.i_repository import IRepository
import app.models.models as models
from .group_entity import GroupEntity, MemberEntity
from .group_value_object import GroupId


class IGroupRepository(IRepository[GroupEntity,GroupId]):
    @abstractmethod
    def _refresh_to_entity(self,model:"models.Group")->GroupEntity:
        pass
    
    @abstractmethod
    def get_all_members(id:GroupId)->list[MemberEntity]:
        pass