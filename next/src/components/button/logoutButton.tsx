"use client";
import Button from "@mui/material/Button";
import { useRouter } from "next/navigation";

export const LogoutButton = () => {
  const router = useRouter();
  const signOut = async () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("id");
    localStorage.removeItem("name");
    router.push("/login");
  };
  return (
    <Button color="inherit" onClick={() => signOut()}>
      ログアウト
    </Button>
  );
};
