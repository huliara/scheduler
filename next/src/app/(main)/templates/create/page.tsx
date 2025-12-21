"use client";
import { fetcher } from "@/axios";
import useSWR from "swr";
import { useRouter } from "next/navigation";
import { GroupResponse } from "@/types/GroupType";

import { SchedulerList } from "@/components/list/List";

export default function GroupList() {
  const { data, error, isLoading } = useSWR<GroupResponse[]>(
    "/groups",
    fetcher
  );
  const router = useRouter();
  if (error) return <div>Error</div>;
  if (isLoading) return <div>Loading...</div>;
  if (!data) return <div>No Data</div>;
  const joined_groups = data.filter((group) =>
    group.users
      .map((user) => user.user_id)
      .includes(localStorage.getItem("id") || "")
  );
  return (
    <SchedulerList
      data={joined_groups.map((group) => {
        return {
          id: group.id,
          name: group.name,
        };
      })}
      onClicks={[
        {
          action: (id: string) => router.push(`/templates/create/${id}`),
          label: "移動",
        },
      ]}
    />
  );
}
