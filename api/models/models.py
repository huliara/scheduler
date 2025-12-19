from __future__ import annotations

import datetime
import uuid
from uuid import uuid4

from ddd.domain.permission.permission import Permission
from ddd.domain.shift.shift_state import ShiftState
from sqlalchemy import ARRAY, Column, Enum, ForeignKey, String, Table
from sqlalchemy.ext.associationproxy import AssociationProxy, association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


experience_table = Table(
    "experience_table",
    Base.metadata,
    Column("user", ForeignKey("user.id"), primary_key=True),
    Column("task", ForeignKey("task.id"), primary_key=True),
)

shifts_table = Table(
    "shifts_table",
    Base.metadata,
    Column("user", ForeignKey("user.id")),
    Column("shift", ForeignKey("shift.id")),
)

class BaseModelMixin:
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(20))


class Shift(BaseModelMixin,Base):
    __tablename__ = "shift"
    start_time: Mapped[datetime.datetime]
    status:Mapped[ShiftState]=mapped_column(Enum(ShiftState),default=ShiftState.before_hiring)
    workers: Mapped[list[User]] = relationship(
        secondary=shifts_table, back_populates="shifts"
    )
    creater_id: Mapped[None | uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL")
    )
    creater: Mapped[User| None] = relationship(back_populates="create_shifts")
    task_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("task.id", ondelete="CASCADE")
    )
    task: Mapped[Task] = relationship(back_populates="shifts", uselist=False)
    group_id:AssociationProxy[list[uuid.UUID]]=association_proxy(
        "task",
        "group_id"
    )
    @hybrid_property
    def end_time(self):
        return self.start_time + self.task.duration


class Task(BaseModelMixin,Base):
    __tablename__ = "task"
    group_id:Mapped[uuid.UUID]=mapped_column(
        ForeignKey("group.id",ondelete="CASCADE")
    )
    group:Mapped[Group]=relationship(back_populates="tasks")
    subtask: Mapped[list[SubTask]] = relationship(
        back_populates="task", cascade="all,delete-orphan"
    )
    max_worker: Mapped[int] = mapped_column(default=1)  # 最大人数
    min_worker: Mapped[int] = mapped_column(default=1)  # 最少人数
    exp_worker: Mapped[int] = mapped_column(default=0)  # 必要な経験者の人数
    wage: Mapped[int] = mapped_column(default=0)
    duration: Mapped[datetime.timedelta] = mapped_column(
        default=datetime.timedelta(hours=1)
    )
    permissions:Mapped[list[Permission]] =mapped_column(ARRAY(Enum(Permission))) 
    shifts: Mapped[list[Shift] ] = relationship(
        back_populates="task", cascade="all,delete"
    )
    experts: Mapped[list[User]] = relationship(
        secondary=experience_table, back_populates="exp_tasks"
    )
    creater_id: Mapped[None | uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="SET NULL")
    )
    creater: Mapped[None | User] = relationship(back_populates="create_tasks")
    tasktemplates: Mapped[list[TaskTemplate]] = relationship(
        back_populates="task", cascade="all,delete"
    )


class SubTask(Base):
    __tablename__ = "subtask"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    order: Mapped[int]
    task_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("task.id", ondelete="CASCADE")
    )
    task: Mapped[Task] = relationship(back_populates="subtask")
    description: Mapped[str] = mapped_column(String(100))
    


class TaskTemplate(Base):
    __tablename__ = "tasktemplate"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    template_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("template.id", ondelete="CASCADE")
    )
    template: Mapped[Template] = relationship(back_populates="tasktemplates")
    task_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("task.id", ondelete="CASCADE")
    )
    task: Mapped[Task] = relationship(back_populates="tasktemplates")
    date_from_start: Mapped[int] = mapped_column(default=0)
    start_time: Mapped[datetime.time]

    @hybrid_property
    def name(self):
        return self.start_time.strftime("%H時") + self.task.name

    @hybrid_property
    def end_time(self):
        return (
            datetime.datetime.combine(datetime.date.today(), self.start_time)
            + self.task.duration
        ).time()


class Template(BaseModelMixin,Base):
    __tablename__ = "template"
    tasktemplates: Mapped[list[TaskTemplate]] = relationship(
        back_populates="template", cascade="all,delete"
    )
    group_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("group.id", ondelete="CASCADE")
    )
    group: Mapped[Group] = relationship(back_populates="templates")
    
class Group(BaseModelMixin,Base):
    __tablename__ = "group"
    users:Mapped[list[GroupUser]] = relationship(back_populates="group",cascade="all,delete")
    tasks:Mapped[list[Task]]=relationship(back_populates='group',cascade='all,delete')
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
    is_active: Mapped[bool] = mapped_column(default=False)
    @hybrid_property
    def exp_tasks(self)->list[Task]:
        return self.user.exp_tasks
    @hybrid_property
    def name(self)->str:
        return self.user.name

class User(Base):
    __tablename__ = "user"
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column(String(28),unique=True)
    password: Mapped[str] = mapped_column(String(400))
    room_number: Mapped[str] = mapped_column(String(10))
    groups: Mapped[list[GroupUser]] = relationship( back_populates="user",cascade="all,delete")
    exp_tasks: Mapped[list[Task]] = relationship(
        secondary=experience_table, back_populates="experts"
    )
    shifts: Mapped[list[Shift]] = relationship(
        secondary=shifts_table, back_populates="workers"
    )
    create_shifts: Mapped[list[Shift]] = relationship(back_populates="creater")
    create_tasks: Mapped[list[Task]] = relationship(back_populates="creater")
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    
    @hybrid_property
    def point(self):
        return sum([group.point for group in self.groups])

    def has_exp(self, task: Task):
        return task in self.exp_tasks
