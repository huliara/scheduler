from enum import Enum


class Permission(Enum):
    add_user='add_user'
    remove_user='remove_user'
    edit_task='edit_task'
    edit_template='edit_template'
    edit_shift='edit_shift'
    generate_shift_from_template='generate_shift_from_template'
    edit_point='edit_point'
    edit_group='edit_group'
    