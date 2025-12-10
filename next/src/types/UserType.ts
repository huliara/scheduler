import { IDs, Password, Text } from "@/utils/types";
import { Base } from "./Base";

type UserBase = {
  name: Text;
  room_number: Text;
};

export type LoginRequest = {
  name: Text;
  password: Password;
};

export type UserResponse = Base & {
  room_number: Text;
  is_active: boolean;
};
export type UsersResponse = {
  users: UserResponse[];
};
export type UserDetailResponse = UserResponse & {
  point: number;
  exp_tasks: Base[];
  shifts: Base[];
  groups: Base[];
  is_active: boolean;
};

export type UserRequest = UserBase & {
  password: Password;
  exp_tasks: IDs;
};
