"use client";
import axios, { fetcher } from "@/axios";
import useSWR from "swr";
import {
  TaskResponse,
  TemplateTask,
  TemplateTaskResponse,
} from "@/types/ResponseType";
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
  TextField,
  Typography,
} from "@mui/material";
import React from "react";
import { TemplateAddTaskFields } from "@/components/form/TemplateAddFields";
import { useRouter } from "next/navigation";
export default function TemplateCreate({
  params,
}: {
  params: { groupId: string; templateId: string };
}) {
  const {
    data: taskData,
    error: taskError,
    isLoading: taskIsLoading,
  } = useSWR<TaskResponse>(`/${params.groupId}/task_details/`, fetcher);
  const [data, setTasks] = React.useState<TemplateTask[]>([]);
  const [name, setName] = React.useState("");
  const [stateField, setTemplateTask] = React.useState<
    TemplateTaskResponse | undefined
  >({
    id: "",
    date_from_start: 0,
    start_time: "08:00",
    task_id: "",
    name: "",
  });
  const router = useRouter();

  if (taskError) return <div>error</div>;
  if (taskIsLoading) return <div>loading...</div>;
  if (!taskData) return <div>no data</div>;

  const handleTaskRemove = (slot: TemplateTask) => {
    setTasks(data.filter((s) => s !== slot));
  };

  const handleTaskAdd = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const form_data = new FormData(event.currentTarget);
    if (!stateField) return;
    const task_id = stateField.task_id;
    const task = {
      id: task_id,
      name: taskData.tasks.find((task) => task.id === task_id)?.name as string,
      date_from_start: Number(form_data.get("date_from_start")) - 1,
      start_time: form_data.get("start_time") as string,
      end_time: form_data.get("end_time") as string,
    };
    setTasks([...data, task]);
  };

  const handleSubmit = () => {
    console.log(data);

    axios
      .post(`${params.groupId}/templates`, {
        name: name,
        slots: data.map((task) => {
          return {
            taskdetail_id: task.id,
            date_from_start: task.date_from_start,
            start_time: task.start_time,
          };
        }),
      })
      .then((response) => {
        router.push(`/${params.groupId}/templates`);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <>
      <Typography variant="h4" component="h1" gutterBottom>
        テンプレートを新規作成
      </Typography>
      <Box component="form" noValidate autoComplete="off">
        <TextField
          id="template_name"
          label="テンプレート名"
          value={name}
          onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
            setName(event.target.value);
          }}
        />
      </Box>
      <Box
        component="form"
        noValidate
        onSubmit={handleTaskAdd}
        sx={{ mt: 3 }}
        maxWidth={500}
      >
        {stateField && (
          <TemplateAddTaskFields
            templateTask={stateField}
            buttonLabel="追加"
            tasks={taskData.tasks.map((task) => {
              return { id: task.id, name: task.name };
            })}
            setTemplateTask={setTemplateTask}
          />
        )}{" "}
        <Button fullWidth variant="contained" onClick={handleSubmit}>
          作成
        </Button>
      </Box>
      <Grid container spacing={2}>
        {new Array(
          data.length > 0
            ? data
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
                      <TableCell></TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {data
                      .filter((slot) => slot.date_from_start === i)
                      .sort((a, b) => a.start_time.localeCompare(b.start_time))
                      .map((slot, index) => (
                        <TableRow key={index}>
                          <TableCell>{slot.name}</TableCell>
                          <TableCell>{slot.start_time}</TableCell>
                          <TableCell>
                            <Button onClick={() => handleTaskRemove(slot)}>
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
