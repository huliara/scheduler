"use client";
import { GroupResponse } from "@/types/ResponseType";
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
import NextAuthProvider from "@/components/provider/NextAuth";
import Link from "next/link";

export default function Top() {
  return (
    <NextAuthProvider>
      <GroupList />
    </NextAuthProvider>
  );
}

const GroupList = () => {
  const { data, error, isLoading } = useSWR<{
    groups: GroupResponse[];
  }>("/groups", fetcher);
  const router = useRouter();
  if (error) return <div>Error</div>;
  if (isLoading) return <div>Loading...</div>;
  const joined_groups = data?.groups.filter((group) => group.role !== null);

  const irrelevant_groups = data?.groups.filter((group) => group.role == null);

  return (
    <>
      <Link href="/mypage">マイページ</Link>
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
            </ListItem>
          ))}
        </List>
      </Container>
    </>
  );
};
