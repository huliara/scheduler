import { Base } from "./Base";

export type GroupUserResponse = Base & {
  room_number: string;
  point: number;
};
export type GroupUsersResponse = {
  users: GroupUserResponse[];
};
