"use client";
import { SlotResponse } from "@/types/ResponseType";
import useSWR from "swr";
import { fetcher } from "@/axios";
import { Typography } from "@mui/material";
import Link from "next/link";
export default function SlotDetail({
  params,
}: {
  params: { groupId: string; slotId: string };
}) {
  const { data, error, isLoading } = useSWR<SlotResponse>(
    `/${params.groupId}/slots/${params.slotId}`,
    fetcher
  );

  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;

  const start_time = new Date(data.start_time);
  const end_time = new Date(data.end_time);

  return (
    <>
      <Typography variant="h4" component="div">
        {data.name}
      </Typography>
      <Typography variant="body1">
        開始時刻: {start_time.getMonth() + 1}月{start_time.getDate()}日{" "}
        {start_time.getHours()}:{start_time.getMinutes()}
      </Typography>
      <Typography variant="body1">
        終了時刻: {end_time.getMonth() + 1}月{end_time.getDate()}日{" "}
        {end_time.getHours()}:{end_time.getMinutes()}
      </Typography>
      <Typography variant="body1">
        仕事内容:
        <Link href={`/${params.groupId}/task_details/${data.taskdetail_id}`}>
          {data.taskdetail_name}
        </Link>
      </Typography>
      <Typography variant="body1">
        参加者:{data.assignees.map((assignee) => assignee.name).join(", ")}
      </Typography>
      <Typography variant="body2">作成者:{data.creater_name}</Typography>
    </>
  );
}
