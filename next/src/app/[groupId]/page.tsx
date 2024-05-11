"use client";
import {
  SlotDisplayCardAssign,
  SlotDisplayCardEnd,
  SlotDisplayCardUnassign,
} from "@/components/card/SlotDisplayCardAssign";
import SlotListOneDay from "@/components/list/SlotListOneDay";
import { ScrollMenu } from "react-horizontal-scrolling-menu";
import "react-horizontal-scrolling-menu/dist/styles.css";
import useSWR from "swr";
import { fetcher } from "@/axios";
import { SlotResponse } from "@/types/ResponseType";
import { useSession } from "next-auth/react";

export default function GroupHome({ params }: { params: { groupId: string } }) {
  const { data, error, isLoading } = useSWR<{ slots: SlotResponse[] }>(
    `/${params.groupId}/slots`,
    fetcher
  );
  const session = useSession();
  if (error || session.status === "unauthenticated")
    return <div>Loading Failed</div>;
  if (!data || !session.data || session.data.user === undefined)
    return <div>loading...</div>;
  if (isLoading) return <div>loading...</div>;

  const futureSlots = data.slots.filter(
    (slot) => new Date(slot.end_time).getTime() > new Date().getTime()
  );

  const days = Array.from(
    new Set(
      futureSlots.map((slot) =>
        new Date(slot.start_time).toLocaleDateString("ja-JP", {
          month: "2-digit",
          day: "numeric",
        })
      )
    )
  ).sort((a, b) => new Date(a).getTime() - new Date(b).getTime());
  return (
    <>
      <h2>入る予定のシフト</h2>
      <ScrollMenu>
        {data.slots
          .filter(
            (slot) =>
              new Date(slot.end_time).getTime() > new Date().getTime() &&
              slot.assignees
                .map((assignee) => assignee.id)
                .includes(session.data.user.id)
          )
          .map((slot, index) => (
            <SlotDisplayCardAssign slot={slot} key={index} />
          ))}
      </ScrollMenu>
      <h2>募集中のシフト</h2>
      <ScrollMenu>
        {days.map((day, index) => {
          const slots = futureSlots
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
                slot.assignees
                  .map((assignee) => assignee.id)
                  .includes(session.data.user.id) ? (
                  <SlotDisplayCardAssign slot={slot} key={index} />
                ) : (
                  <SlotDisplayCardUnassign slot={slot} key={index} />
                )
              )}
            </SlotListOneDay>
          );
        })}
      </ScrollMenu>
      <h2>過去に入ったシフト</h2>
      <ScrollMenu>
        {data.slots
          .filter(
            (slot) =>
              new Date(slot.end_time).getTime() < new Date().getTime() &&
              slot.assignees
                .map((assignee) => assignee.id)
                .includes(session.data.user.id)
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
    </>
  );
}
