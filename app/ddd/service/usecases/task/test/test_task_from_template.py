import datetime
import uuid

import pytest

from app.ddd.domain.task.task_entity import TaskEntity
from app.ddd.domain.task_detail.task_detail_entity import TaskDetailEntity
from app.ddd.domain.template import TemplateEntity, TemplateSlot
from app.ddd.infra.repository import (TaskDetailRepository, TaskRepository,
                                      TemplateRepository)
from app.mock_database import get_mock_db

from ...template.task_from_template import TaskFromTemplateUseCase


@pytest.fixture
def db():
    return get_mock_db()

def test_task_from_template(db):
    task_detail={
            'id':uuid.uuid4(),
            'name':'test',
            'max_worker':1,
            'min_worker':1,
            'exp_worker':0,
            'duration':datetime.timedelta(hours=1),
            'group_id':uuid.uuid4(),
            'permissions':[],
            'wage':0,
            'subtask':[],
        }
    
    slots=[
        {
            'taskdetail_id':task_detail[0]['id'],
            'date_from_start':1,
            'start_time':datetime.time(22,22)
        }
    ]
    task_detail_entity=TaskDetailEntity(**task_detail)
    task_detail_repository=TaskDetailRepository(db)
    task_detail_repository.add(task_detail_entity)
    
    template_repository=TemplateRepository(db)
    
    
    
    task_repository=TaskRepository(db)
    task_detail_repository=TaskDetailRepository(db)
    template_entity=TemplateEntity(
        name='test',
        group_id=1,
        slots=[TemplateSlot(**slot) for slot in slots]
    )
    target_entity=template_repository.add(template_entity)
    usecase=TaskFromTemplateUseCase(
        db=db,template_repository=template_repository,task_repository=task_repository
    )
    tasks:list[TaskEntity]=usecase.execute(template_id=target_entity.id,start_day=datetime.date(2222,2,22))
    assert len(tasks)==1
    assert tasks[0].name=='22時22分からtest'
    assert tasks[0].taskdetail.id==slots[0]['taskdetail_id']
    assert tasks[0].start_time==datetime.datetime(2222,2,23,22,22)
    