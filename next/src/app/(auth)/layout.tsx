"use client";
import { Button, Toolbar } from "@mui/material";
import { useRouter } from "next/navigation";

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  return (
    <>
      <Toolbar>
        <Button color="inherit" onClick={() => router.replace("/login")}>
          ログイン
        </Button>
        <Button color="inherit" onClick={() => router.replace("/signup")}>
          新規登録
        </Button>
      </Toolbar>
      {children}
    </>
  );
}
