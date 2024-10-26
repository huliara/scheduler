"use client";
import * as React from "react";

import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import axios, { fetcher } from "@/axios";
import { SlotResponse, TaskResponse } from "@/types/ResponseType";
import useSWR from "swr";
import { SlotForm } from "@/components/form/SlotForm";
import { FormBase } from "@/components/form/FormBase";

export default function SlotEdit({
  params,
}: {
  params: { groupId: string; slotId: string };
}) {
  const { data, error, isLoading } = useSWR<SlotResponse>(
    `/${params.groupId}/slots/${params.slotId}`,
    fetcher
  );
  const [task_id, setData] = React.useState<string>();
  const {
    data: taskData,
    error: taskError,
    isLoading: taskIsLoading,
  } = useSWR<{ tasks: TaskResponse[] }>(`/${params.groupId}/tasks/`, fetcher);

  React.useEffect(() => {
    if (!data) return;
    setData(data.task_id);
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
      .patch(`${params.groupId}/slots/${params.slotId}`, {
        name: data.get("name"),
        start_time: new Date(data.get("start_time") as string).toISOString(),
        task_id: task_id,
      })
      .then((response) => {
        //mutate();
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <FormBase
      title="募集を編集"
      param={`/${params.groupId}/slots`}
      handleSubmit={handleSubmit}
    >
      <SlotForm
        data={data}
        tasks={taskData.tasks.map((task) => {
          return { id: task.id, name: task.name };
        })}
        task_id={task_id}
        setData={setData}
      />
    </FormBase>
  );
}
