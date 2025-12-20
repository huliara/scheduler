"use client";
import { RequestType } from "@/types/Base";
import {
  Field,
  getFieldType,
  getFieldJA,
  RequestFieldKeys,
} from "@/utils/types";
import FormLabel from "@mui/material/FormLabel";
import Grid from "@mui/material/Grid";
import { styled } from "@mui/material/styles";
import { ReactElement } from "react";
import { UncontrolledFormField } from "../field/UncontrolledFields";
const FormGrid = styled(Grid)(() => ({
  display: "flex",
  flexDirection: "column",
}));

type Props<T extends RequestType> = {
  data: T;
};

export const UncontrolledForm = <T extends RequestType>(
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
          <FormGrid size={fieldType === Field.NUMBER ? 4 : 12} key={key}>
            <FormLabel htmlFor={key} required>
              {fieldJA}
            </FormLabel>
            <UncontrolledFormField
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
