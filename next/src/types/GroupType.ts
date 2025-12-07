import { Base } from "./Base";
import { GroupUserResponse } from "./GroupUser";
export type GroupResponse = Base & {
  users: GroupUserResponse[];
  task_details: Base[];
  template: Base[];
};
