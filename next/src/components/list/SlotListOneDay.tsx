import * as React from "react";
import List from "@mui/material/List";
import { ListSubheader } from "@mui/material";

export default function SlotListOneDay({
  day,
  children,
}: {
  day: string;
  children: React.ReactNode;
}) {
  return (
    <List
      sx={{
        width: "100%",
        maxWidth: 360,
        bgcolor: "background.paper",
        position: "relative",
        overflow: "scroll",
        maxHeight: 500,
        "& ::-webkit-scrollbar": {
          display: "none",
        },
        "& :hover": {
          "::-webkit-scrollbar": {
            display: "inline",
          },
        },
      }}
    >
      <ListSubheader>{day}</ListSubheader>
      {children}
    </List>
  );
}
