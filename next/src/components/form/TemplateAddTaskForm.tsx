"use client";
import useSWR from "swr";
import { Box } from "@mui/system";
import { TemplateAddTaskFields } from "./TemplateAddFields";
import { TemplateTaskResponse, TaskResponse } from "@/types/ResponseType";
import { useEffect, useState } from "react";
import { fetcher } from "@/axios";
export const TemplateAddTaskForm = ({
  groupId,
  handleSubmit,
  templateTask,
  buttonTitle,
}: {
  groupId: string;
  handleSubmit: (data: TemplateTaskResponse) => void;
  templateTask: TemplateTaskResponse;
  buttonTitle: string;
}) => {
  const {
    data: taskData,
    error: taskError,
    isLoading: taskIsLoading,
  } = useSWR<TaskResponse>(`/${groupId}/task_details/`, fetcher);
  const [formData, setTemplateTask] = useState<TemplateTaskResponse>();
  useEffect(() => {
    setTemplateTask(templateTask);
  }, [templateTask]);
  if (!formData) {
    return null;
  }

  if (taskError) return <div>error</div>;
  if (taskIsLoading) return <div>loading...</div>;
  if (!taskData) return <div>no data</div>;

  const handleOnClick = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    handleSubmit(formData);
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
    </Box>
  );
};
