"use client";
import useSWR from "swr";
import { TasksResponse } from "@/types/TaskType";
import axios, { fetcher } from "@/axios";
import { LoadingPage } from "@/components/pages/LoadingPage";
import { ErrorPage } from "@/components/pages/ErrorPage";
import { SchedulerList } from "@/components/list/List";
import { useRouter } from "next/router";
import { Typography } from "@mui/material";
export const GroupTaskList = ({
  groupName,
  groupId,
}: {
  groupName: string;
  groupId: string;
}) => {
  const { data, error, mutate, isLoading } = useSWR<TasksResponse>(
    `/tasks&group_id=${groupId}`,
    fetcher
  );
  const router = useRouter();
  if (error) return <ErrorPage />;
  if (!data || isLoading) return <LoadingPage />;

  const handleOnClick = (task_id: string) => {
    axios
      .delete(`/tasks/${task_id}`)
      .then((res) => {
        mutate();
      })
      .catch((err) => {});
  };

  const listvalues = data.map((task) => {
    return {
      id: task.id,
      name: task.name,
      wage: task.wage,
      duration: task.duration,
    };
  });

  const onClicks = [
    { action: (id: string) => router.push(`/tasks/${id}`), label: "詳細" },
    { action: (id: string) => router.push(`/tasks/${id}/edit`), label: "編集" },
    { action: (id: string) => handleOnClick(id), label: "削除" },
  ];

  return (
    <>
      <Typography variant="h4">{groupName}</Typography>
      <SchedulerList data={listvalues} onClicks={onClicks} />
    </>
  );
};
