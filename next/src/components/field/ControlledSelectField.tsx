"use client";
import MenuItem from "@mui/material/MenuItem";
import { RequestFieldKeys, _fieldURL, getFieldURL } from "@/utils/types";
import useSWR from "swr";
import { Base, RequestType } from "@/types/Base";
import { fetcher } from "@/axios";
import { TextField } from "@mui/material";

export const ControlledSelectField = ({
  fieldKey,
  value,
  params,
  setFormValue,
}: {
  fieldKey: RequestFieldKeys;
  value: string;
  params?: string | null;
  setFormValue: React.Dispatch<React.SetStateAction<RequestType | undefined>>;
}) => {
  const { data, error, isLoading } = useSWR<Base[]>(
    getFieldURL(fieldKey, params),
    fetcher
  );

  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;
  const onChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const selectedValue = event.target.value;
    setFormValue(
      (prev) =>
        ({
          ...prev,
          [fieldKey]: selectedValue,
        } as RequestType)
    );
  };
  console.log(data);
  return (
    <TextField
      id={fieldKey}
      name={fieldKey}
      value={value}
      onChange={onChange}
      select
    >
      {data.map((data) => (
        <MenuItem key={data.id} value={data.id}>
          {data.name}
        </MenuItem>
      ))}
    </TextField>
  );
};
