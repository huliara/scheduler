'use client';
import axios from "@/axios";
import { redirect } from "next/navigation";
import { ReactNode } from "react";

const AuthProvider = ({ children }: { children: ReactNode }) => {
  const user = axios
    .get("/user/profile")
    .then((res) => res.data)
    .catch((err) => redirect("/login"));
  return <>{children}</>;
};

export default AuthProvider;
