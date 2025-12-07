import { Base } from "./Base";

export type GroupUserResponse = Base & {
  room_number: string;
  point: number;
  is_active: boolean;
};
export type GroupUsersResponse = {
  users: GroupUserResponse[];
};
