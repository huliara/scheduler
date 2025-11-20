"use client";
import {
  SlotDisplayCardAssign,
  SlotDisplayCardEnd,
  SlotDisplayCardUnassign,
} from "@/components/card/SlotDisplayCardAssign";
import {
  Accordion,
  AccordionSummary,
  AppBar,
  Box,
  Button,
  Toolbar,
  Typography,
} from "@mui/material";
import { ExpandMore } from "@mui/icons-material";
import SlotListOneDay from "@/components/list/SlotListOneDay";
import { ScrollMenu } from "react-horizontal-scrolling-menu";
import "react-horizontal-scrolling-menu/dist/styles.css";
import useSWR from "swr";
import { fetcher } from "@/axios";
import { UserShiftRespose } from "@/types/ResponseType";
import { useSession } from "next-auth/react";
import { LogoutButton } from "@/components/button/logoutButton";
import { useRouter } from "next/navigation";

export default function Home() {
  const { data, error, mutate, isLoading } = useSWR<UserShiftRespose>(
    `/user/tasks`,
    fetcher
  );
  const session = useSession();
  const router = useRouter();
  if (error || session.status === "unauthenticated")
    return <div>Loading Failed</div>;
  if (!data || !session.data || session.data.user === undefined)
    return <div>loading...</div>;
  if (isLoading) return <div>loading...</div>;
  console.log(data);

  const days = Array.from(
    new Set(
      data.hiring.map((slot) =>
        new Date(slot.start_time).toLocaleDateString("ja-JP", {
          month: "2-digit",
          day: "numeric",
        })
      )
    )
  ).sort((a, b) => new Date(a).getTime() - new Date(b).getTime());
  return (
    <>
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static">
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              Scheduler
            </Typography>
            <Button color="inherit" onClick={() => router.push("/groups")}>
              グループ一覧
            </Button>
            <LogoutButton />
          </Toolbar>
        </AppBar>
      </Box>
      <Accordion defaultExpanded>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <h2>入る予定のシフト</h2>
        </AccordionSummary>
        <ScrollMenu>
          {data.assign.map((slot, index) => (
            <SlotDisplayCardAssign slot={slot} key={index} mutate={mutate} />
          ))}
        </ScrollMenu>
      </Accordion>

      <h2>募集中のシフト</h2>
      <ScrollMenu>
        {days.map((day, index) => {
          const slots = data.hiring
            .filter(
              (slot) =>
                new Date(slot.start_time).toLocaleDateString("ja-JP", {
                  month: "2-digit",
                  day: "numeric",
                }) == day
            )
            .sort(
              (a, b) =>
                new Date(a.start_time).getTime() -
                new Date(b.start_time).getTime()
            );
          return (
            <SlotListOneDay day={day} key={index}>
              {slots.map((slot, index) =>
                slot.workers
                  .map((worker) => worker.id)
                  .includes(session.data.user.id) ? (
                  <SlotDisplayCardAssign
                    slot={slot}
                    key={index}
                    mutate={mutate}
                  />
                ) : (
                  <SlotDisplayCardUnassign task={slot} key={index} />
                )
              )}
            </SlotListOneDay>
          );
        })}
      </ScrollMenu>
      <Accordion>
        <AccordionSummary expandIcon={<ExpandMore />}>
          <h2>過去に入ったシフト</h2>
        </AccordionSummary>
        <ScrollMenu>
          {data.end
            .sort(
              (a, b) =>
                new Date(a.start_time).getTime() -
                new Date(b.start_time).getTime()
            )
            .map((slot, id) => (
              <SlotDisplayCardEnd slot={slot} key={id} />
            ))}
        </ScrollMenu>
      </Accordion>
    </>
  );
}
