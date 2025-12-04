export const permissions = [
  "add_user",
  "remove_user",
  "edit_task",
  "edit_template",
  "edit_role",
  "change_user_role",
  "edit_slot",
  "add_slot_from_template",
  "edit_point",
] as const;
export type Permission = (typeof permissions)[number];
