"use client";
import DeleteConfirmForm from "@/components/form/DeleteConfirmForm";
import axios from "@/axios";
import { useRouter } from "next/navigation";

export default function GroupDeleteForm({
  params,
}: {
  params: { groupId: string };
}) {
  const router = useRouter();
  const handleGroupDelete = () => {
    axios
      .delete(`/admin/groups/${params.groupId}`)
      .then((res) => {
        router.push("/admin/groups");
      })
      .catch((err) => {console.log(err)});
  };
  return (
    <DeleteConfirmForm
      onSubmit={handleGroupDelete}
      redirect={`/admin/groups`}
    />
  );
}
