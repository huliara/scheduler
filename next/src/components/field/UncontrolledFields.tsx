import {
  Field,
  FieldType,
  getFieldJA,
  isPositive,
  RequestFieldKeys,
} from "@/utils/types";
import OutlinedInput from "@mui/material/OutlinedInput";
import { DatePicker, DateTimePicker, TimePicker } from "@mui/x-date-pickers";
import dayjs from "dayjs";
import { UncontrolledSelectField } from "./UncontrolledSelectField";
import { MultiSelectField } from "./UncontrolledMultiSelectField";
import { MuiProvider } from "../provider/MUIProvider";
export const UncontrolledFormField = ({
  fieldKey,
  fieldType,
  defaultValue,
}: {
  fieldKey: RequestFieldKeys;
  fieldType: FieldType;
  defaultValue: number | string | string[];
}) => {
  switch (fieldType) {
    case Field.TEXT:
      return (
        <OutlinedInput
          id={fieldKey}
          name={fieldKey}
          type="text"
          autoComplete={fieldKey}
          required
          size="small"
          defaultValue={defaultValue}
        />
      );

    case Field.PASSWORD:
      return (
        <OutlinedInput
          id={fieldKey}
          name={fieldKey}
          type="password"
          autoComplete={fieldKey}
          required
          size="small"
        />
      );

    case Field.NUMBER:
      return (
        <input
          type="number"
          id={fieldKey}
          name={fieldKey}
          min={isPositive(fieldKey) ? 0 : undefined}
          defaultValue={typeof defaultValue == "number" ? defaultValue : 0}
        />
      );
    case Field.TIME:
      return (
        <MuiProvider>
          <TimePicker
            label="開始時刻"
            ampm={false}
            defaultValue={
              typeof defaultValue == "string" ? dayjs(defaultValue) : dayjs()
            }
            views={["hours", "minutes"]}
          />
        </MuiProvider>
      );
    case Field.DATE:
      return (
        <MuiProvider>
          <DatePicker
            label={getFieldJA(fieldKey)}
            defaultValue={
              typeof defaultValue == "string" ? dayjs(defaultValue) : dayjs()
            }
            views={["year", "month", "day"]}
          />
        </MuiProvider>
      );
    case Field.DATETIME:
      return (
        <MuiProvider>
          <DateTimePicker
            label={getFieldJA(fieldKey)}
            defaultValue={
              typeof defaultValue == "string" ? dayjs(defaultValue) : dayjs()
            }
          />
        </MuiProvider>
      );
    case Field.ID:
      return (
        <UncontrolledSelectField
          fieldKey={fieldKey}
          defaultValue={typeof defaultValue === "string" ? defaultValue : ""}
        />
      );
    case Field.IDs:
      return (
        <MultiSelectField
          fieldKey={fieldKey}
          defaultValue={Array.isArray(defaultValue) ? defaultValue : []}
        />
      );
  }
};
