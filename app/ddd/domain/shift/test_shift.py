import datetime
import uuid
from http import HTTPStatus as status

import pytest
from deepdiff import DeepDiff

from app.ddd.core.exception import DomainException
from app.ddd.domain.task.task_entity import TaskEntity
from app.ddd.domain.user.user_entity import UserEntity

from .shift_entity import ShiftEntity
from .shift_state import ShiftState


def test_task_add_user():
    user=UserEntity(
        id=uuid.uuid4(),
        name='test',
        room_number='test',
        shifts=[],
        exp_tasks=[],
        point=0
    )
    task_detail=TaskEntity(
        name='test_detail',
        id=uuid.uuid4(),
        max_worker=1,
        min_worker=1,
        exp_worker=0,
        duration=datetime.timedelta(hours=1),
        group_id=uuid.uuid4(),
        creater_id=uuid.uuid4()
    )
    task=ShiftEntity(
        id=uuid.uuid4(),
        name='test',
        start_time=datetime.datetime.now()+datetime.timedelta(hours=1),
        status=ShiftState.hiring,
        task=task_detail,
        
    )
    task.add(user)
    assert task.workers==[user]

def test_task_add_exp_user():
    task_detail=TaskEntity(
        id=uuid.uuid4(),
        name='test_detail',
        max_worker=1,
        min_worker=1,
        exp_worker=1,
        duration=datetime.timedelta(hours=1),
        group_id=uuid.uuid4(),
        creater_id=uuid.uuid4()
    )
    user=UserEntity(
        id=uuid.uuid4(),
        name='test',
        room_number='test',
        shifts=[],
        exp_tasks=[task_detail.id],
        point=0
    )
    task=ShiftEntity(
        id=uuid.uuid4(),
        name='test',
        start_time=datetime.datetime.now()+datetime.timedelta(hours=1),
        status=ShiftState.hiring,
        task=task_detail,
    )
    task.add(user)
    assert task.workers==[user]
    
def test_task_add_beginner_with_expert():
    task_detail=TaskEntity(
        id=uuid.uuid4(),
        name='test_detail',
        max_worker=2,
        min_worker=1,
        exp_worker=1,
        duration=datetime.timedelta(hours=1),
        group_id=uuid.uuid4(),
        creater_id=uuid.uuid4()
    )
    user=UserEntity(
        id=uuid.uuid4(),
        name='test',
        room_number='test',
        shifts=[],
        exp_tasks=[],
        point=0
    )
    expert=UserEntity(
        id=uuid.uuid4(),
        name='test',
        room_number='test',
        shifts=[],
        exp_tasks=[task_detail.id],
        point=0
    )
    task=ShiftEntity(
        id=uuid.uuid4(),
        name='test',
        start_time=datetime.datetime.now()+datetime.timedelta(hours=1),
        status=ShiftState.hiring,
        task=task_detail,
        workers=[expert]
    )
    task.add(user)
    assert DeepDiff(list[task.workers],[expert,user],ignore_order=True)

def test_task_add_nonexpert():
    user=UserEntity(
        id=uuid.uuid4(),
        name='test',
        room_number='test',
        shifts=[],
        exp_tasks=[],
        point=0
    )
    task_detail=TaskEntity(
        id=uuid.uuid4(),
        name='test_detail',
        max_worker=1,
        min_worker=1,
        exp_worker=1,
        duration=datetime.timedelta(hours=1),
        group_id=uuid.uuid4(),
        creater_id=uuid.uuid4()
    )
    task=ShiftEntity(
        id=uuid.uuid4(),
        name='test',
        start_time=datetime.datetime.now()+datetime.timedelta(hours=1),
        status=ShiftState.hiring,
        task=task_detail,
        
    )
    with pytest.raises(DomainException) as e:
        task.add(user)
        assert e.value.status_code==status.CONFLICT
    
def test_task_add_user_over_max():
    dummy_user=UserEntity(
        id=uuid.uuid4(),
        name='test',
        room_number='test',
        shifts=[],
        exp_tasks=[],
        point=0
    )

                    
    user=UserEntity(
        id=uuid.uuid4(),
        name='test',
        room_number='test',
        shifts=[],
        exp_tasks=[],
        point=0
    )
    task_detail=TaskEntity(
        id=uuid.uuid4(),
        name='test_detail',
        max_worker=1,
        min_worker=1,
        exp_worker=0,
        duration=datetime.timedelta(hours=1),
        group_id=uuid.uuid4(),
        creater_id=uuid.uuid4()
    )
    task=ShiftEntity(
        id=uuid.uuid4(),
        name='test',
        start_time=datetime.datetime.now()+datetime.timedelta(hours=1),
        status=ShiftState.hiring,
        task=task_detail,
        workers=[dummy_user]
    )
    with pytest.raises(DomainException) as e:
        task.add(user)
        assert e.value.status_code==status.CONFLICT

def test_task_add_only_beginner():
    user=UserEntity(
        id=uuid.uuid4(),
        name='test',
        room_number='test',
        shifts=[],
        exp_tasks=[],
        point=0
    )
    task_detail=TaskEntity(
        id=uuid.uuid4(),
        name='test_detail',
        max_worker=2,
        min_worker=1,
        exp_worker=1,
        duration=datetime.timedelta(hours=1),
        group_id=uuid.uuid4(),
        creater_id=uuid.uuid4()
    )
    task=ShiftEntity(
        id=uuid.uuid4(),
        name='test',
        start_time=datetime.datetime.now()+datetime.timedelta(hours=1),
        status=ShiftState.hiring,
        task=task_detail,
        workers=[user]
    )
    with pytest.raises(DomainException) as e:
        task.add(user)
        assert e.value.status_code==status.CONFLICT

def test_task_add_user_after_end():
    user=UserEntity(
        id=uuid.uuid4(),
        name='test',
        room_number='test',
        shifts=[],
        exp_tasks=[],
        point=0
    )
    task_detail=TaskEntity(
        id=uuid.uuid4(),
        name='test_detail',
        max_worker=1,
        min_worker=1,
        exp_worker=0,
        duration=datetime.timedelta(hours=1),
        group_id=uuid.uuid4(),
        creater_id=uuid.uuid4()
        
    )
    task=ShiftEntity(
        id=uuid.uuid4(),
        name='test',
        start_time=datetime.datetime.now()-datetime.timedelta(hours=2),
        status=ShiftState.decide_assignees,
        task=task_detail,
        workers=[]
    )
    with pytest.raises(DomainException) as e:
        task.add(user)
        assert e.value.status_code==status.CONFLICT
        
def test_task_add_double_booking():
    user=UserEntity(
        id=uuid.uuid4(),
        name='test',
        room_number='test',
        shifts=[],
        exp_tasks=[],
        point=0
    )
    task_detail=TaskEntity(
        id=uuid.uuid4(),
        name='test_detail',
        max_worker=1,
        min_worker=1,
        exp_worker=0,
        duration=datetime.timedelta(hours=1),
        group_id=uuid.uuid4(),
        creater_id=uuid.uuid4()
    )
    task=ShiftEntity(
        id=uuid.uuid4(),
        name='test',
        start_time=datetime.datetime.now()+datetime.timedelta(hours=1),
        status=ShiftState.hiring,
        task=task_detail,
        workers=[user]
    )
    with pytest.raises(DomainException) as e:
        task.add(user)
        assert e.value.status_code==status.CONFLICT