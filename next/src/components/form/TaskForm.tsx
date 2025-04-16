import { ResponseBase, TaskResponse } from "@/types/ResponseType";
import { Grid } from "@mui/material";
import TextField from "@mui/material/TextField";
import Button from "@mui/material/Button";
import SelectField from "./SelectField";

type SlotRequest = {
  name: string;
  start_time: string;
  task_id: string;
};
export const TaskForm = ({
  data,
  tasks,
  task_id,
  setData,
}: {
  data: SlotRequest;
  tasks: ResponseBase[];
  task_id: string;
  setData: React.Dispatch<React.SetStateAction<string>>;
}) => {
  return (
    <Grid container spacing={2}>
      <Grid item xs={12}>
        <TextField
          autoComplete="given-name"
          name="name"
          required
          id="name"
          label="名前"
          autoFocus
          defaultValue={data.name}
        />
      </Grid>
      <Grid item xs={12}>
        <TextField
          fullWidth
          required
          id="start_time"
          label="開始時刻"
          name="start_time"
          type="datetime-local"
          defaultValue={data.start_time.slice(0, 16)}
        />
      </Grid>
      <Grid item xs={12}>
        <SelectField
          data={tasks}
          title="仕事内容"
          id={task_id}
          setData={setData}
        />
      </Grid>
      <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
        保存
      </Button>
    </Grid>
  );
};
