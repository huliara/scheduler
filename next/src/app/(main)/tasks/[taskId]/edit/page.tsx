"use client";
import * as React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import axios, { fetcher } from "@/axios";
import { TaskRequest, TaskResponse } from "@/types/TaskType";
import useSWR from "swr";
import { useSnackbarContext } from "@/components/provider/SnackBar";
import Link from "next/link";
import { use } from "react";
import { permission } from "process";
import { Grid } from "@mui/system";
import { ControlledFormField } from "@/components/field/ControlledFields";
import { ControlledForm } from "@/components/form/ControlledForm";
import { MultiTextField } from "@/components/field/MultiTextField";
import { Button } from "@mui/material";

export default function TaskEdit({
  params,
}: {
  params: Promise<{ taskId: string }>;
}) {
  const taskId = use(params).taskId;
  const { showSnackbar } = useSnackbarContext();
  const [subtasks, setSubtasks] = React.useState<string[]>([]);
  const { data, error, isLoading, mutate } = useSWR<TaskResponse>(
    `/tasks/${taskId}`,
    fetcher
  );
  const [formValue, setFormValue] = React.useState<TaskRequest>();
  React.useEffect(() => {
    if (!data) return;
    setSubtasks(data.subtasks);
    setFormValue({
      name: data.name,
      subtasks: data.subtasks,
      max_worker: data.max_worker,
      min_worker: data.min_worker,
      exp_worker: data.exp_worker,
      wage: data.wage,
      permissions: [],
      duration: data.duration,
      group_id: data.group_id,
    });
  }, [data]);
  if (!data || !formValue) return <div>no data</div>;
  if (error) return <div>error</div>;
  if (isLoading) return <div>loading...</div>;

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    axios
      .patch(`/tasks/${taskId}`, {
        name: data.get("name"),
        subtasks: subtasks,
        max_worker: data.get("max_worker"),
        min_worker: data.get("min_worker"),
        exp_worker: data.get("exp_worker"),
        wage: data.get("wage"),
        duration: parseInt(data.get("duration") as string),
        permission: [],
        group_id: data.get("group_id"),
      })
      .then((response) => {
        mutate();
        showSnackbar("success", "編集しました");
      })
      .catch((err) => {
        showSnackbar("error", "編集に失敗しました");
      });
  };

  const onAdd = (text: string) => {
    setSubtasks([...subtasks, text]);
  };
  const onDelete = (index: number) => {
    setSubtasks(subtasks.filter((_, i) => i !== index));
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
        <Typography component="h1" variant="h5">
          仕事を編集
        </Typography>
        <Grid container spacing={2}>
          <ControlledForm data={formValue} setFormValue={setFormValue} />
          <Typography variant="h6">サブタスク</Typography>
          <MultiTextField state={subtasks} onAdd={onAdd} onDelete={onDelete} />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            保存
          </Button>
        </Grid>
      </Box>
      <Link href={`/tasks`}>一覧へ戻る</Link>
    </Container>
  );
}
