from abc import abstractmethod

from app.ddd.core.i_repository import IRepository
from app.models.models import Group

from .group_entity import GroupEntity
from .group_value_object import GroupId


class IGroupRepository(IRepository[GroupEntity,GroupId]):
    @abstractmethod
    def _refresh_to_entity(self,model:Group)->GroupEntity:
        pass