import Button from "@mui/material/Button";
import Grid from "@mui/material/Grid";
import { UserRequest } from "@/types/UserType";
import { UncontrolledForm } from "./UncontrolledForm";

export const UserForm = ({ data }: { data: UserRequest }) => {
  return (
    <Grid container spacing={2}>
      <UncontrolledForm data={data} />
      <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>
        登録
      </Button>
    </Grid>
  );
};
