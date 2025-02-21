from datetime import date, datetime

from sqlalchemy.orm import Session

from app.cruds.template import generate_slots, post
from app.models.models import Group, TaskDetail, User
from app.schemas.template import TemplateCreate, TemplateTaskBase, TemplateTime

user = {
    "name": "user_1",
    "password": "bid_1_password",
    "block": "B3",
    "room_number": "B310",
}

template_post_data = {
    "name": "testTemplate",
    "tasks": [
        {
            "date_from_start": 0,
            "time": {
                "hour": 0,
                "minute": 0,
            },
        }
    ],
}
task_test_data = [
    {
        "name": "task_1",
        "detail": "bid_1_password",
        "max_woker_num": 3,
        "min_woker_num": 3,
        "exp_woker_num": 3,
    },
    {
        "name": "task_2",
        "detail": "bid_1_password",
        "max_woker_num": 3,
        "min_woker_num": 3,
        "exp_woker_num": 2,
    },
]

test_group = {
    "name": "testGroup",
}


def test_create_template(test_db: Session):
    db_user = User(
        name=user["name"],
        password=user["password"],
        room_number=user["room_number"],
    )
    test_db.add(db_user)
    test_db.commit()
    test_db.refresh(db_user)
    db_group = Group(name=test_group["name"])
    test_db.add(db_group)
    testtask = TaskDetail(
        name=task_test_data[0]["name"],
        detail=task_test_data[0]["detail"],
        max_worker_num=task_test_data[0]["max_woker_num"],
        min_worker_num=task_test_data[0]["min_woker_num"],
        exp_worker_num=task_test_data[0]["exp_woker_num"],
        group=db_group,
    )
    test_db.add(testtask)
    test_db.commit()
    test_db.refresh(testtask)

    starttime = TemplateTime(hour=0, minute=0)
    endtime = TemplateTime(hour=1, minute=0)

    templetask1 = TemplateTaskBase(
        id=testtask.id,
        date_from_start=0,
        start_time=starttime,
        end_time=endtime,
    )

    templetask2 = TemplateTaskBase(
        id=testtask.id,
        date_from_start=0,
        start_time=starttime,
        end_time=endtime,
    )
    templetask3 = TemplateTaskBase(
        id=testtask.id,
        date_from_start=1,
        start_time=starttime,
        end_time=endtime,
    )
    post_data = TemplateCreate(
        name="testTemplate", tasks=[templetask1, templetask2, templetask3]
    )
    template = post(post_data, test_db)
    assert template.name == "testTemplate"
    assert len(template.tasktemplates) == 2
    assert template.tasktemplates[0].start_time.hour == 0
    assert template.tasktemplates[0].start_time.minute == 0
    assert template.tasktemplates[0].end_time.hour == 1
    assert template.tasktemplates[0].end_time.minute == 0
    start_day = date(2021, 1, 1)
    slots = generate_slots(template, start_day, db_user, test_db)

    assert len(slots) == 2
    assert slots[0].start_time == datetime(2021, 1, 1, 0, 0, 0)
    assert slots[0].end_time == datetime(2021, 1, 1, 1, 0, 0)
