"use client";
import { Theme, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import OutlinedInput from "@mui/material/OutlinedInput";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select, { SelectChangeEvent } from "@mui/material/Select";
import Chip from "@mui/material/Chip";
import { Base, RequestType } from "@/types/Base";
import { getFieldJA, RequestFieldKeys, _fieldURL } from "@/utils/types";
import useSWR from "swr";
import { fetcher } from "@/axios";
const ITEM_HEIGHT = 48;
const ITEM_PADDING_TOP = 8;
const MenuProps = {
  PaperProps: {
    style: {
      maxHeight: ITEM_HEIGHT * 4.5 + ITEM_PADDING_TOP,
      width: 250,
    },
  },
};

function getStyles(name: string, personName: readonly string[], theme: Theme) {
  return {
    fontWeight:
      personName.indexOf(name) === -1
        ? theme.typography.fontWeightRegular
        : theme.typography.fontWeightMedium,
  };
}

export const ControlledMultiSelectField = ({
  fieldKey,
  value,
  setFormValue,
}: {
  fieldKey: RequestFieldKeys;
  value: string[];
  setFormValue: React.Dispatch<React.SetStateAction<RequestType | undefined>>;
}) => {
  const theme = useTheme();
  const { data, error, isLoading } = useSWR<Base[]>(
    _fieldURL(fieldKey),
    fetcher
  );
  const handleChange = (event: SelectChangeEvent<typeof value>) => {
    const {
      target: { value },
    } = event;
    // On autofill we get a stringified value.
    setFormValue(
      (prev) =>
        ({
          ...prev,
          [fieldKey]: typeof value === "string" ? value.split(",") : value,
        } as RequestType)
    );
  };

  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;

  return (
    <div>
      <FormControl sx={{ m: 1, width: 300 }}>
        <InputLabel id={fieldKey + "-label"}>{getFieldJA(fieldKey)}</InputLabel>
        <Select
          labelId={fieldKey + "-label"}
          id={fieldKey}
          name={fieldKey}
          multiple
          value={value}
          onChange={handleChange}
          input={<OutlinedInput id={fieldKey} label={getFieldJA(fieldKey)} />}
          renderValue={(selected) => (
            <Box sx={{ display: "flex", flexWrap: "wrap", gap: 0.5 }}>
              {selected.map((value) => {
                const tagname = data.find((tag) => tag.id === value)!.name;
                return <Chip key={value} label={tagname} />;
              })}
            </Box>
          )}
          MenuProps={MenuProps}
        >
          {data.map((tag) => (
            <MenuItem
              key={tag.id}
              value={tag.id}
              style={getStyles(tag.name, value, theme)}
            >
              {tag.name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </div>
  );
};
