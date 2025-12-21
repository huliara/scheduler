"use client";
import { LogoutButton } from "@/components/button/logoutButton";
import { MyDrawer } from "@/components/list/Drawer";
import AuthProvider from "@/components/provider/AuthProvider";
import { AppBar, Box, Toolbar, Typography } from "@mui/material";

export default function MainLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <AuthProvider>
      {" "}
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <MyDrawer />
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Scheduler
            </Typography>
            <LogoutButton />
          </Toolbar>
        </AppBar>
      </Box>
      {children}
    </AuthProvider>
  );
}
