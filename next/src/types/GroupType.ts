import { Base } from "./Base";
import { MemberResponse } from "./GroupUser";
export type GroupResponse = Base & {
  users: MemberResponse[];
  task_details: Base[];
  template: Base[];
};
