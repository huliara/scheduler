"use client";
import useSWR from "swr";
import { MemberResponse } from "@/types/GroupUser";
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
  const { data, error, isLoading, mutate } = useSWR<MemberResponse[]>(
    `/groups/${groupId}/members`,
    fetcher
  );
  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;

  const handleUserActivate = (userId: string, activate: boolean) => {
    axios
      .post(
        `/groups/${groupId}/members/${userId}/activate?activate=${
          activate ? "True" : "False"
        }`
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
            <TableCell>ポイント</TableCell>
            <TableCell>承認</TableCell>
            <TableCell></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data
            .sort((a, b) => a.point - b.point)
            .map((user) => {
              console.log(user.is_active);
              return (
                <TableRow key={user.user_id}>
                  <TableCell>{user.name}</TableCell>
                  <TableCell>{user.point}</TableCell>
                  <TableCell>
                    <Checkbox
                      checked={user.is_active}
                      onClick={() =>
                        handleUserActivate(user.user_id, !user.is_active)
                      }
                    />
                  </TableCell>
                  <TableCell>
                    <Button
                      onClick={() => {
                        handleUserRemove(user.user_id);
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
