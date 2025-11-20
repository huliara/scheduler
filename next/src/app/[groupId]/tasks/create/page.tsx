"use client";
import * as React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import axios, { fetcher } from "@/axios";
import { ShiftResponse, TaskResponse } from "@/types/ResponseType";
import useSWR from "swr";
import { TaskForm } from "@/components/form/TaskForm";
import { useSnackbarContext } from "@/components/provider/SnackBar";

export default function SlotCreate({
  params,
}: {
  params: { groupId: string };
}) {
  const [task_id, setData] = React.useState("");
  const { showSnackbar } = useSnackbarContext();
  const {
    data: taskData,
    error: taskError,
    isLoading: taskIsLoading,
  } = useSWR<TaskResponse>(`/${params.groupId}/task_details/`, fetcher);
  if (taskError) return <div>error</div>;
  if (taskIsLoading) return <div>loading...</div>;
  if (!taskData) return <div>no data</div>;

  const slot_data = {
    id: "",
    name: "",
    start_time: new Date().toISOString(),
    creater_id: "",
    creater_name: "",
    assignees: [],
    task_id: "",
    task_name: "",
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    axios
      .post(`${params.groupId}/slots/`, {
        name: data.get("name"),
        start_time: new Date(data.get("start_time") as string).toISOString(),
        end_time: new Date(data.get("end_time") as string).toISOString(),
        task_id: task_id,
      })
      .then((response) => {
        showSnackbar("success", "作成しました");
      })
      .catch((err) => {
        showSnackbar("error", "作成に失敗しました");
      });
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
        <Typography component="h1" variant="h5">
          仕事を作成
        </Typography>
        <TaskForm
          data={slot_data}
          tasks={taskData.tasks.map((task) => {
            return { id: task.id, name: task.name };
          })}
          task_id={task_id}
          setData={setData}
        />
      </Box>
    </Container>
  );
}
