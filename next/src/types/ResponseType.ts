export type ListProps = {
  url: string;
};
export type ResponseBase = {
  id: string;
  name: string;
};

export type GroupResponse = ResponseBase;
export const permissions = [
  "add_user",
  "remove_user",
  "edit_task",
  "edit_template",
  "edit_role",
  "change_user_role",
  "edit_slot",
  "add_slot_from_template",
  "edit_point",
] as const;

export type Permission = (typeof permissions)[number];

export type RoleResponse = ResponseBase & {
  permissions: Permission[];
};

export type RolesResponse = {
  roles: RoleResponse[];
};

export type GroupUserResponse = GroupResponse & {
  room_number: string;
  point: number;
  is_active: boolean;
  is_owner: boolean;
};

export type GroupUsersResponse = {
  users: GroupUserResponse[];
};

export type UserResponse = ResponseBase & {
  room_number: string;
  is_active: boolean;
};

export type UsersResponse = {
  users: UserResponse[];
};

export type UserDetailResponse = ResponseBase & {
  room_number: string;
  groups: ResponseBase[];
  exp_tasks: ResponseBase[];
  is_active: boolean;
  is_admin: boolean;
};

export type TaskDetailResponse = ResponseBase & {
  subtasks: string[];
  max_worker: number;
  min_worker: number;
  exp_worker: number;
  wage: number;
  duration: number;
  creater_id: string;
  creater_name: string;
  group_id: string;
};

export type TaskDetailsResponse = {
  tasks: TaskDetailResponse[];
};

export type TaskResponse = ResponseBase & {
  start_time: string;
  end_time: string;
  status: number;
  taskdetail: TaskDetailResponse;
  workers: ResponseBase[];
  creater_id: string;
  group_id: string;
};

export type UserTaskRespose = {
  assign: TaskResponse[];
  hiring: TaskResponse[];
  end: TaskResponse[];
};

export type TemplateTask = ResponseBase & {
  date_from_start: number;
  start_time: string;
};

export type TemplateTaskResponse = TemplateTask & {
  taskdetail_id: string;
};

export type TemplateResponse = ResponseBase & {
  group_id: string;
  slots: TemplateTaskResponse[];
};
