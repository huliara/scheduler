import { Base } from "./Base";
import { TaskResponse } from "./TaskType";

export type ShiftBase = {
  name: string;
  start_time: string;
  task_id: string;
};

export type ShiftRequest = ShiftBase;

export type ShiftResponse = Base & {
  start_time: string;
  end_time: string;
  status: number;
  task: TaskResponse;
  workers: Base[];
  creater_id: string;
  group_id: string;
};
export type ShiftsResponse = {
  shifts: ShiftResponse[];
};
