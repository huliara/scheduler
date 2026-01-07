"use client";
import MenuItem from "@mui/material/MenuItem";
import { RequestFieldKeys, _fieldURL, getFieldURL } from "@/utils/types";
import useSWR from "swr";
import { Base } from "@/types/Base";
import { fetcher } from "@/axios";
import { TextField } from "@mui/material";

export const UncontrolledSelectField = ({
  fieldKey,
  defaultValue,
  url,
  params,
}: {
  fieldKey: RequestFieldKeys;
  defaultValue: string;
  url?: string;
  params?: string | null;
}) => {
  const fetchURL = url ?? getFieldURL(fieldKey, params);
  const { data, error, isLoading } = useSWR<Base[]>(fetchURL, fetcher);

  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;
  return (
    <TextField id={fieldKey} name={fieldKey} defaultValue={defaultValue} select>
      {data.map((data) => (
        <MenuItem key={data.id} value={data.id}>
          {data.name}
        </MenuItem>
      ))}
    </TextField>
  );
};
