import { Grid } from "@mui/material";
import Button from "@mui/material/Button";
import { SchedulerForm } from "./Form";
import { ShiftRequest } from "@/types/ShiftType";

export const TaskForm = ({ data }: { data: ShiftRequest }) => {
  return (
    <Grid container spacing={2}>
      <SchedulerForm data={data} />
      <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
        保存
      </Button>
    </Grid>
  );
};
