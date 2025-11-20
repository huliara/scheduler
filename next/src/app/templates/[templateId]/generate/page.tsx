'use client'
import axios from "@/axios";
import {
  Box,
  Button,
  Container,
  Grid,
  TextField,
  Typography,
} from "@mui/material";
import React from "react";

export default function GenerateFromTemplateForm({
  params,
}: {
  params: { groupId: string; templateId: string };
}) {
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    axios
      .post(`/${params.groupId}/templates/${params.templateId}/generate`, {
        start_day: data.get("start_day"),
      })
      .then((res) => {})
      .catch((err) => {});
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box
        sx={{
          marginTop: 8,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
        }}
      >
        <Typography component="h1" variant="h5">
          テンプレートからシフトを作成
        </Typography>
        <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                required
                id="start_day"
                label="開始日"
                name="start_day"
                type="date"
                defaultValue={new Date()
                  .toLocaleDateString("ja-JP", {
                    year: "numeric",
                    month: "2-digit",
                    day: "2-digit",
                  })
                  .replaceAll("/", "-")}
              />
            </Grid>
          </Grid>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            登録完了
          </Button>
        </Box>
      </Box>
    </Container>
  );
}
