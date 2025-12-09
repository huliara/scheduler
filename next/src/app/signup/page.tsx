"use client";
import * as React from "react";
import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import axios from "@/axios";
import { Button, Grid } from "@mui/material";
import { SchedulerForm } from "@/components/form/Form";

export default function SignUp() {
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    axios
      .post("/user", {
        name: data.get("name"),
        password: data.get("password"),
        room_number: data.get("room_number"),
        exp_tasks: data.get("exp_tasks"),
      })
      .then((response) => {})
      .catch((err) => {});
  };
  const defaultData = {
    name: "",
    password: "",
    room_number: "",
    exp_tasks: [],
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
          新規登録
        </Typography>
        <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <Grid container spacing={2}>
            <SchedulerForm data={defaultData} />
          </Grid>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            登録
          </Button>{" "}
        </Box>
      </Box>
    </Container>
  );
}
