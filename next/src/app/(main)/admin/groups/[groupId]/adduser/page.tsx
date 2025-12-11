"use client";
import useSWR from "swr";
import axios, { fetcher } from "@/axios";
import { UsersResponse } from "@/types/UserType";
import {
  Box,
  Table,
  TableHead,
  TableCell,
  TableBody,
  TableRow,
  Button,
  Checkbox,
} from "@mui/material";
import { useState } from "react";

export default function AddUserForm({
  params,
}: {
  params: { groupId: string };
}) {
  const { data, error, mutate, isLoading } = useSWR<UsersResponse>(
    `/admin/users`,
    fetcher
  );
  const [userIds, setUserIds] = useState<string[]>([]);
  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;
  const onChecked = (id: string) => {
    if (userIds.includes(id)) {
      setUserIds(userIds.filter((userId) => userId !== id));
    } else {
      setUserIds([...userIds, id]);
    }
  };
  const handleAddUser = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    axios
      .post(`/${params.groupId}/members`, {
        user_ids: userIds,
      })
      .then((res) => {
        mutate();
      })
      .catch((err) => {
        console.log(err);
      });
  };
  return (
    <>
      <Box component="form" onSubmit={handleAddUser}>
        <Button type="submit">追加</Button>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>ユーザー名</TableCell>
              <TableCell>部屋番号</TableCell>
              <TableCell>休寮</TableCell>
              <TableCell></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {data.users.map((user) => (
              <TableRow key={user.id}>
                <TableCell>{user.name}</TableCell>
                <TableCell>{user.room_number}</TableCell>
                <TableCell>{user.is_active ? "" : "休寮"}</TableCell>
                <TableCell>
                  <Checkbox
                    value={user.id}
                    onChange={() => onChecked(user.id)}
                  />
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </Box>
    </>
  );
}
