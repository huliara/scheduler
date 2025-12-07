"use client";
import useSWR from "swr";
import { GroupUserResponse } from "@/types/GroupUser";
import {
  Button,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import axios, { fetcher } from "@/axios";

export default function UserList({ params }: { params: { groupId: string } }) {
  const { data, error, isLoading, mutate } = useSWR<{
    users: GroupUserResponse[];
  }>(`/${params.groupId}/members`, fetcher);
  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;

  const handleUserRemove = (userId: string) => {
    axios
      .delete(`${params.groupId}/members/${userId}`)
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
      <Button href={`/${params.groupId}/users/create`}>ユーザー追加</Button>
    </>
  );
}
