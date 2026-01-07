"use client";
import Drawer from "@mui/material/Drawer";
import List from "@mui/material/List";
import Divider from "@mui/material/Divider";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import IconButton from "@mui/material/IconButton";
import MenuIcon from "@mui/icons-material/Menu";
import Box from "@mui/material/Box";
import React from "react";
import { useRouter } from "next/navigation";
import HomeIcon from "@mui/icons-material/Home";
import EngineeringIcon from "@mui/icons-material/Engineering";
import ImportContactsIcon from "@mui/icons-material/ImportContacts";
import DashboardIcon from "@mui/icons-material/Dashboard";
import GroupsIcon from "@mui/icons-material/Groups";
export const MyDrawer = () => {
  const [open, setOpen] = React.useState(false);
  const router = useRouter();

  const toggleDrawer = (newOpen: boolean) => () => {
    setOpen(newOpen);
  };

  const DrawerList = (
    <Box sx={{ width: 250 }} role="presentation" onClick={toggleDrawer(false)}>
      <List>
        <ListItem key={0} disablePadding>
          <ListItemButton onClick={() => router.replace(`/`)}>
            <ListItemIcon>
              <HomeIcon />
            </ListItemIcon>
            <ListItemText primary={"ホーム"} />
          </ListItemButton>
        </ListItem>
        <Divider />
        <ListItem key={1} disablePadding>
          <ListItemButton onClick={() => router.replace(`/shifts`)}>
            <ListItemIcon>
              <EngineeringIcon />
            </ListItemIcon>
            <ListItemText primary={"仕事"} />
          </ListItemButton>
        </ListItem>
        <ListItem key={2} disablePadding>
          <ListItemButton onClick={() => router.replace(`/tasks`)}>
            <ListItemIcon>
              <ImportContactsIcon />
            </ListItemIcon>
            <ListItemText primary={"マニュアル"} />
          </ListItemButton>
        </ListItem>
        <ListItem key={4} disablePadding>
          <ListItemButton onClick={() => router.replace(`/templates`)}>
            <ListItemIcon>
              <DashboardIcon />
            </ListItemIcon>
            <ListItemText primary={"テンプレート"} />
          </ListItemButton>
        </ListItem>

        <ListItem key={7} disablePadding>
          <ListItemButton onClick={() => router.replace(`/groups`)}>
            <ListItemIcon>
              <GroupsIcon />
            </ListItemIcon>
            <ListItemText primary={"グループ選択画面へ"} />
          </ListItemButton>
        </ListItem>
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
