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
import { LoadingPage } from "@/components/pages/LoadingPage";
import { ErrorPage } from "@/components/pages/ErrorPage";
import { getGroupIds, handleOnClickDelete } from "@/utils/utils";
import { useRouter } from "next/navigation";
export default function ShiftList() {
  const router = useRouter();
  const { data, error, mutate, isLoading } = useSWR<ShiftResponse[]>(
    `/shifts`,
    fetcher
  );
  if (error) return <ErrorPage />;
  if (!data || isLoading) return <LoadingPage />;

  const groupIds = getGroupIds(data);

  const onClicks = [
    { action: (id: string) => router.push(`/shifts/${id}`), label: "詳細" },
    {
      action: (id: string) => router.push(`/shifts/${id}/edit`),
      label: "編集",
    },
    {
      action: (id: string) => handleOnClickDelete("shifts", id, mutate),
      label: "削除",
    },
  ];

  const handleOnDeletePrune = () => {
    axios
      .delete(`/shifts`, {
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
          {data.map((shift) => {
            const start_time = new Date(shift.start_time);
            return (
              <TableRow key={shift.id}>
                <TableCell>{shift.name}</TableCell>
                <TableCell>
                  {start_time.getMonth() + 1}月{start_time.getDate()}日{" "}
                  {start_time.toLocaleTimeString("ja-JP", {
                    hour: "numeric",
                    minute: "2-digit",
                    hour12: false,
                  })}
                </TableCell>
                <TableCell>
                  <Link href={`shifts/${shift.id}`}>詳細</Link>
                </TableCell>
                <TableCell>
                  <Link href={`shifts/${shift.id}/edit`}>編集</Link>
                </TableCell>
                <TableCell>
                  <Button
                    onClick={() => {
                      handleOnClick(shift.id);
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
      <Link href={`/shifts/create`}>新規作成</Link>
    </>
  );
}
