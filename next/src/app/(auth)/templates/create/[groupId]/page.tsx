"use client";
import axios, { fetcher } from "@/axios";
import { TemplateSlot } from "@/types/TemplateType";
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
import { useRouter } from "next/navigation";
import { TemplateSlotForm } from "@/components/form/TemplateAddSlotForm";
import useSWR from "swr";
import { Base } from "@/types/Base";
import { getFieldURL } from "@/utils/types";
import { ErrorPage } from "@/components/pages/ErrorPage";
import { LoadingPage } from "@/components/pages/LoadingPage";

export default function TemplateCreate({ groupId }: { groupId: string }) {
  const [slots, setSlots] = React.useState<TemplateSlot[]>([]);
  const [name, setName] = React.useState("");
  const {
    data: tasks,
    error,
    isLoading,
  } = useSWR<Base[]>(getFieldURL("task_id", `group_id=${groupId}`), fetcher);

  if (error) return <ErrorPage />;
  if (isLoading || !tasks) return <LoadingPage />;

  const defaultValue = {
    task_id: "",
    date_from_start: 0,
    start_time: "08:00",
  };

  const router = useRouter();

  const handleTaskRemove = (slot: TemplateSlot) => {
    setSlots(slots.filter((s) => s !== slot));
  };

  const handleTaskAdd = (slot: TemplateSlot) => {
    if (
      !slots.some(
        (current) =>
          current.task_id === slot.task_id &&
          current.date_from_start === slot.date_from_start &&
          current.start_time === slot.start_time
      )
    ) {
      setSlots([...slots, slot]);
    }
  };

  const handleSubmit = () => {
    axios
      .post(`/templates`, {
        name: name,
        slots: slots.map((slot) => {
          return {
            task_id: slot.task_id,
            date_from_start: slot.date_from_start,
            start_time: slot.start_time,
          };
        }),
        group_id: groupId,
      })

      .then((response) => {
        router.push(`/templates`);
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
      <TemplateSlotForm
        groupId={groupId}
        defaultValue={defaultValue}
        handleSubmit={handleTaskAdd}
      />
      <Button variant="contained" onClick={handleSubmit} sx={{ mt: 3 }}>
        作成
      </Button>
      <Grid container spacing={2}>
        {new Array(
          slots.length > 0
            ? slots
                .map((slot) => slot.date_from_start)
                .reduce((a, b) => Math.max(a, b)) + 1
            : 0
        )
          .fill(0)
          .map((_, i) => (
            <Grid key={i}>
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
                    {slots
                      .filter((slot) => slot.date_from_start === i)
                      .sort((a, b) => a.start_time.localeCompare(b.start_time))
                      .map((slot, index) => (
                        <TableRow key={index}>
                          <TableCell>
                            {
                              tasks.find((task) => task.id === slot.task_id)
                                ?.name
                            }
                          </TableCell>
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
