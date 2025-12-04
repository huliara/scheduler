import { ID, Text } from "@/utils/types";
import { ShiftRequest } from "./ShiftType";
import { TaskRequest } from "./TaskType";
import { UserRequest } from "./UserType";

export type Base = {
  id: ID;
  name: Text;
};

export type RequestType = UserRequest | ShiftRequest | TaskRequest;
