"use client";
import axios from "@/axios";
import { Container, Typography } from "@mui/material";
import Box from "@mui/material/Box";
import { TaskForm } from "@/components/form/TaskForm";
import { useSnackbarContext } from "@/components/provider/SnackBar";
import Link from "next/link";
import { FormBase } from "@/components/form/FormBase";
export default function TaskCreateForm({
  params,
}: {
  params: { groupId: string };
}) {
  const { showSnackbar } = useSnackbarContext();
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    console.log(data.get("duration"));
    axios
      .post(`${params.groupId}/tasks/`, {
        name: data.get("name"),
        detail: data.get("detail"),
        max_worker_num: data.get("max_worker_num"),
        min_worker_num: data.get("min_worker_num"),
        exp_worker_num: data.get("exp_worker_num"),
        point: data.get("point"),
        duration: parseInt(data.get("duration") as string) * 60,
      })
      .then((response) => {
        showSnackbar("success", "作成しました");
      })
      .catch((err) => {
        showSnackbar("error", "作成に失敗しました");
      });
  };

  const defaultData = {
    id: "",
    name: "",
    detail: "",
    max_worker_num: 1,
    min_worker_num: 1,
    exp_worker_num: 1,
    point: 1,
    duration: 3600,
    creater_id: "",
    creater_name: "",
    group_id: params.groupId,
  };

  return (
    <FormBase
      title={"仕事を作成"}
      param={`/${params.groupId}/tasks`}
      handleSubmit={handleSubmit}
    >
      <TaskForm data={defaultData} />
    </FormBase>
  );
}
