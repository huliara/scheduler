"use client";
import {
  SlotDisplayCardAssign,
  SlotDisplayCardEnd,
  SlotDisplayCardUnassign,
} from "@/components/card/SlotDisplayCardAssign";
import { Accordion, AccordionSummary } from "@mui/material";
import { ExpandMore } from "@mui/icons-material";
import SlotListOneDay from "@/components/list/SlotListOneDay";
import { ScrollMenu } from "react-horizontal-scrolling-menu";
import "react-horizontal-scrolling-menu/dist/styles.css";
import useSWR from "swr";
import { fetcher } from "@/axios";
import { useRouter } from "next/navigation";
import { ShiftsResponse } from "@/types/ShiftType";
import { useEffect, useState } from "react";
import { ErrorPage } from "@/components/pages/ErrorPage";
import { LoadingPage } from "@/components/pages/LoadingPage";

export default function Home() {
  const { data, error, mutate, isLoading } = useSWR<ShiftsResponse>(
    `/user/shifts`,
    fetcher
  );
  const router = useRouter();
  const [userId, setUserId] = useState<string | null>();
  useEffect(() => {
    console.log(localStorage.getItem("id"));
    setUserId(localStorage.getItem("id"));
  }, []);
  if (error) return <ErrorPage />;
  if (!data || isLoading || !userId) return <LoadingPage />;

  const futureShifts = data.filter(
    (shift) => shift.start_time >= new Date().toISOString()
  );

  const days = Array.from(
    new Set(
      futureShifts.map((shift) =>
        new Date(shift.start_time).toLocaleDateString("ja-JP", {
          year: "numeric",
          month: "2-digit",
          day: "numeric",
        })
      )
    )
  ).sort((a, b) => new Date(a).getTime() - new Date(b).getTime());
  return (
    <>
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
                  year: "numeric",
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
                  <SlotDisplayCardUnassign shift={slot} key={index} />
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
          {data
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
