"use client";
import axios, { fetcher } from "@/axios";
import useSWR from "swr";
import { TemplateResponse, TemplateTaskResponse } from "@/types/ResponseType";
import {
  Box,
  Button,
  Grid,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import React from "react";
import { TemplateAddTaskForm } from "@/components/form/TemplateAddTaskForm";
import { TemplateNameForm } from "@/components/form/TemplateNameForm";

export default function TemplateEdit({
  params,
}: {
  params: { groupId: string; templateId: string };
}) {
  const { data, error, isLoading, mutate } = useSWR<TemplateResponse>(
    `/${params.groupId}/templates/${params.templateId}`,
    fetcher
  );

  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;

  const handleTaskRemove = (
    taskdetail_id: string,
    date_from_start: number,
    start_time: string
  ) => {
    axios
      .delete(`/${params.groupId}/templates/${params.templateId}/slots`, {
        data: {
          taskdetail_id: taskdetail_id,
          date_from_start: date_from_start,
          start_time: start_time,
        },
      })
      .then((response) => {
        mutate();
      })
      .catch((err) => {});
  };

  const handleTaskAdd = (selectTemplateTask: TemplateTaskResponse) => {
    axios
      .patch(`/${params.groupId}/templates/${params.templateId}/slots`, {
        date_from_start: Number(selectTemplateTask.date_from_start),
        start_time: selectTemplateTask.start_time,
        taskdetail_id: selectTemplateTask.taskdetail_id,
      })
      .then((response) => {
        mutate();
      })
      .catch((err) => {});
  };

  return (
    <>
      <Typography variant="h4" component="h1" gutterBottom>
        テンプレートを編集
      </Typography>
      <TemplateNameForm
        groupId={params.groupId}
        templateId={params.templateId}
        defaultName={data.name}
      />

      <TemplateAddTaskForm
        groupId={params.groupId}
        handleSubmit={handleTaskAdd}
        templateTask={{
          id: "",
          date_from_start: 0,
          start_time: "08:00",
          taskdetail_id: "",
          name: "",
        }}
        buttonTitle="新規追加"
      />

      <Grid container spacing={2}>
        {new Array(
          data.slots.length > 0
            ? data.slots
                .map((task) => task.date_from_start)
                .reduce((a, b) => Math.max(a, b)) + 1
            : 0
        )
          .fill(0)
          .map((_, i) => (
            <Grid item xs={12} key={i}>
              <Paper sx={{ p: 2, display: "flex", flexDirection: "column" }}>
                <Typography
                  component="h2"
                  variant="h6"
                  color="primary"
                  gutterBottom
                >
                  {i + 1}日目
                </Typography>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>名前</TableCell>
                      <TableCell>開始時刻</TableCell>
                      <TableCell>終了時刻</TableCell>
                      <TableCell></TableCell>
                      <TableCell></TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {data.slots
                      .filter((slot) => slot.date_from_start === i)
                      .sort((a, b) => a.start_time.localeCompare(b.start_time))
                      .map((slot, index) => (
                        <TableRow key={index}>
                          <TableCell>{slot.name}</TableCell>
                          <TableCell>{slot.start_time}</TableCell>
                          <TableCell>
                            <Button
                              onClick={() => {
                                handleTaskRemove(
                                  slot.taskdetail_id,
                                  slot.date_from_start,
                                  slot.start_time
                                );
                              }}
                            >
                              削除
                            </Button>
                          </TableCell>
                        </TableRow>
                      ))}
                  </TableBody>
                </Table>
              </Paper>
            </Grid>
          ))}
      </Grid>
    </>
  );
}
