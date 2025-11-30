from abc import abstractmethod

from ddd.core.i_repository import IRepository
import models.models as models

from .template_entity import TemplateEntity
from .template_value_object import TemplateId


class ITemplateRepository(IRepository[TemplateEntity,TemplateId]):
    
    @abstractmethod
    def update_name(self, id:TemplateId, name:str) -> TemplateEntity:
        pass
    
    @abstractmethod
    def _refresh_to_entity(self, model: "models.Template") -> TemplateEntity:
        pass