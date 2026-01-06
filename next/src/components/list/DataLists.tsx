"use client";
import useSWR from "swr";
import { fetcher } from "@/axios";
import { LoadingPage } from "@/components/pages/LoadingPage";
import { ErrorPage } from "@/components/pages/ErrorPage";
import { SchedulerList } from "@/components/list/List";
import { useRouter } from "next/navigation";
import { Button, Typography } from "@mui/material";
import { getGroupIds, handleOnClickDelete, pick } from "@/utils/utils";
import { GroupDataType } from "@/types/Base";
import { Box } from "@mui/system";

type Props<T extends GroupDataType> = {
  dataName: "tasks" | "templates" | "shifts";
  targetField: (keyof T)[];
  addtionalActions?: { action: (id: string) => void; label: string }[];
  groupActions?: { action: (group_id: string) => void; label: string }[];
};

const DataLists = <T extends GroupDataType>(
  props: React.PropsWithChildren<Props<T>>
) => {
  const router = useRouter();
  const { data, error, mutate, isLoading } = useSWR<T[]>(
    `/${props.dataName}`,
    fetcher
  );
  if (error) return <ErrorPage />;
  if (!data || isLoading) return <LoadingPage />;

  const groupIds = getGroupIds(data);

  const onClicks = [
    {
      action: (id: string) => router.push(`/${props.dataName}/${id}`),
      label: "詳細",
    },
    {
      action: (id: string) => router.push(`/${props.dataName}/${id}/edit`),
      label: "編集",
    },
    {
      action: (id: string) => handleOnClickDelete(props.dataName, id, mutate),
      label: "削除",
    },
  ].concat(props.addtionalActions || []);

  return (
    <Box sx={{ padding: 2 }}>
      {groupIds.map((groupId) => {
        const groupName = data.find(
          (task) => task.group_id === groupId
        )?.group_name;

        const values = data
          .filter((one) => one.group_id === groupId)
          .map((one) => {
            const target = pick(one, props.targetField);
            const cleanedTarget = Object.fromEntries(
              Object.entries(target).map(([key, val]) => [
                key,
                val === null ? undefined : val,
              ])
            );
            return {
              ...cleanedTarget,
              id: one.id,
            };
          });

        return (
          <Box
            key={groupId}
            sx={{
              border: 1,
              borderRadius: 1,
              borderColor: "#ADE0EE",
              padding: 2,
              marginBottom: 4,
            }}
          >
            <Typography variant="h5">{groupName}</Typography>
            <SchedulerList data={values} onClicks={onClicks} />
            {props.groupActions &&
              props.groupActions.map((action) => {
                return (
                  <Button
                    key={action.label}
                    onClick={() => {
                      action.action(groupId);
                    }}
                  >
                    {action.label}
                  </Button>
                );
              })}
          </Box>
        );
      })}
    </Box>
  );
};

export default DataLists;
