from ddd.domain.template import (ITemplateRepository, TemplateEntity,
                                     TemplateId)

from ..remove_usecase import RemoveUseCase


class TemplateRemoveUseCase(RemoveUseCase[TemplateId,TemplateEntity,ITemplateRepository]):
    pass