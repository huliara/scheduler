"use client";
import * as React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import axios, { fetcher } from "@/axios";
import { TaskResponse } from "@/types/TaskType";
import useSWR from "swr";
import { TaskDetailForm } from "@/components/form/TaskDetailForm";
import { useSnackbarContext } from "@/components/provider/SnackBar";
import Link from "next/link";
import { permission } from "process";

export default function TaskEdit({
  params,
}: {
  params: { groupId: string; taskId: string };
}) {
  const { showSnackbar } = useSnackbarContext();
  const [subtasks, setSubtasks] = React.useState<string[]>([]);
  const { data, error, isLoading, mutate } = useSWR<TaskResponse>(
    `/${params.groupId}/task_details/${params.taskId}`,
    fetcher
  );
  console.log(data);
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
      .patch(`${params.groupId}/task_details/${params.taskId}`, {
        name: data.get("name"),
        subtasks: subtasks,
        max_worker: data.get("max_worker_num"),
        min_worker: data.get("min_worker_num"),
        exp_worker: data.get("exp_worker_num"),
        wage: data.get("point"),
        duration: parseInt(data.get("duration") as string) * 60,
        permission: [],
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
        <TaskDetailForm
          data={data}
          subtasks={subtasks}
          setSubtasks={setSubtasks}
        />
      </Box>
      <Link href={`/${params.groupId}/task_details`}>一覧へ戻る</Link>
    </Container>
  );
}
