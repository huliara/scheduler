from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.template import ITemplateRepository, TemplateEntity

from .schema import TemplateCreateParams


class TemplateCreateUseCase(TransactionUseCaseBase):
    
    def __init__(self, db,template_repository:ITemplateRepository):
        super().__init__(db)
        self.template_repository=template_repository
        
    def execute(self,data:TemplateCreateParams):
        
        return self._transaction(data)
    
    def _transaction(self, data:TemplateCreateParams):
        template_entity=TemplateEntity.from_params(data)
        template=self.template_repository.add(template_entity)
        return template