'use client'
import axios from "@/axios";
import DeleteConfirmForm from "@/components/form/DeleteConfirmForm";
import { useRouter } from "next/navigation";
export default function TemplateDelete({
  params,
}: {
  params: { groupId: string; templateId: string };
  }) {
  const router=useRouter()
  const handleSubmit = () => {
    axios
      .delete(`/${params.groupId}/templates/${params.templateId}`)
      .then((res) => {router.push(`/${params.groupId}/templates`)})
      .catch((err) => {});
  };
  return (
    <DeleteConfirmForm
      onSubmit={handleSubmit}
      redirect={`/${params.groupId}/templates`}
    />
  );
}
