import { TaskResponse } from "@/types/ResponseType";
import * as React from "react";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Link from "next/link";
import Typography from "@mui/material/Typography";
import { usePathname } from "next/navigation";

export const toDatetimeString = (time: string) => {
  return new Date(time).toLocaleString("ja-JP", {
    month: "2-digit",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });
};

const toDateString = (time: string) => {
  return new Date(time).toLocaleDateString("ja-JP", {
    month: "2-digit",
    day: "numeric",
  });
};

const toTimeString = (time: string) => {
  return new Date(time).toLocaleTimeString("ja-JP", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  });
};
export const SlotDisplayCardBase = ({
  slot,
  children,
  style,
}: {
  slot: TaskResponse;
  children: React.ReactNode;
  style: React.CSSProperties;
}) => {
  const path = usePathname();
  const startTimeString = toTimeString(slot.start_time);
  const endTimeString = toTimeString(slot.end_time);
  const dateString = toDateString(slot.start_time);
  const assignees = slot.workers.map((assignee) => assignee.name).join(", ");
  return (
    <Card sx={{ minWidth: 120 }} variant="outlined" style={style}>
      <CardContent>
        <Typography variant="h6" component="div">
          <Link href={path + "/tasks/" + slot.id}>{slot.name}</Link>
        </Typography>
        <Typography variant="body1">
          {dateString}: {startTimeString} 〜{endTimeString}
        </Typography>
        <Typography variant="body2">参加者:{assignees}</Typography>
      </CardContent>
      <CardActions>{children}</CardActions>
    </Card>
  );
};
