"use client";
import { Container, Divider } from "@mui/material";
import axios, { fetcher } from "@/axios";
import useSWR from "swr";
import { useRouter } from "next/navigation";
import { GroupResponse } from "@/types/GroupType";
import Link from "next/link";
import { SchedulerList } from "@/components/list/List";

export default function GroupList() {
  const { data, error, mutate, isLoading } = useSWR<GroupResponse[]>(
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

  const irrelevant_groups = Array.from(
    new Set(data).difference(new Set(joined_groups))
  );

  const onClickJoin = (group_id: string) => {
    axios
      .post(`/groups/${group_id}/members/join`)
      .then((res) => mutate())
      .catch((err) => console.log(err));
  };

  return (
    <>
      <Container>
        <Divider>参加中のグループ</Divider>
        {
          <SchedulerList
            data={joined_groups.map((group) => {
              return {
                id: group.id,
                name: group.name,
              };
            })}
            onClicks={[
              {
                action: (id: string) => router.push(`/groups/${id}`),
                label: "移動",
              },
            ]}
          />
        }
      </Container>
      <Container>
        <Divider>他のグループ</Divider>
        <SchedulerList
          data={irrelevant_groups.map((group) => {
            return {
              id: group.id,
              name: group.name,
            };
          })}
          onClicks={[
            {
              action: (id: string) => onClickJoin(id),
              label: "参加",
            },
          ]}
        />
      </Container>
      <Link href={`/groups/create`}>新規作成</Link>
    </>
  );
}
