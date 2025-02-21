from enum import Enum


class Permission(Enum):
    add_user='add_user'
    remove_user='remove_user'
    edit_task='edit_task'
    edit_template='edit_template'
    edit_taskdetail='edit_taskdetail'
    generate_task_from_template='generate_task_from_template'
    edit_point='edit_point'
    