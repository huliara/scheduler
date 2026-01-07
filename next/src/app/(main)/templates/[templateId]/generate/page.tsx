"use client";
import axios from "@/axios";
import { UncontrolledFormField } from "@/components/field/UncontrolledFields";
import { Field } from "@/utils/types";
import { Box, Button, Container, Grid, Typography } from "@mui/material";
import dayjs from "dayjs";
import { useRouter } from "next/navigation";
import React, { use } from "react";

export default function GenerateFromTemplateForm({
  params,
}: {
  params: Promise<{ templateId: string }>;
}) {
  const router = useRouter();
  const templateId = use(params).templateId;
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    axios
      .post(`/templates/${templateId}/generate`, {
        start_day: data.get("start_day"),
        add_default_worker: data.get("add_default_worker") === "on",
      })
      .then((res) => {
        router.push("/");
      })
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
            <Grid>
              <UncontrolledFormField
                fieldKey="start_day"
                fieldType={Field.DATE}
                defaultValue={dayjs().format("YYYY-MM-DD")}
              />
            </Grid>
            <Grid>
              <UncontrolledFormField
                fieldKey="add_default_worker"
                fieldType={Field.CheckBox}
                defaultValue={true}
              />
            </Grid>
          </Grid>
          <Button
            type="submit"
            fullWidth
            variant="contained"
            sx={{ mt: 3, mb: 2 }}
          >
            募集
          </Button>
        </Box>
      </Box>
    </Container>
  );
}
