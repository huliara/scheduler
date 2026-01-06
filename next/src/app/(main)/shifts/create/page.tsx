"use client";
import * as React from "react";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import axios from "@/axios";
import { ShiftForm } from "@/components/form/ShiftForm";
import { useSnackbarContext } from "@/components/provider/SnackBar";

export default function ShiftCreate() {
  const { showSnackbar } = useSnackbarContext();

  const defaultData = {
    name: "",
    start_time: new Date().toISOString(),
    task_id: "",
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    axios
      .post(`/shifts`, {
        name: data.get("name"),
        start_time: new Date(data.get("start_time") as string).toISOString(),
        end_time: new Date(data.get("end_time") as string).toISOString(),
        task_id: data.get("task_id"),
      })
      .then((response) => {
        showSnackbar("success", "作成しました");
      })
      .catch((err) => {
        showSnackbar("error", "作成に失敗しました");
      });
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
        <Typography component="h1" variant="h5">
          仕事を作成
        </Typography>
        <ShiftForm data={defaultData} />
      </Box>
    </Container>
  );
}
