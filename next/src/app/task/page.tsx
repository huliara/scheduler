"use client";
import useSWR from "swr";
import { TasksResponse } from "@/types/TaskType";
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
export default function TaskList({ params }: { params: { groupId: string } }) {
  const { data, error, mutate, isLoading } = useSWR<TasksResponse>(
    `/${params.groupId}/task_details`,
    fetcher
  );
  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;
  const handleOnClick = (task_id: string) => {
    axios
      .delete(`/${params.groupId}/task_details/${task_id}`)
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
            <TableCell>仕事名</TableCell>
            <TableCell>ポイント</TableCell>
            <TableCell>所要時間(分)</TableCell>
            <TableCell></TableCell>
            <TableCell></TableCell>
            <TableCell></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.tasks.map((task) => (
            <TableRow key={task.id}>
              <TableCell>{task.name}</TableCell>
              <TableCell>{task.wage}</TableCell>
              <TableCell>{task.duration}</TableCell>
              <TableCell>
                <Link href={`/${params.groupId}/task_details/${task.id}`}>
                  詳細
                </Link>
              </TableCell>
              <TableCell>
                <Link href={`/${params.groupId}/task_details/${task.id}/edit`}>
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
      <Link href={`/${params.groupId}/task_details/create`}>新規作成</Link>
    </>
  );
}
