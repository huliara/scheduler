from abc import abstractmethod

from app.ddd.core.i_repository import IRepository
from app.models.models import Template

from .template_entity import TemplateEntity
from .template_value_object import TemplateId


class ITemplateRepository(IRepository[TemplateEntity,TemplateId]):
    
    @abstractmethod
    def _refresh_to_entity(self, model: Template) -> TemplateEntity:
        pass