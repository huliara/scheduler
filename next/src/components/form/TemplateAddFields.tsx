import { Button, Grid, TextField } from "@mui/material";
import SelectField from "./SelectField";
import { ResponseBase, TemplateTaskResponse } from "@/types/ResponseType";

export const TemplateAddTaskFields = ({
  templateTask,
  buttonLabel,
  tasks,
  setTemplateTask,
}: {
  templateTask: TemplateTaskResponse;
  buttonLabel: string;
  tasks: ResponseBase[];
  setTemplateTask: React.Dispatch<
    React.SetStateAction<TemplateTaskResponse | undefined>
  >;
}) => {
  const setTaskId = (id: string) => {
    setTemplateTask({ ...templateTask, task_id: id });
  };
  return (
    <Grid container spacing={2}>
      <Grid item xs={12} sm={6}>
        <TextField
          required
          id="date_from_start"
          label="何日目"
          name="date_from_start"
          type="number"
          inputProps={{ min: 1, max: 100, step: 1 }}
          value={templateTask.date_from_start + 1}
          onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
            setTemplateTask({
              ...templateTask,
              date_from_start: parseInt(event.target.value) - 1,
            });
          }}
        />
      </Grid>
      <Grid item xs={12}>
        <TextField
          fullWidth
          required
          id="start_time"
          label="開始時刻"
          name="start_time"
          type="time"
          value={templateTask.start_time}
          onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
            setTemplateTask({
              ...templateTask,
              start_time: event.target.value,
            });
          }}
        />
      </Grid>
      <Grid item xs={12}>
        <SelectField
          data={tasks}
          title="仕事内容"
          id={templateTask.task_id}
          setData={setTaskId}
        />
      </Grid>
      <Button type="submit" variant="contained" sx={{ mt: 3, mb: 2 }}>
        {buttonLabel}
      </Button>
    </Grid>
  );
};
