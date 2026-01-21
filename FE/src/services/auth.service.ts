import { api, LoginResponse } from "@/lib/api";

const LOGIN_PATH = "/api/auth/login";

export async function login(
  user_name: string,
  password: string
): Promise<LoginResponse> {
  const response = await api.post<LoginResponse>(LOGIN_PATH, {
    user_name,
    password
  });

  if (typeof window !== "undefined") {
    window.localStorage.setItem("auth_token", response.data.token);
    window.localStorage.setItem("user_id", String(response.data.user_id));
    window.localStorage.setItem("role_id", String(response.data.role_id));
    if (response.data.household_id != null) {
      window.localStorage.setItem(
        "household_id",
        String(response.data.household_id)
      );
    } else {
      window.localStorage.removeItem("household_id");
    }
    // Store full user info for easy access
    window.localStorage.setItem(
      "user_info",
      JSON.stringify({
        user_id: response.data.user_id,
        role_id: response.data.role_id,
        household_id: response.data.household_id,
      })
    );
  }

  return response.data;
}

export const getCurrentUser = async (): Promise<any> => {
  const response = await api.get("/api/auth/me");
  return response.data;
};

export const updateProfile = async (data: {
  user_name?: string;
  email?: string;
  description?: string;
  password?: string;
}): Promise<any> => {
  const response = await api.put("/api/auth/me", data);
  return response.data;
};
