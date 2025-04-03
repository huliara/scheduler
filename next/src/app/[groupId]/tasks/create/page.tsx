"use client";
import axios from "@/axios";
import { Container, Typography } from "@mui/material";
import Box from "@mui/material/Box";
import { TaskForm } from "@/components/form/TaskForm";
import { useSnackbarContext } from "@/components/provider/SnackBar";
import Link from "next/link";
import { useState } from "react";
export default function TaskCreateForm({
  params,
}: {
  params: { groupId: string };
}) {
  const { showSnackbar } = useSnackbarContext();
  const [subtasks, setSubtasks] = useState<string[]>([]);
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    console.log(data.get("duration"));
    axios
      .post(`${params.groupId}/task_details/`, {
        name: data.get("name"),
        subtasks: subtasks,
        max_worker: data.get("max_worker_num"),
        min_worker: data.get("min_worker_num"),
        exp_worker: data.get("exp_worker_num"),
        wage: data.get("point"),
        duration: parseInt(data.get("duration") as string),
        permission: [],
      })
      .then((response) => {
        showSnackbar("success", "作成しました");
      })
      .catch((err) => {
        showSnackbar("error", "作成に失敗しました");
      });
  };

  const defaultData = {
    id: "",
    name: "",
    detail: [],
    max_worker_num: 1,
    min_worker_num: 1,
    exp_worker_num: 1,
    point: 1,
    duration: 60,
    creater_id: "",
    creater_name: "",
    group_id: params.groupId,
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
        <Typography component="h1" variant="h5">
          仕事を新規作成
        </Typography>
        <TaskForm
          data={defaultData}
          subtasks={subtasks}
          setSubtasks={setSubtasks}
        />
      </Box>
      <Link href={`/${params.groupId}/tasks`}>一覧へ戻る</Link>
    </Container>
  );
}
