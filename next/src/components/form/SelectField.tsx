"use client";
import * as React from "react";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import {
  getFieldJA,
  RequestFieldKeys,
  _fieldURL,
  getFieldURL,
} from "@/utils/types";
import useSWR from "swr";
import { Base } from "@/types/Base";
import { fetcher } from "@/axios";

export const SelectField = ({
  fieldKey,
  defaultValue,
  params,
}: {
  fieldKey: RequestFieldKeys;
  defaultValue: string;
  params?: string | null;
}) => {
  const { data, error, isLoading } = useSWR<Base[]>(
    getFieldURL(fieldKey, params),
    fetcher
  );

  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;
  return (
    <div>
      <FormControl sx={{ m: 1, minWidth: 120 }}>
        <InputLabel id={fieldKey}>{getFieldJA(fieldKey)}</InputLabel>
        <Select
          labelId={fieldKey}
          id={fieldKey}
          defaultValue={defaultValue}
          label={getFieldJA(fieldKey)}
        >
          {data.map((data) => (
            <MenuItem key={data.id} value={data.id}>
              {data.name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </div>
  );
};
