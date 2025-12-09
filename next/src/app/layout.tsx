import { Inter } from "next/font/google";
import { Metadata } from "next";
import { AppRouterCacheProvider } from "@mui/material-nextjs/v13-appRouter";
import { Theme } from "@/components/provider/Theme";
import { SnackbarProvider } from "@/components/provider/SnackBar";
import AuthGuard from "@/components/provider/AuthProvider";
const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "scheduler",
  description: "Task management system for kumano domitory",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <AppRouterCacheProvider>
          <AuthGuard>
            <Theme>
              <SnackbarProvider>{children}</SnackbarProvider>
            </Theme>
          </AuthGuard>
        </AppRouterCacheProvider>
      </body>
    </html>
  );
}
