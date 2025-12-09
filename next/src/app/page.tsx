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
import { LogoutButton } from "@/components/button/logoutButton";
import { useRouter } from "next/navigation";
import { ShiftsResponse } from "@/types/ShiftType";

export default function Home() {
  const { data, error, mutate, isLoading } = useSWR<ShiftsResponse>(
    `/user/shifts`,
    fetcher
  );
  const router = useRouter();
  const userId = localStorage.getItem("id");
  if (error) return <div>Loading Failed</div>;
  if (!data || isLoading || !userId) return <div>loading...</div>;

  const futureShifts = data.shifts.filter(
    (shift) => shift.start_time >= new Date().toISOString()
  );

  const days = Array.from(
    new Set(
      futureShifts.map((shift) =>
        new Date(shift.start_time).toLocaleDateString("ja-JP", {
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
          {futureShifts
            .filter((shift) =>
              shift.workers.map((user) => user.id).includes(userId)
            )
            .map((slot, index) => (
              <SlotDisplayCardAssign slot={slot} key={index} mutate={mutate} />
            ))}
        </ScrollMenu>
      </Accordion>

      <h2>募集中のシフト</h2>
      <ScrollMenu>
        {days.map((day, index) => {
          const slots = futureShifts
            .filter(
              (slot) =>
                new Date(slot.start_time).toLocaleDateString("ja-JP", {
                  month: "2-digit",
                  day: "numeric",
                }) === day
            )
            .sort(
              (a, b) =>
                new Date(a.start_time).getTime() -
                new Date(b.start_time).getTime()
            );
          return (
            <SlotListOneDay day={day} key={index}>
              {slots.map((slot, index) =>
                slot.workers.map((worker) => worker.id).includes(userId) ? (
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
          {data.shifts
            .filter((shift) => shift.start_time < new Date().toISOString())
            .filter((shift) =>
              shift.workers.map((user) => user.id).includes(userId)
            )
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
