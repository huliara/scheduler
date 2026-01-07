import { ShiftResponse, ShiftsResponse } from "@/types/ShiftType";
import * as React from "react";
import { SlotDisplayCardBase } from "./SlotDisplayCardBase";
import { Button } from "@mui/material";
import axios from "@/axios";
import { KeyedMutator } from "swr";
import { UncontrolledSelectField } from "../field/UncontrolledSelectField";
import { Box } from "@mui/system";
export const SlotDisplayCardAssign = ({
  slot,
  mutate,
}: {
  slot: ShiftResponse;
  mutate: KeyedMutator<ShiftsResponse>;
}) => {
  const handleCancel = (slot_id: string) => {
    axios
      .post(`/shifts/${slot_id}/cancel`)
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

export const SlotDisplayCardUnassign = ({
  shift,
  mutate,
}: {
  shift: ShiftResponse;
  mutate: KeyedMutator<ShiftsResponse>;
}) => {
  const assignSlot = () => {
    axios
      .post(`/shifts/${shift.id}/assign`)
      .then((res) => {
        mutate();
      })
      .catch((err) => {});
  };
  return (
    <SlotDisplayCardBase slot={shift} style={{ backgroundColor: "white" }}>
      <Button size="small" onClick={assignSlot}>
        参加する
      </Button>
    </SlotDisplayCardBase>
  );
};

export const SlotDisplayCardEnd = ({
  shift,
  mutate,
}: {
  shift: ShiftResponse;
  mutate: KeyedMutator<ShiftsResponse>;
}) => {
  return (
    <SlotDisplayCardBase slot={shift} style={{ backgroundColor: "white" }}>
      <WorkerReplaceForm shift={shift} mutate={mutate} />
    </SlotDisplayCardBase>
  );
};

export const SlotDisplayCardWorking = ({
  slot,
  mutate,
}: {
  slot: ShiftResponse;
  mutate: KeyedMutator<ShiftsResponse>;
}) => {
  const completeSlot = (done: boolean) => {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        axios
          .post(`/shifts/${slot.id}/complete`, {
            done: done,
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
          })
          .then((res) => {
            mutate();
          })
          .catch((err) => {
            console.log(err);
          });
      },
      (error) => {
        console.log(error);
      }
    );
  };

  return (
    <SlotDisplayCardBase slot={slot} style={{ backgroundColor: "white" }}>
      <Button size="small" onClick={() => completeSlot(true)}>
        仕事しました
      </Button>
      <Button size="small" onClick={() => completeSlot(false)}>
        しませんでした
      </Button>
      <WorkerReplaceForm shift={slot} mutate={mutate} />
    </SlotDisplayCardBase>
  );
};

const WorkerReplaceForm = ({
  shift,
  mutate,
}: {
  shift: ShiftResponse;
  mutate: KeyedMutator<ShiftsResponse>;
}) => {
  const handleConvert = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    axios
      .patch(`/shifts/${shift.id}/workers`, {
        new_worker_id: data.get("member_id"),
      })
      .then((res) => {
        mutate();
      })
      .catch((err) => {
        console.log(err);
      });
  };
  return (
    <Box component="form" onSubmit={handleConvert}>
      <UncontrolledSelectField
        fieldKey="member_id"
        defaultValue=""
        url={`/groups/${shift.group_id}/members`}
      />
      <Button type="submit" size="small">
        交代
      </Button>
    </Box>
  );
};
