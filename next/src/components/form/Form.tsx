import { RequestType } from "@/types/Base";
import {
  Field,
  FieldType,
  getFieldType,
  getFieldJA,
  isPositive,
  RequestFieldKeys,
} from "@/utils/types";
import FormLabel from "@mui/material/FormLabel";
import Grid from "@mui/material/Grid";
import OutlinedInput from "@mui/material/OutlinedInput";
import { styled } from "@mui/material/styles";
import { ReactElement } from "react";
import { NumberField } from "@base-ui-components/react/number-field";
import { DateTimePicker, TimePicker, DatePicker } from "@mui/x-date-pickers";
import dayjs from "dayjs";
import { SelectField } from "./SelectField";
import { MultiSelectField } from "./MultiSelectField";
const FormGrid = styled(Grid)(() => ({
  display: "flex",
  flexDirection: "column",
}));

type Props<T extends RequestType> = {
  data: T;
};

export const FormField = ({
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
        <NumberField.Root
          id={fieldKey}
          name={fieldKey}
          min={isPositive(fieldKey) ? 0 : undefined}
          defaultValue={typeof defaultValue == "number" ? defaultValue : 0}
        >
          <NumberField.ScrubArea>
            <NumberField.ScrubAreaCursor />
          </NumberField.ScrubArea>
          <NumberField.Group>
            <NumberField.Decrement />
            <NumberField.Input />
            <NumberField.Increment />
          </NumberField.Group>
        </NumberField.Root>
      );
    case Field.TIME:
      return (
        <TimePicker
          label={getFieldJA(fieldKey)}
          ampm={false}
          defaultValue={
            typeof defaultValue == "string" ? dayjs(defaultValue) : dayjs()
          }
          views={["hours", "minutes"]}
        />
      );
    case Field.DATE:
      return (
        <DatePicker
          label={getFieldJA(fieldKey)}
          defaultValue={
            typeof defaultValue == "string" ? dayjs(defaultValue) : dayjs()
          }
          views={["year", "month", "day"]}
        />
      );
    case Field.DATETIME:
      return (
        <DateTimePicker
          label={getFieldJA(fieldKey)}
          defaultValue={
            typeof defaultValue == "string" ? dayjs(defaultValue) : dayjs()
          }
        />
      );
    case Field.ID:
      return (
        <SelectField
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

export const SchedulerForm = <T extends RequestType>(
  props: React.PropsWithChildren<Props<T>>
): ReactElement<any, any> => {
  return (
    <>
      {(Object.keys(props.data) as RequestFieldKeys[]).map((key) => {
        const value = (props.data as any)[key];
        const fieldType = getFieldType(key);
        const fieldJA = getFieldJA(key);
        if (fieldType === Field.MULTI_TEXT) {
          return null;
        }
        return (
          <FormGrid size={{ xs: 12, md: 6 }}>
            <FormLabel htmlFor={key} required>
              {fieldJA}
            </FormLabel>
            <FormField
              fieldKey={key}
              fieldType={fieldType}
              defaultValue={value}
            />
          </FormGrid>
        );
      })}
    </>
  );
};
