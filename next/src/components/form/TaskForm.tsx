import { TaskRequest } from "@/types/TaskType";
import { Grid, Typography } from "@mui/material";
import Button from "@mui/material/Button";
import { Dispatch, SetStateAction, useState } from "react";
import { SchedulerForm } from "./Form";
import { MultiTextField } from "../field/MultiTextField";

export const TaskForm = ({
  data,
  subtasks,
  setSubtasks,
}: {
  data: TaskRequest;
  subtasks: string[];
  setSubtasks: Dispatch<SetStateAction<string[]>>;
}) => {
  const onAdd = (text: string) => {
    setSubtasks([...subtasks, text]);
  };
  const onDelete = (index: number) => {
    setSubtasks(subtasks.filter((_, i) => i !== index));
  };
  return (
    <Grid container spacing={2}>
      <SchedulerForm data={data} />
      <Typography variant="h6">サブタスク</Typography>
      <MultiTextField state={subtasks} onAdd={onAdd} onDelete={onDelete} />
      <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
        保存
      </Button>
    </Grid>
  );
};
