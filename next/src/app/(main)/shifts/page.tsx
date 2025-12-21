"use client";
import useSWR from "swr";
import { ShiftResponse } from "@/types/ShiftType";
import { Button } from "@mui/material";
import { fetcher } from "@/axios";
import Link from "next/link";
import axios from "@/axios";
import { LoadingPage } from "@/components/pages/LoadingPage";
import { ErrorPage } from "@/components/pages/ErrorPage";
import DataLists from "@/components/list/DataLists";
export default function ShiftList() {
  const { data, error, mutate, isLoading } = useSWR<ShiftResponse[]>(
    `/shifts`,
    fetcher
  );
  if (error) return <ErrorPage />;
  if (!data || isLoading) return <LoadingPage />;

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
      <DataLists<ShiftResponse>
        dataName="shifts"
        targetField={["name", "start_time"]}
      />
      <Link href={`/shifts/create`}>新規作成</Link>
    </>
  );
}
