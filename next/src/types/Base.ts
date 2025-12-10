import { ID, Text } from "@/utils/types";
import { ShiftRequest } from "./ShiftType";
import { TaskRequest } from "./TaskType";
import { LoginRequest, UserRequest } from "./UserType";
import { TemplateSlot } from "./TemplateType";

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
