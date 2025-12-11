import axios from "@/axios";
import { redirect } from "next/navigation";
import { ReactNode } from "react";

const AuthProvider = ({ children }: { children: ReactNode }) => {
  const user = axios
    .get("/users/profile")
    .then((res) => res.data)
    .catch((err) => redirect("/login"));
  return <>{children}</>;
};

export default AuthProvider;
