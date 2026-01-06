## Geminiで書いたテスト。現状使えません。

import pytest
from unittest.mock import MagicMock, AsyncMock
from datetime import datetime, timedelta
import uuid

from ddd.service.usecases.shift.allocator.shifts_allocate_worker import ShiftAllocationWorkerUseCase, AllocWorkerDTO
from ddd.domain.shift.shift_value_object import ShiftId
from ddd.domain.task import TaskEntity, TaskId
from ddd.domain.user import UserEntity, UserId
from ddd.domain.group import GroupId

# モックの準備
@pytest.fixture
def mock_user_repo():
    repo = MagicMock()
    return repo

@pytest.fixture
def mock_shift_repo():
    repo = MagicMock()
    return repo

@pytest.fixture
def usecase(mock_user_repo, mock_shift_repo):
    return ShiftAllocationWorkerUseCase(mock_user_repo, mock_shift_repo)

def create_task(id_str, min_w=1, max_w=2, exp_w=0, wage=1000):
    return TaskEntity(
        id=TaskId(uuid.UUID(id_str)),
        name="Test Task",
        max_worker=max_w,
        min_worker=min_w,
        exp_worker=exp_w,
        duration=timedelta(hours=1),
        group_id=GroupId(uuid.uuid4()),
        creater_id=UserId(uuid.uuid4()),
        wage=wage
    )

def create_shift(id_str, task):
    # 未来の日時を設定してバリデーションエラーを回避
    start_time = datetime.now() + timedelta(days=1)
    return ShiftEntity(
        id=ShiftId(uuid.UUID(id_str)),
        name="Test Shift",
        start_time=start_time,
        task=task,
        workers=[]
    )

def create_user(id_str, exp_tasks=None):
    if exp_tasks is None:
        exp_tasks = []
    return UserEntity(
        id=UserId(uuid.UUID(id_str)),
        name="Test User",
        room_number="101",
        exp_tasks=exp_tasks,
        point=0
    )

def create_alloc_dto(id_str, point=0, exp_tasks=None):
    if exp_tasks is None:
        exp_tasks = []
    return AllocWorkerDTO(
        id=UserId(uuid.UUID(id_str)),
        point=point,
        exp_tasks=exp_tasks
    )

@pytest.mark.asyncio
async def test_execute_normal(usecase, mock_user_repo, mock_shift_repo):
    # データの準備
    task_id_uuid = uuid.uuid4()
    task_id = TaskId(task_id_uuid)
    # max_worker=1, min_worker=1 なので必ず1人割り当てられるはず
    task = create_task(str(task_id), min_w=1, max_w=1, exp_w=0)
    shift = create_shift(str(uuid.uuid4()), task)
    
    user_id_uuid = uuid.uuid4()
    user_id = UserId(user_id_uuid)
    user_entity = create_user(str(user_id), exp_tasks=[task_id])
    user_dto = create_alloc_dto(str(user_id), exp_tasks=[task_id])
    
    shifts = [shift]
    users = [user_dto]
    
    # モックの振る舞い設定
    # find_by_id は同期メソッド
    mock_user_repo.find_by_id.return_value = user_entity
    mock_shift_repo.save.side_effect = lambda x: x # そのまま返す
    
    # 実行
    result = await usecase.execute(shifts, users)
    
    # 検証
    assert len(result) == 1
    # mipの計算結果によるが、条件を満たすなら割り当てられるはず
    # ここでは1つのシフトに1人のユーザー、条件も合致するので割り当てられると期待
    assert len(result[0].workers) == 1
    assert result[0].workers[0].id == user_id
    mock_shift_repo.save.assert_called()

@pytest.mark.asyncio
async def test_execute_empty_shifts(usecase):
    result = await usecase.execute([], [create_alloc_dto(str(uuid.uuid4()))])
    assert result == []

@pytest.mark.asyncio
async def test_execute_empty_users(usecase):
    task = create_task(str(uuid.uuid4()))
    shift = create_shift(str(uuid.uuid4()), task)
    result = await usecase.execute([shift], [])
    assert result == []

@pytest.mark.asyncio
async def test_execute_too_many_shifts(usecase):
    shifts = [create_shift(str(uuid.uuid4()), create_task(str(uuid.uuid4()))) for _ in range(41)]
    users = [create_alloc_dto(str(uuid.uuid4()))]
    with pytest.raises(ValueError, match="shift_ids must be less than 40"):
        await usecase.execute(shifts, users)

@pytest.mark.asyncio
async def test_execute_too_many_users(usecase):
    task = create_task(str(uuid.uuid4()))
    shift = create_shift(str(uuid.uuid4()), task)
    users = [create_alloc_dto(str(uuid.uuid4())) for _ in range(501)]
    with pytest.raises(ValueError, match="user_ids must be less than 500"):
        await usecase.execute([shift], users)
