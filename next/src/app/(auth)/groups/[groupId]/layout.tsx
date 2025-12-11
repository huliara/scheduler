import * as React from "react";
import Box from "@mui/material/Box";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import { MyDrawer } from "@/components/list/Drawer";
import { LogoutButton } from "@/components/button/logoutButton";
export default async function TemporaryDrawer({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ groupId: string }>;
}) {
  const groupId = (await params).groupId;
  return (
    <div>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <MyDrawer groupId={groupId} />
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Scheduler
            </Typography>
            <LogoutButton />
          </Toolbar>
        </AppBar>
      </Box>
      {children}
    </div>
  );
}
