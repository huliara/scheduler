"use client";
import {
  Button,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";
import { PropsWithChildren, ReactElement } from "react";
import { getFieldJA, ResponseFieldKeys } from "@/utils/types";
import { ResponseType } from "@/types/Base";

type Props<T> = {
  data: T[];
  onClicks: { action: (id: string) => void; label: string }[];
};

type OptionalResponseFieldKeys = Exclude<ResponseFieldKeys, "id">;

type ResponseListType = { id: string } & {
  [key in OptionalResponseFieldKeys]?: string | number;
};

export const SchedulerList = <T extends ResponseListType>(
  props: PropsWithChildren<Props<T>>
): ReactElement<any, any> => {
  return (
    <>
      <Table>
        <TableHead>
          <TableRow>
            {(Object.keys(props.data[0]) as ResponseFieldKeys[])
              .filter((key) => key === "id")
              .map((key) => {
                return <TableCell key={key}>{getFieldJA(key)}</TableCell>;
              })}
            {Array(props.onClicks.length).map((_) => (
              <TableCell />
            ))}
          </TableRow>
        </TableHead>
        <TableBody>
          {props.data.map((row) => (
            <TableRow key={row.id}>
              {(Object.keys(row) as ResponseFieldKeys[])
                .filter((key) => key === "id")
                .map((key) => {
                  const value = (row as any)[key];
                  return value ? (
                    <TableCell key={key}>{value}</TableCell>
                  ) : (
                    <TableCell key={key} />
                  );
                })}
              {props.onClicks.map((onClick) => {
                return (
                  <TableCell>
                    <Button
                      onClick={() => {
                        onClick.action(row.id);
                      }}
                    >
                      {onClick.label}
                    </Button>
                  </TableCell>
                );
              })}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </>
  );
};
