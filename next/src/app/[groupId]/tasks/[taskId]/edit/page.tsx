"use client";
import * as React from "react";

import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import axios, { fetcher } from "@/axios";
import { TaskResponse, TaskDetailResponse } from "@/types/ResponseType";
import useSWR from "swr";
import { TaskForm } from "@/components/form/TaskForm";

export default function SlotEdit({
  params,
}: {
  params: { groupId: string; taskId: string };
}) {
  const { data, error, isLoading } = useSWR<TaskResponse>(
    `/${params.groupId}/tasks/${params.taskId}`,
    fetcher
  );
  const [task_id, setData] = React.useState<string>();
  const {
    data: taskData,
    error: taskError,
    isLoading: taskIsLoading,
  } = useSWR<{ tasks: TaskDetailResponse[] }>(
    `/${params.groupId}/task_details/`,
    fetcher
  );

  React.useEffect(() => {
    if (!data) return;
    setData(data.taskdetail.id);
  }, [data]);
  if (error | taskError) return <div>error</div>;
  if (isLoading || taskIsLoading) return <div>loading...</div>;
  if (!data || !taskData) return <div>no data</div>;
  if (!task_id) return <div>no task_id</div>;

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    console.log(data.get("start_time"));
    console.log(new Date(data.get("start_time") as string).toISOString());
    axios
      .patch(`${params.groupId}/tasks/${params.taskId}`, {
        name: data.get("name"),
        start_time: new Date(data.get("start_time") as string).toISOString(),
        taskdetail_id: task_id,
      })
      .then((response) => {
        //mutate();
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
        <Typography component="h1" variant="h5">
          仕事を編集
        </Typography>
        <TaskForm
          data={data}
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
