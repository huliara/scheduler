import { Base, RequestType } from "@/types/Base";
import {
  Field,
  fieldType,
  formFieldJA,
  isPositive,
  RequestFieldKeys,
} from "@/utils/types";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";
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

const FormField = ({
  fieldKey,
  defaultValue,
}: {
  fieldKey: RequestFieldKeys;
  defaultValue: number | string | string[];
}) => {
  const field = fieldType(fieldKey);
  switch (field) {
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
          label={formFieldJA(fieldKey)}
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
          label={formFieldJA(fieldKey)}
          defaultValue={
            typeof defaultValue == "string" ? dayjs(defaultValue) : dayjs()
          }
          views={["year", "month", "day"]}
        />
      );
    case Field.DATETIME:
      return (
        <DateTimePicker
          label={formFieldJA(fieldKey)}
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
    <Grid container spacing={3}>
      {(Object.keys(props.data) as RequestFieldKeys[]).map((key) => {
        const value = (props.data as any)[key];
        if (fieldType(key) === Field.MULTI_TEXT) {
          return null;
        }
        return (
          <FormGrid size={{ xs: 12, md: 6 }}>
            <FormLabel htmlFor={key} required>
              {formFieldJA(key)}
            </FormLabel>
            <FormField fieldKey={key} defaultValue={value} />
          </FormGrid>
        );
      })}
    </Grid>
  );
};
