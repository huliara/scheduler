"use client";
import * as React from "react";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import axios, { fetcher } from "@/axios";
import useSWR from "swr";
import { UserDetailResponse } from "@/types/UserType";
import { UncontrolledForm } from "@/components/form/UncontrolledForm";
import { LoadingPage } from "@/components/pages/LoadingPage";

export default function ProfileEdit() {
  const { data: user } = useSWR<UserDetailResponse>("/user", fetcher);

  if (!user) {
    return <LoadingPage />;
  }

  const defaultData = {
    name: user.name,
    password: "",
    room_number: user.room_number,
    exp_tasks: user.exp_tasks.map((task) => task.id),
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    axios
      .patch("/user/profile", {
        name: data.get("name"),
        room_number: data.get("room_number"),
        exp_tasks: data.get("exp_tasks"),
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
          プロフィールを変更
        </Typography>
        <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <Grid container spacing={2}>
            <UncontrolledForm data={defaultData} />
          </Grid>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            保存
          </Button>
        </Box>
      </Box>
    </Container>
  );
}
