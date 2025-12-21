"use client";
import * as React from "react";

import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import axios, { fetcher } from "@/axios";
import { ShiftResponse } from "@/types/ShiftType";
import useSWR from "swr";
import { ShiftForm } from "@/components/form/ShiftForm";
import { use } from "react";
export default function ShiftEdit({
  params,
}: {
  params: Promise<{ shiftId: string }>;
}) {
  const shiftId = use(params).shiftId;
  const { data, error, isLoading } = useSWR<ShiftResponse>(
    `/shifts/${shiftId}`,
    fetcher
  );

  if (error) return <div>error</div>;
  if (!data || isLoading) return <div>no data</div>;

  const defaultValue = {
    name: data.name,
    start_time: data.start_time,
    task_id: data.task.id,
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    axios
      .patch(`/shifts/${shiftId}`, {
        name: data.get("name"),
        start_time: new Date(data.get("start_time") as string).toISOString(),
        task_id: data.get("task_id"),
      })
      .then((response) => {
        //mutate();
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
        <Typography component="h1" variant="h5">
          仕事を編集
        </Typography>
        <ShiftForm data={defaultValue} />
      </Box>
    </Container>
  );
}
