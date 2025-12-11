"use client"
import { useRouter } from "next/navigation";

import { ReactNode, useEffect } from "react";

const AuthProvider = ({ children }: { children: ReactNode }) => {
  const router = useRouter()
  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      router.push("/login");
    }
  },[])


  return <>{children}</>;
};

export default AuthProvider;
