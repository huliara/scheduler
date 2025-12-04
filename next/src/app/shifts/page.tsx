"use client";
import useSWR from "swr";
import { ShiftResponse } from "@/types/ShiftType";
import {
  Button,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";
import { fetcher } from "@/axios";
import Link from "next/link";
import axios from "@/axios";
export default function TaskList({ params }: { params: { groupId: string } }) {
  const { data, error, mutate, isLoading } = useSWR<{ tasks: ShiftResponse[] }>(
    `/${params.groupId}/tasks`,
    fetcher
  );
  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;
  console.log(data);
  const handleOnClick = (slot_id: string) => {
    axios
      .delete(`/${params.groupId}/tasks/${slot_id}`)
      .then((res) => {
        mutate();
      })
      .catch((err) => {});
  };
  const handleOnDeletePrune = () => {
    axios
      .delete(`/${params.groupId}/tasks`, {
        params: {
          expired: true,
        },
      })
      .then((res) => {
        mutate();
      })
      .catch((err) => {});
  };
  return (
    <>
      <Button
        onClick={() => {
          handleOnDeletePrune();
        }}
      >
        不要なシフトを削除
      </Button>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>仕事名</TableCell>
            <TableCell>開始時刻</TableCell>
            <TableCell></TableCell>
            <TableCell></TableCell>
            <TableCell></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.tasks.map((slot) => {
            const start_time = new Date(slot.start_time);
            return (
              <TableRow key={slot.id}>
                <TableCell>{slot.name}</TableCell>
                <TableCell>
                  {start_time.getMonth() + 1}月{start_time.getDate()}日{" "}
                  {start_time.toLocaleTimeString("ja-JP", {
                    hour: "numeric",
                    minute: "2-digit",
                    hour12: false,
                  })}
                </TableCell>
                <TableCell>
                  <Link href={`tasks/${slot.id}`}>詳細</Link>
                </TableCell>
                <TableCell>
                  <Link href={`tasks/${slot.id}/edit`}>編集</Link>
                </TableCell>
                <TableCell>
                  <Button
                    onClick={() => {
                      handleOnClick(slot.id);
                    }}
                  >
                    削除
                  </Button>
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
      <Link href={`/${params.groupId}/slots/create`}>新規作成</Link>
    </>
  );
}
