import datetime
import uuid

import pytest

from app.ddd.domain.group import GroupEntity
from app.ddd.domain.task.task_entity import TaskEntity
from app.ddd.domain.task_detail.task_detail_entity import TaskDetailEntity
from app.ddd.domain.template import TemplateEntity, TemplateSlot
from app.ddd.domain.user import UserEntity
from app.ddd.infra.repository import (GroupRepository, TaskDetailRepository,
                                      TaskRepository, TemplateRepository,
                                      UserRepository)
from app.ddd.service.usecases.template.schema import TaskFromTemplateParams
from app.ddd.service.usecases.template.task_from_template import \
    TaskFromTemplateUseCase
from app.mock_database import SessionLocal


@pytest.fixture
def db():
    return SessionLocal

def test_task_from_template(db):
    creater=UserEntity(
        id=None,
        name='test',
        room_number='test',
        exp_tasks=[],
        tasks=[],
        point=0,
        is_admin=False
    )
    user_repository=UserRepository(db)
    creater=user_repository.add(creater,'test')
    group_enitity=GroupEntity(
        id=None,
        name='test',
        users=[],
        task_details=[],
        template=[]
    )
    group=GroupRepository(db).add(group_enitity)
    group_id=group.id
    
    task_detail={
            'id':None,
            'name':'test',
            'max_worker':1,
            'min_worker':1,
            'exp_worker':0,
            'duration':datetime.timedelta(hours=1),
            'group_id':group_id,
            'creater_id':creater.id,
            'permissions':[],
            'wage':0,
            'subtask':[],
            
        }
    
    task_detail_entity=TaskDetailEntity(**task_detail)
    task_detail_repository=TaskDetailRepository(db)
    task_detail_entity=task_detail_repository.add(task_detail_entity)
    slots=[
        {
            'taskdetail_id':task_detail_entity.id,
            'date_from_start':1,
            'start_time':datetime.time(22,22)
        }
    ]
    
    template_repository=TemplateRepository(db)
    
    
    
    task_repository=TaskRepository(db)
    task_detail_repository=TaskDetailRepository(db)
    template_entity=TemplateEntity(
        id=None,
        name='test',
        group_id=group_id,
        slots=[TemplateSlot(**slot) for slot in slots]
    )
    target_entity=template_repository.add(template_entity)
    print(target_entity.id)
    usecase=TaskFromTemplateUseCase(
        db=db,
        template_repository=template_repository,
        task_repository=task_repository,
        task_detail_repository=task_detail_repository
    )
    params=TaskFromTemplateParams(
        creater_id=creater.id,
        template_id=target_entity.id,
        start_date=datetime.date(2222,2,22)
    )
    tasks:list[TaskEntity]=usecase.execute(params)
    assert len(tasks)==1
    assert tasks[0].name=='22時22分からtest'
    assert tasks[0].taskdetail.id==slots[0]['taskdetail_id']
    assert tasks[0].start_time==datetime.datetime(2222,2,23,22,22)
    