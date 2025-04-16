"use client";
import useSWR from "swr";
import { Box } from "@mui/system";
import { TemplateAddTaskFields } from "./TemplateAddFields";
import { TemplateTaskResponse, TaskDetailResponse } from "@/types/ResponseType";
import { useEffect, useState } from "react";
import { fetcher } from "@/axios";
export const TemplateEditTaskForm = ({
  groupId,
  handleSubmit,
  templateTask,
  buttonTitle,
}: {
  groupId: string;
  handleSubmit: (src: TemplateTaskResponse, dst: TemplateTaskResponse) => void;
  templateTask: TemplateTaskResponse;
  buttonTitle: string;
}) => {
  const {
    data: taskData,
    error: taskError,
    isLoading: taskIsLoading,
  } = useSWR<TaskDetailResponse>(`/${groupId}/task_details/`, fetcher);
  const [formData, setTemplateTask] = useState<TemplateTaskResponse>();
  let prev_slot = templateTask;
  useEffect(() => {
    setTemplateTask(templateTask);
    prev_slot = templateTask;
  }, [templateTask]);
  if (!formData) {
    return null;
  }

  if (taskError) return <div>error</div>;
  if (taskIsLoading) return <div>loading...</div>;
  if (!taskData) return <div>no data</div>;

  const handleOnClick = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    handleSubmit(prev_slot, formData);
  };

  return (
    <Box
      component="form"
      noValidate
      onSubmit={handleOnClick}
      sx={{ mt: 3 }}
      maxWidth={500}
    >
      <TemplateAddTaskFields
        buttonLabel={buttonTitle}
        templateTask={formData}
        setTemplateTask={setTemplateTask}
        tasks={taskData.tasks}
      />
      <li>{formData.task_id}</li>
      <li>{formData.date_from_start}</li>
      <li>{formData.start_time}</li>
    </Box>
  );
};
