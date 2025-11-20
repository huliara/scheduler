"use client";
import axios from "@/axios";
import { Container, Typography } from "@mui/material";
import Box from "@mui/material/Box";
import { RoleForm } from "@/components/form/RoleForm";
import { useSnackbarContext } from "@/components/provider/SnackBar";
import { useState } from "react";
import { Permission } from "@/types/ResponseType";
export default function RoleCreateForm({
  params,
}: {
  params: { groupId: string };
}) {
  const { showSnackbar } = useSnackbarContext();
  const [permissions, setPermissions] = useState<Permission[]>([]);
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    console.log(data.get("name"));
    axios
      .post(`${params.groupId}/roles/`, {
        name: data.get("name"),
        permissions: permissions,
      })
      .then((response) => {
        showSnackbar("success", "作成しました");
      })
      .catch((err) => {
        showSnackbar("error", "作成に失敗しました");
      });
  };

  const defaultData = {
    name: "",
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
        <Typography component="h1" variant="h5">
          ロールを新規作成
        </Typography>
        <RoleForm
          name={defaultData.name}
          permissions={permissions}
          setPermissions={setPermissions}
        />
      </Box>
    </Container>
  );
}
