"use client";
import useSWR from "swr";
import { ResponseBase } from "@/types/ResponseType";
import { ShiftResponse } from "@/types/ShiftType";
import { UserResponse } from "@/types/UserType";
import { TaskResponse } from "@/types/TaskType";
import {
  Button,
  Grid,
  List,
  ListItem,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";
import axios, { fetcher } from "@/axios";
import Link from "next/link";
export default function AdminUserList({
  params,
}: {
  params: { groupId: string };
}) {
  const { data, error, isLoading } = useSWR<{ users: UserResponse[] }>(
    `/admin/users`,
    fetcher
  );
  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;

  return (
    <>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>ユーザー名</TableCell>
            <TableCell></TableCell>
            <TableCell></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.users.map((user) => {
            return (
              <TableRow key={user.id}>
                <TableCell>{user.name}</TableCell>
                <TableCell>
                  <Link href={`users/${user.id}/edit`}>編集</Link>
                </TableCell>
                <TableCell>
                  <Link href={`users/${user.id}/delete`}>削除</Link>
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </>
  );
}
