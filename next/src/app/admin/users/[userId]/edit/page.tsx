"use client";
import * as React from "react";
import axios from "@/axios";
import CssBaseline from "@mui/material/CssBaseline";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import Grid from "@mui/material/Grid";
import TextField from "@mui/material/TextField";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import Button from "@mui/material/Button";
import useSWR from "swr";
import { fetcher } from "@/axios";
import { UserDetailResponse } from "@/types/UserType";
export default function AdminUserEdit({
  params,
}: {
  params: { userId: string };
}) {
  const { data, error, isLoading } = useSWR<UserDetailResponse>(
    `/admin/users/${params.userId}`,
    fetcher
  );
  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    axios
      .patch(`/admin/users/${params.userId}`, {
        name: data.get("name"),
        room_number: data.get("room_number"),
        is_active: data.get("is_active") ? false : true,
        is_admin: data.get("is_admin") ? true : false,
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
          ユーザーを編集
        </Typography>
        <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <TextField
                autoComplete="given-name"
                name="name"
                required
                fullWidth
                id="name"
                label="名前"
                autoFocus
                defaultValue={data.name}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                required
                fullWidth
                id="room_number"
                label="部屋番号"
                name="room_number"
                autoComplete="room_number"
                defaultValue={data.room_number}
              />
            </Grid>
            <Grid item xs={12}>
              <FormControlLabel
                control={
                  <Checkbox
                    id="is_active"
                    name="is_active"
                    defaultChecked={!data.is_active}
                    inputProps={{ "aria-label": "controlled" }}
                  />
                }
                label="休寮中"
              />
            </Grid>
            <Grid item xs={12}>
              <FormControlLabel
                control={
                  <Checkbox
                    id="is_admin"
                    name="is_admin"
                    defaultChecked={data.is_admin}
                    inputProps={{ "aria-label": "controlled" }}
                  />
                }
                label="管理者にする"
              />
            </Grid>
          </Grid>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            保存
          </Button>{" "}
        </Box>
      </Box>
    </Container>
  );
}
