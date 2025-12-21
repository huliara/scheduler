import { Box, Button, TextField } from "@mui/material";
import axios from "@/axios";
import { useEffect, useState } from "react";
export const TemplateNameForm = ({
  groupId,
  templateId,
  defaultName,
}: {
  groupId: string;
  templateId: string;
  defaultName: string;
}) => {
  const [name, setName] = useState("");
  useEffect(() => {
    setName(defaultName);
  }, [defaultName]);

  const handleNameSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    axios
      .patch(`/templates/${templateId}`, {
        name: name,
      })
      .then((response) => {})
      .catch((err) => {});
  };
  return (
    <Box
      component="form"
      noValidate
      autoComplete="off"
      onSubmit={handleNameSubmit}
    >
      <TextField
        id="template_name"
        label="テンプレート名"
        value={name}
        onChange={(event: React.ChangeEvent<HTMLInputElement>) => {
          setName(event.target.value);
        }}
      />
      <Button type="submit" variant="contained" sx={{ mt: 3, mb: 2 }}>
        名前の変更を保存
      </Button>
    </Box>
  );
};
