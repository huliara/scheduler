"use client";
import Button from "@mui/material/Button";
import React from "react";

export const LogoutButton = () => {
  const signOut = async () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("id");
    localStorage.removeItem("name");
  };
  return (
    <Button color="inherit" onClick={() => signOut()}>
      ログアウト
    </Button>
  );
};
