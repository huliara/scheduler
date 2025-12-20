"use client";
import useSWR from "swr";
import { TemplateResponse } from "@/types/TemplateType";
import { fetcher } from "@/axios";
import Link from "next/link";
import { getGroupIds, handleOnClickDelete } from "@/utils/utils";
import { useRouter } from "next/navigation";
import { Typography } from "@mui/material";
import { SchedulerList } from "@/components/list/List";
export default function TemplateList() {
  const { data, error, mutate, isLoading } = useSWR<TemplateResponse[]>(
    `/templates`,
    fetcher
  );
  const router = useRouter();
  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;

  const groupIds = getGroupIds(data);

  const onClicks = [
    { action: (id: string) => router.push(`/templates/${id}`), label: "詳細" },
    {
      action: (id: string) => router.push(`/templates/${id}/generate`),
      label: "募集",
    },
    {
      action: (id: string) => handleOnClickDelete("templates", id, mutate()),
      label: "削除",
    },
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
            };
          });

        return (
          <div key={groupId}>
            <Typography variant="h5">{groupName}</Typography>
            <SchedulerList data={values} onClicks={onClicks} />
          </div>
        );
      })}
      <Link href={`/templates/create`}>新規作成</Link>
    </>
  );
}
