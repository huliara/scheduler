import { Inter } from "next/font/google";
import { Metadata } from "next";
import { AppRouterCacheProvider } from '@mui/material-nextjs/v16-appRouter';
import { Theme } from "@/components/provider/Theme";
import { SnackbarProvider } from "@/components/provider/SnackBar";

const inter = Inter({ subsets: ["latin"] });

const metadata: Metadata = {
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
            <Theme>
              <SnackbarProvider>{children}</SnackbarProvider>
            </Theme>
        </AppRouterCacheProvider>
      </body>
    </html>
  );
}
