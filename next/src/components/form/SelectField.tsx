import * as React from "react";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import { formFieldJA, RequestFieldKeys, selectFieldURL } from "@/utils/types";
import useSWR from "swr";
import { Base } from "@/types/Base";
import { fetcher } from "@/axios";

export const SelectField = ({
  fieldKey,
  defaultValue,
}: {
  fieldKey: RequestFieldKeys;
  defaultValue: string;
}) => {
  const { data, error, isLoading } = useSWR<Base[]>(
    selectFieldURL(fieldKey),
    fetcher
  );

  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;
  return (
    <div>
      <FormControl sx={{ m: 1, minWidth: 120 }}>
        <InputLabel id={fieldKey}>{formFieldJA(fieldKey)}</InputLabel>
        <Select
          labelId={fieldKey}
          id={fieldKey}
          defaultValue={defaultValue}
          label={formFieldJA(fieldKey)}
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
