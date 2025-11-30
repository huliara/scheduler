from ddd.domain.template import (ITemplateRepository, TemplateEntity,
                                     TemplateId)

from ..get_usecase import GetUseCase


class TemplateGetUseCase(GetUseCase[TemplateId,TemplateEntity,ITemplateRepository]):
    pass
    
    