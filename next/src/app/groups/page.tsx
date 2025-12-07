"use client";
import {
  Container,
  Divider,
  List,
  ListItem,
  ListItemButton,
  ListItemText,
} from "@mui/material";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward";
import axios, { fetcher } from "@/axios";
import React from "react";
import useSWR from "swr";
import { useRouter } from "next/navigation";
import { GroupResponse } from "@/types/GroupType";
import AddIcon from "@mui/icons-material/Add";

export default function GroupList() {
  const { data, error, isLoading } = useSWR<{
    groups: GroupResponse[];
  }>("/groups", fetcher);
  const router = useRouter();
  if (error) return <div>Error</div>;
  if (isLoading) return <div>Loading...</div>;
  if (!data) return <div>No Data</div>;
  const joined_groups = data.groups.filter((group) =>
    group.users
      .map((user) => user.id)
      .includes(localStorage.getItem("id") || "")
  );

  const irrelevant_groups = Array.from(
    new Set(data.groups).difference(new Set(joined_groups))
  );

  const onClickJoin = (group_id: string) => {
    axios
      .post(`/groups/${group_id}/members/join`)
      .then((res) => console.log(res))
      .catch((err) => console.log(err));
  };

  return (
    <>
      <Container>
        <Divider>参加中のグループ</Divider>
        <List>
          {joined_groups?.map((group) => (
            <ListItem key={group.id}>
              <ListItemText primary={group.name} />
              <ListItemButton>
                <ArrowForwardIcon
                  onClick={() => {
                    router.push(`/${group.id}/`);
                  }}
                />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Container>
      <Container>
        <Divider>他のグループ</Divider>
        <List>
          {irrelevant_groups?.map((group) => (
            <ListItem key={group.id}>
              <ListItemText primary={group.name} />
              <ListItemButton
                onClick={() => {
                  onClickJoin(group.id);
                }}
              >
                <AddIcon />
              </ListItemButton>
            </ListItem>
          ))}
        </List>
      </Container>
    </>
  );
}
