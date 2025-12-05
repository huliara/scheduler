import * as React from "react";
import Button from "@mui/material/Button";
import CssBaseline from "@mui/material/CssBaseline";
import TextField from "@mui/material/TextField";
import Grid from "@mui/material/Grid";
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import Container from "@mui/material/Container";
import { createTheme, ThemeProvider } from "@mui/material/styles";
import { MultiSelectField } from "@/components/form/MultiSelectField";
import { ResponseBase } from "@/types/ResponseType";
const theme = createTheme();

export const UserCreateForm = ({
  task,
  handleSubmit,
  exp_task,
  setExpTask,
}: {
  task: ResponseBase[];
  handleSubmit: () => void;
  exp_task: string[];
  setExpTask: React.Dispatch<React.SetStateAction<string[]>>;
}) => {
  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
          }}
        >
          <Typography component="h1" variant="h5">
            ユーザ
          </Typography>
          <Box
            component="form"
            noValidate
            onSubmit={handleSubmit}
            sx={{ mt: 3 }}
          >
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  autoComplete="given-name"
                  name="name"
                  required
                  fullWidth
                  id="name"
                  label="名前"
                  autoFocus
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  required
                  fullWidth
                  id="room_number"
                  label="部屋番号"
                  name="room_number"
                  autoComplete="room_number"
                />
              </Grid>

              <Grid item xs={12}>
                <TextField
                  required
                  fullWidth
                  name="password"
                  label="Password"
                  id="password"
                  autoComplete="new-password"
                />
              </Grid>
              <Grid item xs={12}>
                <MultiSelectField
                  options={task}
                  title="経験したことのあるタスク"
                  defaultValue={exp_task}
                  setData={setExpTask}
                />
              </Grid>
            </Grid>
            <Button
              type="submit"
              fullWidth
              variant="contained"
              sx={{ mt: 3, mb: 2 }}
            >
              登録完了
            </Button>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
};
