import { RequestType } from "@/types/Base";
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
import { DateTimePicker } from "@mui/x-date-pickers/DateTimePicker";
import dayjs from "dayjs";
const FormGrid = styled(Grid)(() => ({
  display: "flex",
  flexDirection: "column",
}));

type Props<T extends RequestType> = {
  data: T;
};

const FormField = <T extends number|string|string[]>(key: RequestFieldKeys,defaultValue:T,options?:T[]) => {
  const field = fieldType(key);
  switch (field) {
    case Field.TEXT:
      return (
        <OutlinedInput
          id={key}
          name={key}
          type="text"
          autoComplete={key}
          required
              size="small"
              defaultValue={defaultValue}
        />
      );

    case Field.PASSWORD:
      return (
        <OutlinedInput
          id={key}
          name={key}
          type="password"
          autoComplete={key}
          required
          size="small"
        />
      );

    case Field.NUMBER:
      return (
        <NumberField.Root
          id={key}
          name={key}
              min={isPositive(key) ? 0 : undefined}
              defaultValue={typeof defaultValue=="number"?defaultValue:0}
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
    case Field.DATETIME:
      return (
        <DateTimePicker
          label={formFieldJA(key)}
          defaultValue={typeof defaultValue=='string'? dayjs(defaultValue):dayjs(today)}
        />
      );
      case Field.ID:
          return (
            
        )
  }
};

export const SchedulerForm = <T extends RequestType>(
  props: React.PropsWithChildren<Props<T>>
): ReactElement<any, any> => {
  return (
    <Grid container spacing={3}>
          {(Object.keys(props.data) as (RequestFieldKeys[])).map((key) => {
          const value=(props.data as any)[key]
        return (
          <FormGrid size={{ xs: 12, md: 6 }}>
            <FormLabel htmlFor={key} required>
              First name
            </FormLabel>
            {FormField(key,value)}
          </FormGrid>
        );
      })}

      <FormGrid size={{ xs: 12, md: 6 }}>
        <FormLabel htmlFor="last-name" required>
          Last name
        </FormLabel>
        <OutlinedInput
          id="last-name"
          name="last-name"
          type="last-name"
          placeholder="Snow"
          autoComplete="last name"
          required
          size="small"
        />
      </FormGrid>
      <FormGrid size={{ xs: 12 }}>
        <FormLabel htmlFor="address1" required>
          Address line 1
        </FormLabel>
        <OutlinedInput
          id="address1"
          name="address1"
          type="address1"
          placeholder="Street name and number"
          autoComplete="shipping address-line1"
          required
          size="small"
        />
      </FormGrid>
      <FormGrid size={{ xs: 12 }}>
        <FormLabel htmlFor="address2">Address line 2</FormLabel>
        <OutlinedInput
          id="address2"
          name="address2"
          type="address2"
          placeholder="Apartment, suite, unit, etc. (optional)"
          autoComplete="shipping address-line2"
          required
          size="small"
        />
      </FormGrid>
      <FormGrid size={{ xs: 6 }}>
        <FormLabel htmlFor="city" required>
          City
        </FormLabel>
        <OutlinedInput
          id="city"
          name="city"
          type="city"
          placeholder="New York"
          autoComplete="City"
          required
          size="small"
        />
      </FormGrid>
      <FormGrid size={{ xs: 6 }}>
        <FormLabel htmlFor="state" required>
          State
        </FormLabel>
        <OutlinedInput
          id="state"
          name="state"
          type="state"
          placeholder="NY"
          autoComplete="State"
          required
          size="small"
        />
      </FormGrid>
      <FormGrid size={{ xs: 6 }}>
        <FormLabel htmlFor="zip" required>
          Zip / Postal code
        </FormLabel>
        <OutlinedInput
          id="zip"
          name="zip"
          type="zip"
          placeholder="12345"
          autoComplete="shipping postal-code"
          required
          size="small"
        />
      </FormGrid>
      <FormGrid size={{ xs: 6 }}>
        <FormLabel htmlFor="country" required>
          Country
        </FormLabel>
        <OutlinedInput
          id="country"
          name="country"
          type="country"
          placeholder="United States"
          autoComplete="shipping country"
          required
          size="small"
        />
      </FormGrid>
      <FormGrid size={{ xs: 12 }}>
        <FormControlLabel
          control={<Checkbox name="saveAddress" value="yes" />}
          label="Use this address for payment details"
        />
      </FormGrid>
    </Grid>
  );
};
