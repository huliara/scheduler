"use client";
import { TaskResponse } from "@/types/TaskType";
import { fetcher } from "@/axios";
import { Typography } from "@mui/material";
import useSWR from "swr";
import { use } from "react";
export default function TaskDetail({
  params,
}: {
  params: Promise<{ taskId: string }>;
}) {
  const taskId = use(params).taskId;
  const { data, error, isLoading } = useSWR<TaskResponse>(
    `/tasks/${taskId}`,
    fetcher
  );

  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;
  const detail_text = data.subtasks.concat();

  return (
    <>
      <Typography variant="h4" component="div">
        {data.name}
      </Typography>
      <Typography variant="body1">仕事内容：{detail_text}</Typography>
      <Typography variant="body1">最大参加者数: {data.max_worker}</Typography>
      <Typography variant="body1">最低参加者数: {data.min_worker}</Typography>
      <Typography variant="body1">最低経験者数: {data.exp_worker}</Typography>
      <Typography variant="body1">ポイント: {data.wage}</Typography>
      <Typography variant="body1">作成者: {data.creater_name}</Typography>
    </>
  );
}
