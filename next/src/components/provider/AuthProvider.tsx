import axios from "@/axios";
import { redirect } from "next/navigation";
import { ReactNode } from "react";

const AuthProvider = ({ children }: { children: ReactNode }) => {
  const user = axios
    .get("/login")
    .then((res) => {
      localStorage.setItem("id", res.data.id);
      localStorage.setItem("name", res.data.name);
      localStorage.setItem("accessToken", res.data.access_token);
    })
    .catch((err) => redirect("/login"));
  return <>{children}</>;
};

export default AuthProvider;
