import { Base } from "./Base";

export type ShiftBase = {
  start_time: string;
  task_id: string;
};

export type ShiftRequest = ShiftBase;

export type ShiftsResponse = {
  shifts: ShiftBase[];
};

export type ShiftResponse = Base & {
  start_time: string;
  end_time: string;
  status: number;
  task: Base;
  workers: Base[];
  creater_id: string;
  group_id: string;
};
