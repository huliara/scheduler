"use client";
import { ResponseBase } from "@/types/ResponseType";
import { ShiftResponse } from "@/types/ShiftType";
import { TaskResponse } from "@/types/TaskType";
import { fetcher } from "@/axios";
import { Typography } from "@mui/material";
import useSWR from "swr";
export default function TaskDetail({
  params,
}: {
  params: { groupId: string; taskId: string };
}) {
  const { data, error, isLoading } = useSWR<TaskResponse>(
    `/${params.groupId}/task_details/${params.taskId}`,
    fetcher
  );

  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;
  const detail_text = data.subtasks[0];

  return (
    <>
      <Typography variant="h4" component="div">
        {data.name}
      </Typography>
      <Typography variant="body1">仕事内容：{detail_text}</Typography>
      <Typography variant="body1">
        最大参加者数: {data.max_worker_num}
      </Typography>
      <Typography variant="body1">
        最低参加者数: {data.min_worker_num}
      </Typography>
      <Typography variant="body1">
        最低経験者数: {data.exp_worker_num}
      </Typography>
      <Typography variant="body1">ポイント: {data.point}</Typography>
      <Typography variant="body1">作成者: {data.creater_name}</Typography>
    </>
  );
}
