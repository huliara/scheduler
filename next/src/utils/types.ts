import { ShiftRequest } from "@/types/ShiftType";
import { TaskRequest } from "@/types/TaskType";
import { UserRequest } from "@/types/UserType";
export type Text = string;
export type Password = string;
export type ID = string;
export type IDs = ID[];
export type MultiText = Text[];
export type DatetimeString = string;
export type TimeString = string;
export type DateString = string;

export const Field = {
  TEXT: "text",
  PASSWORD: "password",
  NUMBER: "number",
  TIME: "time",
  DATE: "date",
  DATETIME: "datetime-local",
  ID: "id",
  IDs: "ids",
  MULTI_TEXT: "multi_text",
} as const;

export type FieldType = (typeof Field)[keyof typeof Field];

type RequestAllFieldType = UserRequest & ShiftRequest & TaskRequest;

export type RequestFieldKeys = keyof RequestAllFieldType;

export const fieldType = (key: RequestFieldKeys): FieldType => {
  switch (key) {
    case "name":
    case "room_number":
      return Field.TEXT;
    case "start_time":
      return Field.DATETIME;
    case "task_id":
    case "group_id":
      return Field.ID;
    case "subtasks":
      return Field.MULTI_TEXT;
    case "max_worker":
    case "min_worker":
    case "exp_worker":
    case "wage":
    case "duration":
      return Field.NUMBER;
    case "permissions":
      return Field.MULTI_TEXT;
    case "exp_tasks":
      return Field.IDs;
    case "password":
      return Field.PASSWORD;
  }
};

export const formFieldJA = (key: RequestFieldKeys): string => {
  switch (key) {
    case "name":
      return "名前";
    case "room_number":
      return "部屋番号";
    case "start_time":
      return "開始日時";
    case "task_id":
      return "タスク";
    case "group_id":
      return "グループ";
    case "subtasks":
      return "サブタスク";
    case "max_worker":
      return "最大人数";
    case "min_worker":
      return "最小人数";
    case "exp_worker":
      return "経験者数";
    case "wage":
      return "ポイント";
    case "duration":
      return "所要時間(分)";
    case "permissions":
      return "権限";
    case "exp_tasks":
      return "経験したタスク";
    case "password":
      return "パスワード";
    default:
      return key;
  }
};

export const isPositive = (key: RequestFieldKeys): boolean => {
  return (
    key === "max_worker" ||
    key === "min_worker" ||
    key === "exp_worker" ||
    key === "duration"
  );
};

export const selectFieldURL = (key: RequestFieldKeys): string => {
  switch (key) {
    case "task_id":
      return "/api/tasks";
    case "group_id":
      return "/api/groups";
    case "exp_tasks":
      return "/api/tasks";
    default:
      return "";
  }
};
