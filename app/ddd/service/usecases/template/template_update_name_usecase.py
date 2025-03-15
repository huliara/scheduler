from app.ddd.core.exception import UseCaseException
from app.ddd.core.transaction_usecase_base import TransactionUseCaseBase
from app.ddd.domain.template import ITemplateRepository, TemplateEntity


class TemplateUpdateNameUseCase(TransactionUseCaseBase):
    
    def __init__(self, db,template_repository:ITemplateRepository):
        super().__init__(db)
        self.template_repository=template_repository
        
    def execute(self,id,name)->TemplateEntity:
        
        return self._transaction(id,name)
    
    def _transaction(self, id,name)->TemplateEntity:
        try:
            template=self.template_repository.update_name(id,name)
        except:
            raise UseCaseException('Invalid Template Entity')
        return template