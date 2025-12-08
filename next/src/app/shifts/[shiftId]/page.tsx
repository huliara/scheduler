import { ShiftResponse } from "@/types/ShiftType";
import useSWR from "swr";
import { fetcher } from "@/axios";
import { Typography } from "@mui/material";
import Link from "next/link";
import { LoadingPage } from "@/components/pages/LoadingPage";
import { ErrorPage } from "@/components/pages/ErrorPage";

export default function SlotDetail({
  params,
}: {
  params: { shiftId: string };
}) {
  const { data, error, isLoading } = useSWR<ShiftResponse>(
    `/shifts/${params.shiftId}`,
    fetcher
  );

  if (error) return <ErrorPage />;
  if (!data || isLoading) return <LoadingPage />;

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
        <Link href={`/tasks/${data.task.id}`}>{data.task.name}</Link>
      </Typography>
      <Typography variant="body1">
        参加者:{data.workers.map((assignee) => assignee.name).join(", ")}
      </Typography>
    </>
  );
}
