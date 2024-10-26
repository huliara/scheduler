"use client";
import * as React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import axios, { fetcher } from "@/axios";
import { TaskResponse } from "@/types/ResponseType";
import useSWR from "swr";
import { TaskForm } from "@/components/form/TaskForm";
import { useSnackbarContext } from "@/components/provider/SnackBar";
import Link from "next/link";
import { FormBase } from "@/components/form/FormBase";

export default function TaskEdit({
  params,
}: {
  params: { groupId: string; taskId: string };
}) {
  const { showSnackbar } = useSnackbarContext();
  const { data, error, isLoading, mutate } = useSWR<TaskResponse>(
    `/${params.groupId}/tasks/${params.taskId}`,
    fetcher
  );
  if (error) return <div>error</div>;
  if (isLoading) return <div>loading...</div>;
  if (!data) return <div>no data</div>;

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);

    axios
      .patch(`${params.groupId}/tasks/${params.taskId}`, {
        name: data.get("name"),
        detail: data.get("detail"),
        max_worker_num: data.get("max_worker_num"),
        min_worker_num: data.get("min_worker_num"),
        exp_worker_num: data.get("exp_worker_num"),
        point: data.get("point"),
        duration: parseInt(data.get("duration") as string) * 60,
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
    <FormBase
      title="仕事を編集"
      param={`/${params.groupId}/tasks`}
      handleSubmit={handleSubmit}
    >
      <TaskForm data={data} />
    </FormBase>
  );
}
