"use client";
import Drawer from "@mui/material/Drawer";
import List from "@mui/material/List";
import Divider from "@mui/material/Divider";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import InboxIcon from "@mui/icons-material/MoveToInbox";
import MailIcon from "@mui/icons-material/Mail";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import Box from "@mui/material/Box";
import React from "react";
import { useRouter } from "next/navigation";

export const MyDrawer = ({ groupId }: { groupId: string }) => {
  const [open, setOpen] = React.useState(false);
  const router = useRouter();

  const toggleDrawer = (newOpen: boolean) => () => {
    setOpen(newOpen);
  };

  const DrawerList = (
    <Box sx={{ width: 250 }} role="presentation" onClick={toggleDrawer(false)}>
      <List>
        <ListItem key={1} disablePadding>
          <ListItemButton onClick={() => router.replace(`/${groupId}/slots`)}>
            <ListItemIcon>
              <InboxIcon />
            </ListItemIcon>
            <ListItemText primary={"仕事"} />
          </ListItemButton>
        </ListItem>
        <ListItem key={2} disablePadding>
          <ListItemButton
            onClick={() => router.replace(`/${groupId}/task_details`)}
          >
            <ListItemIcon>
              <InboxIcon />
            </ListItemIcon>
            <ListItemText primary={"マニュアル"} />
          </ListItemButton>
        </ListItem>
        <ListItem key={3} disablePadding>
          <ListItemButton onClick={() => router.replace(`/${groupId}/users`)}>
            <ListItemIcon>
              <InboxIcon />
            </ListItemIcon>
            <ListItemText primary={"ユーザー一覧"} />
          </ListItemButton>
        </ListItem>
        <ListItem key={4} disablePadding>
          <ListItemButton
            onClick={() => router.replace(`/${groupId}/templates`)}
          >
            <ListItemIcon>
              <InboxIcon />
            </ListItemIcon>
            <ListItemText primary={"テンプレート"} />
          </ListItemButton>
        </ListItem>
        <ListItem key={5} disablePadding>
          <ListItemButton onClick={() => router.replace(`/${groupId}/roles`)}>
            <ListItemIcon>
              <InboxIcon />
            </ListItemIcon>
            <ListItemText primary={"ロール"} />
          </ListItemButton>
        </ListItem>
        <ListItem key={6} disablePadding>
          <ListItemButton onClick={() => router.replace(`/${groupId}`)}>
            <ListItemIcon>
              <InboxIcon />
            </ListItemIcon>
            <ListItemText primary={"募集中の仕事"} />
          </ListItemButton>
        </ListItem>
        <ListItem key={7} disablePadding>
          <ListItemButton onClick={() => router.replace(`/groups`)}>
            <ListItemIcon>
              <InboxIcon />
            </ListItemIcon>
            <ListItemText primary={"グループ選択画面へ"} />
          </ListItemButton>
        </ListItem>
      </List>
      <Divider />
      <List>
        {["All mail", "Trash", "Spam"].map((text, index) => (
          <ListItem key={text} disablePadding>
            <ListItemButton>
              <ListItemIcon>
                {index % 2 === 0 ? <InboxIcon /> : <MailIcon />}
              </ListItemIcon>
              <ListItemText primary={text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <>
      <IconButton
        size="large"
        edge="start"
        color="inherit"
        aria-label="menu"
        sx={{ mr: 2 }}
        onClick={toggleDrawer(true)}
      >
        <MenuIcon />
      </IconButton>

      <Drawer open={open} onClose={toggleDrawer(false)}>
        {DrawerList}
      </Drawer>
    </>
  );
};
