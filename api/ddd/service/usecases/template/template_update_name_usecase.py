from ddd.core.exception import UseCaseException
from ddd.core.transaction_usecase_base import TransactionUseCaseBase
from ddd.domain.template import ITemplateRepository, TemplateEntity


class TemplateUpdateNameUseCase(TransactionUseCaseBase):
    
    def __init__(self,template_repository:ITemplateRepository):
        self.template_repository=template_repository
        
    def execute(self,id,name)->TemplateEntity:
        
        return self._transaction(id,name)
    
    def _transaction(self, id,name)->TemplateEntity:
        try:
            template=self.template_repository.update_name(id,name)
        except:
            raise UseCaseException('Invalid Template Entity')
        return template