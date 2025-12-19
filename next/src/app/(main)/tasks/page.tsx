"use client";
import useSWR from "swr";
import { TaskResponse } from "@/types/TaskType";
import axios, { fetcher } from "@/axios";
import { LoadingPage } from "@/components/pages/LoadingPage";
import { ErrorPage } from "@/components/pages/ErrorPage";
import { SchedulerList } from "@/components/list/List";
import { useRouter } from "next/navigation";
import { Typography } from "@mui/material";
import Link from "next/link";
const TaskList = () => {
  const router = useRouter();
  const { data, error, mutate, isLoading } = useSWR<TaskResponse[]>(
    `/tasks`,
    fetcher
  );
  console.log(data);
  if (error) return <ErrorPage />;
  if (!data || isLoading) return <LoadingPage />;

  const groupIds = Array.from(new Set(data.map((task) => task.group_id)));

  const handleOnClick = (task_id: string) => {
    axios
      .delete(`/tasks/${task_id}`)
      .then((res) => {
        mutate();
      })
      .catch((err) => {});
  };

  const onClicks = [
    { action: (id: string) => router.push(`/tasks/${id}`), label: "詳細" },
    { action: (id: string) => router.push(`/tasks/${id}/edit`), label: "編集" },
    { action: (id: string) => handleOnClick(id), label: "削除" },
  ];

  return (
    <>
      {groupIds.map((groupId) => {
        const groupName = data.find(
          (task) => task.group_id === groupId
        )?.group_name;

        const values = data
          .filter((task) => task.group_id === groupId)
          .map((task) => {
            return {
              id: task.id,
              name: task.name,
              wage: task.wage,
              duration: task.duration,
            };
          });

        return (
          <>
            <Typography variant="h4">{groupName}</Typography>
            <SchedulerList data={values} onClicks={onClicks} />
          </>
        );
      })}
      <Link href={`/tasks/create`}>新規作成</Link>
    </>
  );
};

export default TaskList;
