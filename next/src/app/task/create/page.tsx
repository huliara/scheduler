"use client";
import axios from "@/axios";
import { Container, Typography } from "@mui/material";
import Box from "@mui/material/Box";
import { TaskForm } from "@/components/form/TaskForm";
import { useSnackbarContext } from "@/components/provider/SnackBar";
import Link from "next/link";
import { useState } from "react";
export default function TaskCreateForm() {
  const { showSnackbar } = useSnackbarContext();
  const [subtasks, setSubtasks] = useState<string[]>([]);
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    axios
      .post(`/tasks`, {
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
        showSnackbar("success", "作成しました");
      })
      .catch((err) => {
        showSnackbar("error", "作成に失敗しました");
      });
  };

  const defaultData = {
    name: "",
    subtasks: [],
    max_worker: 1,
    min_worker: 1,
    exp_worker: 1,
    wage: 1,
    permissions: [],
    duration: 60,
    group_id: "",
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
      <Link href={`/tasks`}>一覧へ戻る</Link>
    </Container>
  );
}
