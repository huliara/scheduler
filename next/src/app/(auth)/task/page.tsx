"use client";
import useSWR from "swr";
import { TasksResponse } from "@/types/TaskType";
import {
  Button,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";
import axios, { fetcher } from "@/axios";
import Link from "next/link";
import { LoadingPage } from "@/components/pages/LoadingPage";
import { ErrorPage } from "@/components/pages/ErrorPage";
export default function TaskList() {
  const { data, error, mutate, isLoading } = useSWR<TasksResponse>(
    `/tasks`,
    fetcher
  );
  if (error) return <ErrorPage />;
  if (!data || isLoading) return <LoadingPage />;
  const handleOnClick = (task_id: string) => {
    axios
      .delete(`/tasks/${task_id}`)
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
                <Link href={`/tasks/${task.id}`}>詳細</Link>
              </TableCell>
              <TableCell>
                <Link href={`/tasks/${task.id}/edit`}>編集</Link>
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
      <Link href={`/tasks/create`}>新規作成</Link>
    </>
  );
}
