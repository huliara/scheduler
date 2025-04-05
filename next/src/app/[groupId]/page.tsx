"use client";
import {
  Container,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
} from "@mui/material";
import useSWR from "swr";
import { fetcher } from "@/axios";
import { GroupResponse } from "@/types/ResponseType";
import { useRouter } from "next/navigation";
export default function GroupHome({ params }: { params: { groupId: string } }) {
  const { data, error, isLoading } = useSWR<GroupResponse>(
    `/groups/${params.groupId}`,
    fetcher
  );

  const router = useRouter();
  if (error) return <div>Error</div>;
  if (isLoading) return <div>Loading...</div>;
  return (
    <>
      <h1>{data?.name}</h1>
      <List>
        <ListItem>
          <ListItemButton
            onClick={() => {
              router.push(`/${params.groupId}/tasks`);
            }}
          >
            仕事
          </ListItemButton>
        </ListItem>
        <ListItem>
          <ListItemButton
            onClick={() => {
              router.push(`/${params.groupId}/task_details`);
            }}
          >
            マニュアルなど
          </ListItemButton>
        </ListItem>
        <ListItem>
          <ListItemButton
            onClick={() => {
              router.push(`/${params.groupId}/templates`);
            }}
          >
            募集テンプレート
          </ListItemButton>
        </ListItem>
        <ListItem>
          <ListItemButton
            onClick={() => {
              router.push(`/${params.groupId}/users`);
            }}
          >
            ユーザー
          </ListItemButton>
        </ListItem>
      </List>
    </>
  );
}
