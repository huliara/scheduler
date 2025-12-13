import datetime
import uuid

import pytest

from .template_entity import TemplateEntity
from .template_value_object import TemplateSlot


def test_template_from_params():
    same_detail=uuid.uuid4()
    name='name'
    group_id=uuid.uuid4()
    slots=[
        TemplateSlot(same_detail,name,0,datetime.time(hour=12) ),
        TemplateSlot(same_detail,name,0,datetime.time(hour=12))
           ]
    template_entity=TemplateEntity.from_params('name', group_id, slots)
    assert template_entity.name=='name'
    assert template_entity.group_id==group_id
    assert list(template_entity.slots)==[TemplateSlot(same_detail,name,0,datetime.time(hour=12) )]

def test_template_negative_date_from_start():
    with pytest.raises(ValueError) as e:
        TemplateSlot(uuid.uuid4(),"name",-1,datetime.time(hour=12))
        assert e.value=='date_from_start must be positive'