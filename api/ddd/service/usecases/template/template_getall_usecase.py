from ddd.domain.template import ITemplateRepository, TemplateEntity

from ..getall_usecase import GetAllUseCase


class TemplateGetAllUseCase(GetAllUseCase[TemplateEntity,ITemplateRepository]):
    pass
    
    