"use client";
import axios from "@/axios";
import { useRouter } from "next/navigation";

import { ReactNode, useEffect } from "react";

const AuthProvider = ({ children }: { children: ReactNode }) => {
  const router = useRouter();
  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      router.push("/login");
    }
    axios.get("/user/profile", {}).catch((e) => {
      if (e.response.status === 401 || e.response.status === 403)
        router.push("/login");
    });
  }, []);

  return <>{children}</>;
};

export default AuthProvider;
