import axios from "@/axios";
import { redirect } from "next/navigation";
import { ReactNode } from "react";

const AuthGuard = ({ children }: { children: ReactNode }) => {
  const user = axios
    .get("/user/profile")
    .then((res) => res.data)
    .catch((err) => redirect("/login"));
  return <>{children}</>;
};

export default AuthGuard;
