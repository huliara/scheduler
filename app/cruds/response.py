from app.models.models import (Group, GroupUser, Role, Task, TaskDetail,
                               TaskTemplate, Template, User)


def response_base(model):
    return {
        "id": model.id,
        "name": model.name,
    }


def user_display(user: User):
    return {
        "id": user.id,
        "name": user.name,
        "room_number": user.room_number,
        "is_active": user.is_active,
    }


def user_detail_display(user: User):
    return user_display(user) | {
        "groups": [
            {"id": group.group_id, "name": group.group.name} for group in user.groups
        ],
        "exp_tasks": [response_base(task) for task in user.exp_tasks],
        "slots": [response_base(slot) for slot in user.tasks],
        "create_slot": [response_base(slot) for slot in user.create_task],
        "create_task": [response_base(task) for task in user.create_taskdetail],
        "is_admin": user.is_admin,
    }


def slot_display(slot: Task):
    return {
        "id": slot.id,
        "name": slot.name,
        "start_time": slot.start_time,
        "end_time": slot.end_time,
        "creater_id": slot.creater_id,
        "creater_name": slot.creater.name,
        "assignees": [response_base(user) for user in slot.workers],
        "task_id": slot.task_id,
        "task_name": slot.task.name,
    }


def slots_display(slots: Task):
    return [slot_display(slot) for slot in slots]


def task_display(task: TaskDetail):
    return {
        "id": task.id,
        "name": task.name,
        "detail": task.detail,
        "max_worker_num": task.max_worker,
        "min_worker_num": task.min_worker,
        "exp_worker_num": task.exp_worker,
        "point": task.wage,
        "duration": int(task.duration.total_seconds()),
        "creater_id": task.creater_id,
        "creater_name": task.creater.name,
        "group_id": task.group_id,
    }


def tasks_display(tasks: TaskDetail):
    return [task_display(task) for task in tasks]


def template_display(template: Template):
    return {
        "id": template.id,
        "name": template.name,
        "group_id": template.group_id,
        "slots": [tasktemplate_display(task) for task in template.tasktemplates],
    }


def tasktemplate_display(tasktemplate: TaskTemplate):
    return {
        "id": tasktemplate.id,
        "name": tasktemplate.name,
        "task_id": tasktemplate.task_id,
        "date_from_start": tasktemplate.date_from_start,
        "start_time": tasktemplate.start_time,
    }


def group_user_display(user: GroupUser):
    return {
        "id": user.user_id,
        "name": user.user.name,
        "room_number": user.user.room_number,
        "point": user.point,
        "role": [response_base(role) for role in user.roles],
        "is_active": user.user.is_active,
    }
    
def group_display(group: Group):
    return {
        "id": group.id,
        "name": group.name
    }


permissions = [
    "add_user",
    "remove_user",
    "edit_task",
    "edit_template",
    "edit_role",
    "change_user_role",
    "edit_slot",
    "add_slot_from_template",
    "edit_point",
]


def role_display(role: Role):
    return {
        "id": role.id,
        "name": role.name,
        "permissions": [
            permission
            for permission in permissions
            if getattr(role, permission, None)
        ],
    }
