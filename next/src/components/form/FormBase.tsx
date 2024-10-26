import { Container, Typography } from "@mui/material";
import Box from "@mui/material/Box";
import Link from "next/link";
export const FormBase = ({
  children,
  title,
  param,
  handleSubmit,
}: {
  children: React.ReactNode;
  title: string;
  param: string;
  handleSubmit: (event: React.FormEvent<HTMLFormElement>) => void;
}) => {
  return (
    <Container component="main" maxWidth="xs">
      <Box component="form" noValidate onSubmit={handleSubmit} sx={{ mt: 3 }}>
        <Typography component="h1" variant="h5">
          {title}
        </Typography>
        {children}
      </Box>
      <Link href={param}>戻る</Link>
    </Container>
  );
};
