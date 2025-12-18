"use client";
import useSWR from "swr";
import { GroupUserResponse } from "@/types/GroupUser";
import {
  Button,
  Checkbox,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import axios, { fetcher } from "@/axios";
import { use } from "react";

export default function MemberList({
  params,
}: {
  params: Promise<{ groupId: string }>;
}) {
  const groupId = use(params).groupId;
  const { data, error, isLoading, mutate } = useSWR<{
    users: GroupUserResponse[];
  }>(`/groups/${groupId}/members`, fetcher);
  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;

  const handleUserActivate = (userId: string, activate: boolean) => {
    axios
      .post(
        `/groups/${groupId}/members/${userId}/activate&activate=${activate}`
      )
      .then((res) => {
        mutate();
      })
      .catch((error) => {});
  };

  const handleUserRemove = (userId: string) => {
    axios
      .delete(`/groups/${groupId}/members/${userId}`)
      .then((res) => {
        mutate();
      })
      .catch((error) => {});
  };

  return (
    <>
      <Typography component="h1" variant="h5">
        ユーザー一覧
      </Typography>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>ユーザー名</TableCell>
            <TableCell>部屋番号</TableCell>
            <TableCell>ポイント</TableCell>
            <TableCell>承認</TableCell>
            <TableCell></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.users
            .sort((a, b) => a.point - b.point)
            .map((user) => {
              return (
                <TableRow key={user.id}>
                  <TableCell>{user.name}</TableCell>
                  <TableCell>{user.room_number}</TableCell>
                  <TableCell>{user.point}</TableCell>
                  <TableCell>
                    <Checkbox
                      checked={user.is_active}
                      onClick={() =>
                        handleUserActivate(user.id, !user.is_active)
                      }
                    />
                  </TableCell>
                  <TableCell>
                    <Button
                      onClick={() => {
                        handleUserRemove(user.id);
                      }}
                    >
                      除外
                    </Button>
                  </TableCell>
                </TableRow>
              );
            })}
        </TableBody>
      </Table>
    </>
  );
}
