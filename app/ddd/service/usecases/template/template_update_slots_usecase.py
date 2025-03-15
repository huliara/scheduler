from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.template import ITemplateRepository, TemplateEntity


class TemplateUpdateSlotsUseCase(TransactionUseCaseBase):
    
    def __init__(self, db,template_repository:ITemplateRepository):
        super().__init__(db)
        self.template_repository=template_repository
        
    def execute(self,tempalte:TemplateEntity)->TemplateEntity:
        return self._transaction(tempalte)
    def _transaction(self, template:TemplateEntity)->TemplateEntity:
        try:
            new_template=self.template_repository.update(template)
        except:
            raise UseCaseException('Invalid Template Entity')
        return new_template