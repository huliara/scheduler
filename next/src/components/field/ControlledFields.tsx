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
import { MuiProvider } from "../provider/MUIProvider";
import { ControlledSelectField } from "./ControlledSelectField";
import { ControlledMultiSelectField } from "./ControlledMultiSelectField";
import { RequestType } from "@/types/Base";

type Props<T extends RequestType> = {
  fieldKey: RequestFieldKeys;
  fieldType: FieldType;
  value: number | string | string[];
  setFormValue: React.Dispatch<React.SetStateAction<T | undefined>>;
};

export const ControlledFormField = <T extends RequestType>({
  fieldKey,
  fieldType,
  value,
  setFormValue,
}: React.PropsWithChildren<Props<T>>) => {
  switch (fieldType) {
    case Field.TEXT:
    case Field.PASSWORD:
      return (
        <OutlinedInput
          id={fieldKey}
          name={fieldKey}
          type={fieldType === Field.PASSWORD ? "password" : "text"}
          autoComplete={fieldKey}
          required
          size="small"
          value={value}
          onChange={(event) =>
            setFormValue(
              (prev) =>
                ({
                  ...prev,
                  [fieldKey]: event.target.value,
                } as T)
            )
          }
        />
      );

    case Field.NUMBER:
      return (
        <input
          type="number"
          id={fieldKey}
          name={fieldKey}
          min={isPositive(fieldKey) ? 0 : undefined}
          value={typeof value == "number" ? value : 0}
          onChange={(e) =>
            setFormValue(
              (prev) =>
                ({
                  ...prev,
                  [fieldKey]: Number(e.target.value),
                } as T)
            )
          }
        />
      );
    case Field.TIME:
      return (
        <MuiProvider>
          <TimePicker
            label={getFieldJA(fieldKey)}
            ampm={false}
            value={typeof value == "string" ? dayjs(value) : dayjs()}
            views={["hours", "minutes"]}
            onChange={(newValue: dayjs.Dayjs | null) => {
              setFormValue((prev) => ({ ...prev, [fieldKey]: newValue } as T));
            }}
          />
        </MuiProvider>
      );
    case Field.DATE:
      return (
        <MuiProvider>
          <DatePicker
            label={getFieldJA(fieldKey)}
            value={typeof value == "string" ? dayjs(value) : dayjs()}
            views={["year", "month", "day"]}
            onChange={(newValue: dayjs.Dayjs | null) => {
              setFormValue((prev) => ({ ...prev, [fieldKey]: newValue } as T));
            }}
          />
        </MuiProvider>
      );
    case Field.DATETIME:
      return (
        <MuiProvider>
          <DateTimePicker
            label={getFieldJA(fieldKey)}
            value={typeof value == "string" ? dayjs(value) : dayjs()}
            onChange={(newValue: dayjs.Dayjs | null) => {
              setFormValue((prev) => ({ ...prev, [fieldKey]: newValue } as T));
            }}
          />
        </MuiProvider>
      );
    case Field.ID:
      return (
        <ControlledSelectField
          fieldKey={fieldKey}
          value={typeof value === "string" ? value : ""}
          setFormValue={setFormValue}
        />
      );
    case Field.IDs:
      return (
        <ControlledMultiSelectField
          fieldKey={fieldKey}
          value={Array.isArray(value) ? value : []}
          setFormValue={setFormValue}
        />
      );
  }
};
