import datetime

import pytest
from ddd.domain.group import GroupEntity
from ddd.domain.task.task_entity import TaskEntity
from ddd.domain.user import UserEntity
from ddd.infra.repository import (GroupRepository, 
                                  TaskRepository, 
                                  UserRepository)
from mock_database import SessionLocal

@pytest.fixture
def db():
    return SessionLocal

def test_find_all_tasks(db):
    creater=UserEntity(
        id=None,
        name='test',
        room_number='test',
        exp_tasks=[],
        shifts=[],
        point=0,
        is_admin=False
    )
    user_repository=UserRepository(db)
    creater=user_repository.add(creater,'test')
    group_enitity=GroupEntity(
        id=None,
        name='test',
        members=[],
        tasks=[],
        template=[]
    )
    group_repository=GroupRepository(db)
    _=group_repository.add(group_enitity)
    group=group_repository.find_all()[0]
    group_id=group.id
    print(f'Created group with ID: {group_id}')
    
    task={
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
    
    task_entity=TaskEntity(**task)
    task_repository=TaskRepository(db)
    task=task_repository.add(task_entity)
    
    tasks=task_repository.find_by_group(group_id)
    assert tasks[0].id is not None
    assert len(tasks)==1
    assert tasks[0].name=='test'