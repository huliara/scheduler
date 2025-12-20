import { ID, Text, TimeString } from "@/utils/types";
import { Base } from "./Base";

export type TemplateSlot = {
  task_id: ID;
  date_from_start: number;
  start_time: TimeString;
};

export type TemplateSlotResponse = TemplateSlot & {
  id: ID;
  name: Text;
};
export type TemplateResponse = Base & {
  group_id: ID;
  group_name: Text | null;
  slots: TemplateSlotResponse[];
};
export type TemplateRequest = {
  name: Text;
  slots: TemplateSlot[];
  group_id: ID;
};
