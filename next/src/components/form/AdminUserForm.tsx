import * as React from "react";
import Button from "@mui/material/Button";
import TextField from "@mui/material/TextField";
import Grid from "@mui/material/Grid";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";

export const AdminUserForm = () => {
  return (
    <>
      <Grid container spacing={2}>
        <Grid>
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
        <Grid>
          <TextField
            required
            fullWidth
            id="room_number"
            label="部屋番号"
            name="room_number"
            autoComplete="room_number"
          />
        </Grid>

        <Grid>
          <TextField
            required
            fullWidth
            name="password"
            label="Password"
            id="password"
            autoComplete="new-password"
          />
        </Grid>
        <Grid>
          <FormControlLabel
            control={
              <Checkbox
                id="is_admin"
                name="is_admin"
                inputProps={{ "aria-label": "controlled" }}
              />
            }
            label="管理者にする"
          />
        </Grid>
      </Grid>
      <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
        登録完了
      </Button>
    </>
  );
};
