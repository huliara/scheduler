import { Base } from "./Base";

export type TaskBase = {
  subtasks: string[];
  max_worker: number;
  min_worker: number;
  exp_worker: number;
  wage: number;
  permissions: string[];
  duration: number;
  group_id: string;
};

export type TaskResponse = Base &
  TaskBase & {
    creater_id: string;
  };
export type TasksResponse = {
  tasks: TaskResponse[];
};
export type TaskRequest = TaskBase & {
  name: string;
};
