"use client";
import axios, { fetcher } from "@/axios";
import { UserResponse } from "@/types/ResponseType";
import { useEffect, useState } from "react";
import {
  Button,
  Card,
  CardActions,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import { ScrollMenu } from "react-horizontal-scrolling-menu";
import "react-horizontal-scrolling-menu/dist/styles.css";

export default function GroupUserAddPage({
  params,
}: {
  params: { groupId: string };
}) {
  const [postUsers, setPostUsers] = useState<UserResponse[]>([]);
  const [searchParam, setSearchParams] = useState<string>("");
  const [users, setUsers] = useState<UserResponse[]>([]);

  useEffect(() => {
    axios.get(`admin/users`).then((res) => {
      setUsers(res.data.users);
    });
  }, []);

  const handleAddUser = () => {
    axios
      .post(`/${params.groupId}/users`, {
        user_ids: postUsers.map((user) => user.id),
      })
      .then((res) => {})
      .catch((err) => {
        console.log(err);
      });
  };

  const UserCard = ({ user }: { user: UserResponse }) => {
    return (
      <Card sx={{ maxWidth: 120 }} variant="outlined">
        <CardContent>
          <Typography>{user.name}</Typography>
          <Typography>{user.room_number}</Typography>
          <CardActions>
            <Button
              onClick={() => {
                setPostUsers(postUsers.filter((postUser) => postUser !== user));
              }}
            >
              削除
            </Button>
          </CardActions>
        </CardContent>
      </Card>
    );
  };

  return (
    <>
      <Button onClick={handleAddUser}>追加</Button>
      <ScrollMenu>
        {postUsers.map((user) => (
          <UserCard key={user.id} user={user} />
        ))}
      </ScrollMenu>
      <TextField
        value={searchParam}
        label="部屋番号"
        onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
          setSearchParams(event.target.value);
        }}
      />
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>ユーザー名</TableCell>
            <TableCell>部屋番号</TableCell>
            <TableCell>休寮</TableCell>
            <TableCell></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {users
            .filter((user) => !user.room_number.indexOf(searchParam))
            .map((user) => {
              return (
                <TableRow key={user.id}>
                  <TableCell>{user.name}</TableCell>
                  <TableCell>{user.room_number}</TableCell>
                  <TableCell>{user.is_active ? "" : "休寮中"}</TableCell>
                  <TableCell>
                    <Button
                      onClick={() => {
                        if (postUsers.includes(user)) {
                          setPostUsers(
                            postUsers.filter((userId) => userId.id !== user.id)
                          );
                        } else {
                          setPostUsers([...postUsers, user]);
                        }
                      }}
                    >
                      {postUsers.includes(user) ? "削除" : "選択"}
                    </Button>
                  </TableCell>
                </TableRow>
              );
            })}
        </TableBody>
      </Table>
    </>
  );
}
