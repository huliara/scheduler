"use client";
import { TemplateResponse } from "@/types/TemplateType";
import Link from "next/link";
import { useRouter } from "next/navigation";
import DataLists from "@/components/list/DataLists";
export default function TemplateList() {
  const router = useRouter();

  const onClicks = [
    {
      action: (id: string) => router.push(`/templates/${id}/generate`),
      label: "募集",
    },
  ];

  return (
    <>
      <DataLists<TemplateResponse>
        dataName="templates"
        targetField={["name"]}
        addtionalActions={onClicks}
      />
      <Link href={`/templates/create`}>新規作成</Link>
    </>
  );
}
