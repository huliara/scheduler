import { ShiftResponse } from "./ShiftType";

export type ListProps = {
  url: string;
};

export type UserShiftRespose = {
  assign: ShiftResponse[];
  hiring: ShiftResponse[];
  end: ShiftResponse[];
};
