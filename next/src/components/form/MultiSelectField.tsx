import * as React from "react";
import { Theme, useTheme } from "@mui/material/styles";
import Box from "@mui/material/Box";
import OutlinedInput from "@mui/material/OutlinedInput";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import Chip from "@mui/material/Chip";
import { Base } from "@/types/Base";
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

export const MultiSelectField = ({
  fieldKey,
  defaultValue,
}: {
  fieldKey: RequestFieldKeys;
  defaultValue: string[];
}) => {
  const theme = useTheme();
  const { data, error, isLoading } = useSWR<Base[]>(
    _fieldURL(fieldKey),
    fetcher
  );

  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;

  return (
    <div>
      <FormControl sx={{ m: 1, width: 300 }}>
        <InputLabel id={fieldKey}>{getFieldJA(fieldKey)}</InputLabel>
        <Select
          labelId={fieldKey}
          id={fieldKey}
          multiple
          defaultValue={defaultValue}
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
              style={getStyles(tag.name, defaultValue, theme)}
            >
              {tag.name}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </div>
  );
};
