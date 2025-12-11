"use client";
import * as React from "react";
import axios from "@/axios";
import { AdminUserForm } from "@/components/form/AdminUserForm";
import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import Link from "next/link";

export default function AdminUserCreate() {
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    axios
      .post("/admin/users", {
        name: data.get("name"),
        password: data.get("password"),
        room_number: data.get("room_number"),
        is_admin: data.get('is_admin') ? true : false,
      })
      .then((response) => {})
      .catch((err) => {});
  };

  return (
    <Container component="main" maxWidth="xs">
      <CssBaseline />
      <Box
        sx={{
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography component="h1" variant="h5">
          ユーザーを新規作成
        </Typography>
        <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <AdminUserForm  />
        </Box>
      </Box>
        <Link href="/admin/users" >ユーザー一覧に戻る</Link>
    </Container>
  );
}
