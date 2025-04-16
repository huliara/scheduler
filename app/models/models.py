from __future__ import annotations

import datetime
import uuid
from uuid import uuid4

from sqlalchemy import ARRAY, Column, Enum, ForeignKey, String, Table
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.ddd.domain.permission.permission import Permission
from app.ddd.domain.task.task_state import TaskState

experience_table = Table(
    "experience_table",
    Base.metadata,
    Column("user", ForeignKey("user.id"), primary_key=True),
    Column("taskdetail", ForeignKey("taskdetail.id"), primary_key=True),
)

tasks_table = Table(
    "tasks_table",
    Base.metadata,
    Column("user", ForeignKey("user.id")),
    Column("task", ForeignKey("task.id")),
)



class Task(Base):
    __tablename__ = "task"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(20))
    start_time: Mapped[datetime.datetime]
    status:Mapped[TaskState]=mapped_column(Enum(TaskState),default=TaskState.before_hiring)
    workers: Mapped[list[User]] = relationship(
        secondary=tasks_table, back_populates="tasks"
    )
    creater_id: Mapped[None | uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL")
    )
    creater: Mapped[User| None] = relationship(back_populates="create_tasks")
    taskdetail_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("taskdetail.id", ondelete="CASCADE")
    )
    taskdetail: Mapped[TaskDetail] = relationship(back_populates="tasks", uselist=False)
    group_id:AssociationProxy[list[uuid.UUID]]=association_proxy(
        "taskdetail",
        "group_id"
    )
    @hybrid_property
    def end_time(self):
        return self.start_time + self.taskdetail.duration


class TaskDetail(Base):
    __tablename__ = "taskdetail"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(20))
    group_id:Mapped[uuid.UUID]=mapped_column(
        ForeignKey("group.id",ondelete="CASCADE")
    )
    group:Mapped[Group]=relationship(back_populates="taskdetail")
    subtask: Mapped[list[SubTask]] = relationship(
        back_populates="taskdetail", cascade="all,delete-orphan"
    )
    max_worker: Mapped[int] = mapped_column(default=1)  # 最大人数
    min_worker: Mapped[int] = mapped_column(default=1)  # 最少人数
    exp_worker: Mapped[int] = mapped_column(default=0)  # 必要な経験者の人数
    wage: Mapped[int] = mapped_column(default=0)
    duration: Mapped[datetime.timedelta] = mapped_column(
        default=datetime.timedelta(hours=1)
    )
    permissions:Mapped[list[Permission]] =mapped_column(ARRAY(Enum(Permission))) 
    tasks: Mapped[list[Task] ] = relationship(
        back_populates="taskdetail", cascade="all,delete"
    )
    experts: Mapped[list[User]] = relationship(
        secondary=experience_table, back_populates="exp_tasks"
    )
    creater_id: Mapped[None | uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL")
    )
    creater: Mapped[None | User] = relationship(back_populates="create_taskdetail")
    tasktemplates: Mapped[list[TaskTemplate]] = relationship(
        back_populates="taskdetail", cascade="all,delete"
    )


class SubTask(Base):
    __tablename__ = "subtask"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    order: Mapped[int]
    taskdetail_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("taskdetail.id", ondelete="CASCADE")
    )
    taskdetail: Mapped[TaskDetail] = relationship(back_populates="subtask")
    description: Mapped[str] = mapped_column(String(100))
    


class TaskTemplate(Base):
    __tablename__ = "tasktemplate"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    template_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("template.id", ondelete="CASCADE")
    )
    template: Mapped[Template] = relationship(back_populates="tasktemplates")
    taskdetail_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("taskdetail.id", ondelete="CASCADE")
    )
    taskdetail: Mapped[TaskDetail] = relationship(back_populates="tasktemplates")
    date_from_start: Mapped[int] = mapped_column(default=0)
    start_time: Mapped[datetime.time]

    @hybrid_property
    def name(self):
        return self.start_time.strftime("%H時") + self.taskdetail.name

    @hybrid_property
    def end_time(self):
        return (
            datetime.datetime.combine(datetime.date.today(), self.start_time)
            + self.taskdetail.duration
        ).time()


class Template(Base):
    __tablename__ = "template"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(20))
    tasktemplates: Mapped[list[TaskTemplate]] = relationship(
        back_populates="template", cascade="all,delete"
    )
    group_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("group.id", ondelete="CASCADE")
    )
    group: Mapped[Group] = relationship(back_populates="templates")
    
class Group(Base):
    __tablename__ = "group"
    id:Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    name:Mapped[str] = mapped_column(String(20))
    users:Mapped[list[GroupUser]] = relationship(back_populates="group",cascade="all,delete")
    taskdetail:Mapped[list[TaskDetail]]=relationship(back_populates='group',cascade='all,delete')
    templates:Mapped[list[Template]] = relationship(back_populates="group",cascade="all,delete")
    
class GroupUser(Base):
    __tablename__ = "group_user"
    group_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("group.id", ondelete="CASCADE"), primary_key=True
    )
    group: Mapped[Group] = relationship(back_populates="users")
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), primary_key=True
    )
    user: Mapped[User] = relationship(back_populates="groups")
    point: Mapped[float] = mapped_column(default=0)

class User(Base):
    __tablename__ = "user"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(20),unique=True)
    password: Mapped[str] = mapped_column(String(400))
    room_number: Mapped[str] = mapped_column(String(10))
    groups: Mapped[list[GroupUser]] = relationship( back_populates="user",cascade="all,delete")
    exp_tasks: Mapped[list[TaskDetail]] = relationship(
        secondary=experience_table, back_populates="experts"
    )
    tasks: Mapped[list[Task]] = relationship(
        secondary=tasks_table, back_populates="workers"
    )
    create_tasks: Mapped[list[Task]] = relationship(back_populates="creater")
    create_taskdetail: Mapped[list[TaskDetail]] = relationship(back_populates="creater")
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    
    @hybrid_property
    def point(self):
        return sum([group.point for group in self.groups])

    def has_exp(self, task: TaskDetail):
        return task in self.exp_tasks
