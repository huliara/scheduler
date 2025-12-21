"use client";
import { TaskResponse } from "@/types/TaskType";
import Link from "next/link";
import DataLists from "@/components/list/DataLists";
const TaskList = () => {
  return (
    <>
      <DataLists<TaskResponse>
        dataName="tasks"
        targetField={["name", "wage", "duration"]}
      />
      <Link href={`/tasks/create`}>新規作成</Link>
    </>
  );
};

export default TaskList;
