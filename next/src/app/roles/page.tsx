"use client";
import useSWR from "swr";
import { RolesResponse } from "@/types/ResponseType";
import {
  Button,
  Tab,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";
import axios, { fetcher } from "@/axios";
import Link from "next/link";
export default function RoleList({ params }: { params: { groupId: string } }) {
  const { data, error, mutate, isLoading } = useSWR<RolesResponse>(
    `/${params.groupId}/roles`,
    fetcher
  );
  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;
  const handleOnClick = (role_id: string) => {
    axios
      .delete(`/${params.groupId}/roles/${role_id}`)
      .then((res) => {
        mutate();
      })
      .catch((err) => {});
  };

  return (
    <>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>ロール名</TableCell>
            <TableCell></TableCell>
            <TableCell></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          <TableRow>
            <TableCell>グループ管理者</TableCell>
            <TableCell>編集不可</TableCell>
            <TableCell>削除不可</TableCell>
          </TableRow>
          {data.roles.map((task) => (
            <TableRow key={task.id}>
              <TableCell>{task.name}</TableCell>
              <TableCell>
                <Link href={`/${params.groupId}/roles/${task.id}/edit`}>
                  編集
                </Link>
              </TableCell>
              <TableCell>
                <Button
                  onClick={() => {
                    handleOnClick(task.id);
                  }}
                >
                  削除
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Link href={`/${params.groupId}/roles/create`}>新規作成</Link>
    </>
  );
}
