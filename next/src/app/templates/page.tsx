"use client";
import useSWR from "swr";
import { TemplateResponse } from "@/types/ResponseType";
import {
  Button,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
} from "@mui/material";
import axios, { fetcher } from "@/axios";
import Link from "next/link";
export default function TemplateList({
  params,
}: {
  params: { groupId: string };
}) {
  const { data, error, mutate, isLoading } = useSWR<{
    templates: TemplateResponse[];
  }>(`/${params.groupId}/templates`, fetcher);
  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;

  const handleOnClick = (template_id: string) => {
    axios
      .delete(`/${params.groupId}/templates/${template_id}`)
      .then((res) => {
        mutate();
      })
      .catch((err) => {});
  };

  return (
    <>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>名前</TableCell>
            <TableCell></TableCell>
            <TableCell></TableCell>
            <TableCell></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.templates.map((template) => (
            <TableRow key={template.id}>
              <TableCell>{template.name}</TableCell>
              <TableCell>
                <Link href={`/${params.groupId}/templates/${template.id}`}>
                  詳細
                </Link>
              </TableCell>
              <TableCell>
                <Link
                  href={`/${params.groupId}/templates/${template.id}/generate`}
                >
                  シフトを募集
                </Link>
              </TableCell>
              <TableCell>
                <Button onClick={() => {handleOnClick(template.id)}}>削除</Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
      <Link href={`/${params.groupId}/templates/create`}>新規作成</Link>
    </>
  );
}
