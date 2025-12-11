"use client";
import axios from "@/axios";
import { SchedulerForm } from "@/components/form/Form";
import { Box, Button, Grid, Typography } from "@mui/material";
import { Container } from "@mui/system";
import { FormEvent } from "react";

export default function Login() {
  const data = {
    name: "",
    password: "",
  };
  const signIn = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    await axios
      .post("/login", {
        headers: {
          "Content-Type": "application/json",
        },
        body: {
          user_name: formData.get("name"),
          password: formData.get("password"),
        },
      })
      .then((response) => {
        localStorage.setItem("accessToken", response.data.access_token);
        localStorage.setItem("id", response.data.id);
        localStorage.setItem("name", response.data.name);
        return { success: "success login" };
      })
      .catch(() => {
        return { error: "Invalid credentials" };
      });
    return { error: "Invalid credentials" };
  };
  return (
    <Box component="form" noValidate onSubmit={signIn}>
      <Container
        component="main"
        maxWidth="xs"
        sx={{
          mt: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography component="h1" variant="h5">
          ログイン
        </Typography>
        <Grid container spacing={2}>
          <SchedulerForm data={data} />
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            ログイン
          </Button>
        </Grid>
      </Container>
    </Box>
  );
}
