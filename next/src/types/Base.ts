import { ID, Text } from "@/utils/types";
import { ShiftRequest, ShiftResponse } from "./ShiftType";
import { TaskRequest, TaskResponse } from "./TaskType";
import { LoginRequest, UserRequest, UserResponse } from "./UserType";
import { TemplateResponse, TemplateSlot } from "./TemplateType";

export type Base = {
  id: ID;
  name: Text;
};

export type RequestType =
  | UserRequest
  | ShiftRequest
  | TaskRequest
  | TemplateSlot
  | LoginRequest;

export type ResponseType =
  | ShiftResponse
  | TaskResponse
  | TemplateResponse
  | UserResponse;

export type GroupDataType = ShiftResponse | TaskResponse | TemplateResponse;
