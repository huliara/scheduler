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
import { TemplateEditTaskForm } from "@/components/form/TemplateEditTaskForm";

export default function TemplateEdit({
  params,
}: {
  params: { groupId: string; templateId: string };
}) {
  const { data, error, isLoading, mutate } = useSWR<TemplateResponse>(
    `/${params.groupId}/templates/${params.templateId}`,
    fetcher
  );
  const [selectId, setId] = React.useState<string>();

  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;

  const handleTaskRemove = (templateTaskId: string) => {
    axios
      .delete(
        `/${params.groupId}/templates/${params.templateId}/tasks/${templateTaskId}`
      )
      .then((response) => {
        mutate();
      })
      .catch((err) => {});
  };

  const handleTaskAdd = (selectTemplateTask: TemplateTaskResponse) => {
    axios
      .post(`/${params.groupId}/templates/${params.templateId}/slots`, {
        date_from_start: Number(selectTemplateTask?.date_from_start),
        start_time: selectTemplateTask?.start_time,
        id: selectTemplateTask?.task_id,
      })
      .then((response) => {
        mutate();
      })
      .catch((err) => {});
  };

  const handleTaskEdit = (
    src: TemplateTaskResponse,
    dst: TemplateTaskResponse
  ) => {
    if (!dst) return;
    axios
      .patch(`/${params.groupId}/templates/${params.templateId}/slot`, {
        src: {
          taskdetail_id: src.task_id,
          date_from_start: Number(src.date_from_start),
          start_time: src.start_time,
        },
        dst: {
          taskdetail_id: dst.task_id,
          date_from_start: Number(dst.date_from_start),
          start_time: dst.start_time,
        },
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
      {selectId ? (
        <>
          {" "}
          <TemplateEditTaskForm
            groupId={params.groupId}
            handleSubmit={handleTaskEdit}
            templateTask={data.slots.find((slot) => selectId === slot.id)!}
            buttonTitle="変更を保存"
          />
        </>
      ) : (
        <TemplateAddTaskForm
          groupId={params.groupId}
          handleSubmit={handleTaskAdd}
          templateTask={{
            id: "",
            date_from_start: 0,
            start_time: "08:00",
            task_id: "",
            name: "",
          }}
          buttonTitle="新規追加"
        />
      )}
      {selectId ? (
        <Grid item xs={12}>
          <Button
            fullWidth
            variant="contained"
            onClick={() => setId(undefined)}
          >
            +新規追加
          </Button>
        </Grid>
      ) : (
        <></>
      )}
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
                        <TableRow key={index} selected={selectId === slot.id}>
                          <TableCell>{slot.name}</TableCell>
                          <TableCell>{slot.start_time}</TableCell>
                          <TableCell>
                            <Button
                              onClick={() => {
                                setId((prev) => {
                                  return slot.id;
                                });
                              }}
                            >
                              編集
                            </Button>
                          </TableCell>
                          <TableCell>
                            <Button
                              onClick={() => {
                                handleTaskRemove(slot.id);
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
