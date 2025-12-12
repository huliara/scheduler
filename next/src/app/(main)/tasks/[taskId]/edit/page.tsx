"use client";
import * as React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import axios, { fetcher } from "@/axios";
import { TaskResponse } from "@/types/TaskType";
import useSWR from "swr";
import { TaskForm } from "@/components/form/TaskForm";
import { useSnackbarContext } from "@/components/provider/SnackBar";
import Link from "next/link";

export default function TaskEdit({ params }: { params: { taskId: string } }) {
  const { showSnackbar } = useSnackbarContext();
  const [subtasks, setSubtasks] = React.useState<string[]>([]);
  const { data, error, isLoading, mutate } = useSWR<TaskResponse>(
    `/tasks/${params.taskId}`,
    fetcher
  );
  React.useEffect(() => {
    if (!data) return;
    setSubtasks(data.subtasks);
  }, [data]);
  if (!data) return <div>no data</div>;
  if (error) return <div>error</div>;
  if (isLoading) return <div>loading...</div>;

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    axios
      .patch(`/tasks/${params.taskId}`, {
        name: data.get("name"),
        subtasks: subtasks,
        max_worker: data.get("max_worker"),
        min_worker: data.get("min_worker"),
        exp_worker: data.get("exp_worker"),
        wage: data.get("point"),
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

  return (
    <Container component="main" maxWidth="xs">
      <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
        <Typography component="h1" variant="h5">
          仕事を編集
        </Typography>
        <TaskForm data={data} subtasks={subtasks} setSubtasks={setSubtasks} />
      </Box>
      <Link href={`/tasks`}>一覧へ戻る</Link>
    </Container>
  );
}
