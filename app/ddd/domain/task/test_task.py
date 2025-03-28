import datetime
import uuid
from http import HTTPStatus as status

import pytest
from .task_entity import TaskEntity
from .task_state import TaskState

from app.ddd.core.exception import DomainException
from app.ddd.domain.task_detail.task_detail_entity import TaskDetailEntity
from app.ddd.domain.user.user_entity import UserEntity
from app.models.models import Task, TaskDetail, User


def test_task_add_user():
    user=UserEntity(
        id=uuid.uuid4(),
        name='test',
        tasks=[],
        exp_tasks=[],
        point=0
    )
    task_detail=TaskDetailEntity(
        name='test_detail',
        id=uuid.uuid4(),
        max_worker=1,
        min_worker=1,
        exp_worker=0,
        duration=datetime.timedelta(hours=1),
        group_id=uuid.uuid4()
    )
    task=TaskEntity(
        id=uuid.uuid4(),
        name='test',
        start_time=datetime.datetime.now()+datetime.timedelta(hours=1),
        status=TaskState.hiring,
        taskdetail=task_detail,
        
    )
    task.add(user)
    assert task.workers==[user.id]

def test_task_add_exp_user():
    task_detail=TaskDetailEntity(
        id=uuid.uuid4(),
        name='test_detail',
        max_worker=1,
        min_worker=1,
        exp_worker=1,
        duration=datetime.timedelta(hours=1),
        group_id=uuid.uuid4()
    )
    user=UserEntity(
        id=uuid.uuid4(),
        name='test',
        tasks=[],
        exp_tasks=[task_detail.id],
        point=0
    )
    task=TaskEntity(
        id=uuid.uuid4(),
        name='test',
        start_time=datetime.datetime.now()+datetime.timedelta(hours=1),
        status=TaskState.hiring,
        taskdetail=task_detail,
    )
    task.add(user)
    assert task.workers==[user.id]
    
def test_task_add_beginner_with_expert():
    task_detail=TaskDetailEntity(
        id=uuid.uuid4(),
        name='test_detail',
        max_worker=2,
        min_worker=1,
        exp_worker=1,
        duration=datetime.timedelta(hours=1),
        group_id=uuid.uuid4()
    )
    user=UserEntity(
        id=uuid.uuid4(),
        name='test',
        tasks=[],
        exp_tasks=[],
        point=0
    )
    expert=UserEntity(
        id=uuid.uuid4(),
        name='test',
        tasks=[],
        exp_tasks=[task_detail.id],
        point=0
    )
    task=TaskEntity(
        id=uuid.uuid4(),
        name='test',
        start_time=datetime.datetime.now()+datetime.timedelta(hours=1),
        status=TaskState.hiring,
        taskdetail=task_detail,
        workers=[expert.id]
    )
    task.add(user)
    assert task.workers==[user.id]

def test_task_add_nonexpert():
    user=UserEntity(
        id=uuid.uuid4(),
        name='test',
        tasks=[],
        exp_tasks=[],
        point=0
    )
    task_detail=TaskDetailEntity(
        id=uuid.uuid4(),
        name='test_detail',
        max_worker=1,
        min_worker=1,
        exp_worker=1,
        duration=datetime.timedelta(hours=1),
        group_id=uuid.uuid4()
    )
    task=TaskEntity(
        id=uuid.uuid4(),
        name='test',
        start_time=datetime.datetime.now()+datetime.timedelta(hours=1),
        status=TaskState.hiring,
        taskdetail=task_detail,
        
    )
    with pytest.raises(DomainException) as e:
        task.add(user)
        assert e.value.status_code==status.CONFLICT
    
def test_task_add_user_over_max():
    user=UserEntity(
        id=uuid.uuid4(),
        name='test',
        tasks=[],
        exp_tasks=[],
        point=0
    )
    task_detail=TaskDetailEntity(
        id=uuid.uuid4(),
        name='test_detail',
        max_worker=1,
        min_worker=1,
        exp_worker=0,
        duration=datetime.timedelta(hours=1),
        group_id=uuid.uuid4()
    )
    task=TaskEntity(
        id=uuid.uuid4(),
        name='test',
        start_time=datetime.datetime.now()+datetime.timedelta(hours=1),
        status=TaskState.hiring,
        taskdetail=task_detail,
        workers=[uuid.uuid4()]
    )
    with pytest.raises(DomainException) as e:
        task.add(user)
        assert e.value.status_code==status.CONFLICT

def test_task_add_only_beginner():
    user=UserEntity(
        id=uuid.uuid4(),
        name='test',
        tasks=[],
        exp_tasks=[],
        point=0
    )
    task_detail=TaskDetailEntity(
        id=uuid.uuid4(),
        name='test_detail',
        max_worker=2,
        min_worker=1,
        exp_worker=1,
        duration=datetime.timedelta(hours=1),
        group_id=uuid.uuid4()
    )
    task=TaskEntity(
        id=uuid.uuid4(),
        name='test',
        start_time=datetime.datetime.now()+datetime.timedelta(hours=1),
        status=TaskState.hiring,
        taskdetail=task_detail,
        workers=[user.id]
    )
    with pytest.raises(DomainException) as e:
        task.add(user)
        assert e.value.status_code==status.CONFLICT

def test_task_add_user_after_end():
    user=UserEntity(
        id=uuid.uuid4(),
        name='test',
        tasks=[],
        exp_tasks=[],
        point=0
    )
    task_detail=TaskDetailEntity(
        id=uuid.uuid4(),
        name='test_detail',
        max_worker=1,
        min_worker=1,
        exp_worker=0,
        duration=datetime.timedelta(hours=1),
        group_id=uuid.uuid4()
    )
    task=TaskEntity(
        id=uuid.uuid4(),
        name='test',
        start_time=datetime.datetime.now()-datetime.timedelta(hours=2),
        status=TaskState.decide_assignees,
        taskdetail=task_detail,
        workers=[]
    )
    with pytest.raises(DomainException) as e:
        task.add(user)
        assert e.value.status_code==status.CONFLICT
        
def test_task_add_double_booking():
    user=UserEntity(
        id=uuid.uuid4(),
        name='test',
        tasks=[],
        exp_tasks=[],
        point=0
    )
    task_detail=TaskDetailEntity(
        id=uuid.uuid4(),
        name='test_detail',
        max_worker=1,
        min_worker=1,
        exp_worker=0,
        duration=datetime.timedelta(hours=1),
        group_id=uuid.uuid4()
    )
    task=TaskEntity(
        id=uuid.uuid4(),
        name='test',
        start_time=datetime.datetime.now()+datetime.timedelta(hours=1),
        status=TaskState.hiring,
        taskdetail=task_detail,
        workers=[user.id]
    )
    with pytest.raises(DomainException) as e:
        task.add(user)
        assert e.value.status_code==status.CONFLICT