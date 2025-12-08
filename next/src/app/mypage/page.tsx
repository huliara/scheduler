"use client";
import {
  Chip,
  Divider,
  List,
  ListItem,
  ListItemText,
  Typography,
} from "@mui/material";
import useSWR from "swr";
import { fetcher } from "@/axios";
import { UserDetailResponse } from "@/types/UserType";
import PersonAddIcon from "@mui/icons-material/PersonAdd";
import Hiking from "@mui/icons-material/Hiking";
import Link from "next/link";
import { LoadingPage } from "@/components/pages/LoadingPage";

const style = {
  p: 0,
  width: "100%",
  maxWidth: "auto",
  borderRadius: 2,
  border: "1px solid",
  borderColor: "divider",
  backgroundColor: "background.paper",
};

export default function MyPage() {
  const { data: user } = useSWR<UserDetailResponse>("/user", fetcher);
  if (!user) {
    return <LoadingPage />;
  }

  return (
    <>
      <List sx={style}>
        <ListItem>
          <ListItemText primary={`名前: ${user.name}`} />
        </ListItem>
        <Divider component="li" />
        <ListItem>
          <ListItemText primary={`部屋番号: ${user.room_number}`} />
        </ListItem>
        <Divider component="li" />
        <ListItem>
          <ListItemText primary="所属団体" />
        </ListItem>
        <Divider component="li" />
        <ListItem>
          {user.groups.map((group) => (
            <Chip key={group.id} label={group.name} />
          ))}
        </ListItem>
        <Divider component="li" />
        <ListItem>
          <ListItemText primary="経験した仕事" />
        </ListItem>
        <Divider component="li" />
        <ListItem>
          {user.exp_tasks.map((task) => (
            <Chip key={task.id} label={task.name} />
          ))}
        </ListItem>
        <Divider component="li" />
        <ListItem>
          {user.is_active ? (
            <></>
          ) : (
            <>
              <Hiking />
              <Typography>休寮中</Typography>
            </>
          )}
        </ListItem>
      </List>
      <Link href={"/mypage/edit"}>編集</Link>
    </>
  );
}
