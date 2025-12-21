"use client";
import { fetcher } from "@/axios";
import useSWR from "swr";
import { TemplateResponse } from "@/types/TemplateType";
import {
  Grid,
  Link,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  Typography,
} from "@mui/material";
import { use } from "react";

export default function TemplateDetail({
  params,
}: {
  params: Promise<{ templateId: string }>;
}) {
  const templateId = use(params).templateId;
  const { data, error, isLoading } = useSWR<TemplateResponse>(
    `/templates/${templateId}`,
    fetcher
  );

  if (error) return <div>error</div>;
  if (!data) return <div>no data</div>;
  if (isLoading) return <div>loading...</div>;

  const last_date =
    data.slots.length !== 0
      ? 1 +
        data.slots
          .map((slot) => slot.date_from_start)
          .reduce((a, b) => Math.max(a, b))
      : 1; // => 10

  return (
    <>
      <Typography variant="h4" component="h1" gutterBottom>
        {data.name}
      </Typography>
      <Grid container spacing={2}>
        <Grid>
          <Link href={`/templates/${templateId}/generate`}>シフトを募集</Link>
        </Grid>
        <Grid>
          <Link href={`/templates/${templateId}/edit`}>編集</Link>
        </Grid>
        <Grid>
          <Link href={`/templates/${templateId}/delete`}>削除</Link>
        </Grid>{" "}
        {new Array(last_date).fill(0).map((_, i) => (
          <Grid key={i}>
            <Paper sx={{ p: 2, display: "flex", flexDirection: "column" }}>
              <Typography
                component="h2"
                variant="h6"
                color="primary"
                gutterBottom
              >
                {i + 1}日目
              </Typography>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>名前</TableCell>
                    <TableCell>開始時刻</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {data.slots
                    .filter((slot) => slot.date_from_start === i)
                    .sort((a, b) => a.start_time.localeCompare(b.start_time))
                    .map((slot) => (
                      <TableRow key={slot.id}>
                        <TableCell>{slot.name}</TableCell>
                        <TableCell>{slot.start_time}</TableCell>
                      </TableRow>
                    ))}
                </TableBody>
              </Table>
            </Paper>
          </Grid>
        ))}
      </Grid>
    </>
  );
}
