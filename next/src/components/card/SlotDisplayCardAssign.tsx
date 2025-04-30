import { useParams } from "next/navigation";
import { UserTaskRespose, TaskResponse } from "@/types/ResponseType";
import * as React from "react";
import { SlotDisplayCardBase } from "./SlotDisplayCardBase";
import { Button } from "@mui/material";
import axios from "@/axios";
import CheckIcon from "@mui/icons-material/Check";
import { KeyedMutator } from "swr";
export const SlotDisplayCardAssign = ({
  slot,
  mutate,
}: {
  slot: TaskResponse;
  mutate: KeyedMutator<UserTaskRespose>;
}) => {
  const groupId = useParams().groupId;
  const handleCancel = (slot_id: string) => {
    axios
      .post(`/${groupId}/tasks/${slot_id}/cancel`)
      .then((res) => {
        mutate();
      })
      .catch((err) => {});
  };
  return (
    <SlotDisplayCardBase slot={slot} style={{ backgroundColor: "#bdbdbd" }}>
      <Button onClick={() => handleCancel(slot.id)}>キャンセル</Button>
    </SlotDisplayCardBase>
  );
};

export const SlotDisplayCardUnassign = ({ task }: { task: TaskResponse }) => {
  const [isAssigned, setAssigned] = React.useState(false);
  const assignSlot = () => {
    axios
      .post(`/${task.group_id}/tasks/${task.id}/assign`)
      .then((res) => {
        setAssigned(true);
      })
      .catch((err) => {});
  };
  return (
    <SlotDisplayCardBase slot={task} style={{ backgroundColor: "white" }}>
      {isAssigned ? (
        <CheckIcon />
      ) : (
        <Button size="small" onClick={assignSlot}>
          参加する
        </Button>
      )}
    </SlotDisplayCardBase>
  );
};

export const SlotDisplayCardEnd = ({ slot }: { slot: TaskResponse }) => {
  const groupId = slot.group_id;
  const [isCompleted, setCompleted] = React.useState(false);
  const completeSlot = (done: boolean) => {
    axios
      .post(`/${groupId}/tasks/${slot.id}/complete`, { done: done })
      .then((res) => {
        setCompleted(true);
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return (
    <SlotDisplayCardBase slot={slot} style={{ backgroundColor: "white" }}>
      {isCompleted ? (
        <CheckIcon />
      ) : (
        <>
          <Button size="small" onClick={() => completeSlot(true)}>
            仕事しました
          </Button>
          <Button size="small" onClick={() => completeSlot(false)}>
            しませんでした
          </Button>
        </>
      )}
    </SlotDisplayCardBase>
  );
};
