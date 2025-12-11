"use client";
import DeleteConfirmForm from "@/components/form/DeleteConfirmForm";
import axios from "@/axios";

export default function UserDeleteForm({
  params,
}: {
  params: { userId: string };
}) {
  const handleUserDelete = () => {
    axios
      .delete(`admin/users/${params.userId}`)
      .then((res) => {})
      .catch((err) => {});
  };
  return (
    <DeleteConfirmForm onSubmit={handleUserDelete} redirect={`/admin/users`} />
  );
}
