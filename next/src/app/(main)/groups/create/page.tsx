"use client";
import axios from "@/axios";
import { Container, Typography } from "@mui/material";
import Box from "@mui/material/Box";
import { useSnackbarContext } from "@/components/provider/SnackBar";
import Link from "next/link";
import { GroupForm } from "@/components/form/GroupForm";
import { useRouter } from "next/navigation";
export default function GroupCreateForm() {
  const { showSnackbar } = useSnackbarContext();
  const router = useRouter();
  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    axios
      .post(`/groups`, {
        name: data.get("name"),
      })
      .then((response) => {
        showSnackbar("success", "作成しました");
        console.log(response.data);
        router.replace(`/groups/${response.data.id}`);
      })
      .catch((err) => {
        showSnackbar("error", "作成に失敗しました");
      });
  };

  const defaultData = {
    id: "",
    name: "",
  };

  return (
    <Container component="main" maxWidth="xs">
      <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
        <Typography component="h1" variant="h5">
          グループを新規作成
        </Typography>
        <GroupForm data={defaultData} />
      </Box>
      <Link href={`/groups`}>一覧へ戻る</Link>
    </Container>
  );
}
