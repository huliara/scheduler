import * as React from "react";
import Button from "@mui/material/Button";
import Grid from "@mui/material/Grid";
import { UserRequest } from "@/types/UserType";
import { SchedulerForm } from "./Form";

export const UserForm = ({ data }: { data: UserRequest }) => {
  return (
    <Grid container spacing={2}>
      <SchedulerForm data={data} />
      <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
        登録
      </Button>
    </Grid>
  );
};
