import { AppProvider } from "@toolpad/core/AppProvider";
import { AuthProvider, SignInPage } from "@toolpad/core/SignInPage";
import axios from "@/axios";

const providers = [{ id: "credentials", name: "Email and Password" }];

const signIn = async (
  provider: AuthProvider,
  formData: { email: string; password: string }
) => {
  await axios
    .post("http://localhost:8888/login", {
      headers: {
        "Content-Type": "application/json",
      },
      body: {
        user_name: formData.email,
        password: formData.password,
      },
    })
    .then((response) => {
      localStorage.setItem("accessToken", response.data.access_token);
      return { success: "success login" };
    })
    .catch(() => {
      return { error: "Invalid credentials" };
    });
  return { error: "Invalid credentials" };
};

export default function App() {
  return (
    <AppProvider>
      <SignInPage
        providers={providers}
        slotProps={{
          emailField: { autoFocus: false },
          form: { noValidate: true },
        }}
        signIn={signIn}
      />
    </AppProvider>
  );
}
