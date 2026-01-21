import {
  api,
  RegistrationPayload,
  RegistrationResponse,
  SubscriptionPlanDto
} from "@/lib/api";

const PLANS_PUBLIC_PATH = "/api/public/subscription-plans";
const REGISTER_PATH = "/api/public/register";

export async function fetchActivePlans(): Promise<SubscriptionPlanDto[]> {
  const response = await api.get<SubscriptionPlanDto[]>(PLANS_PUBLIC_PATH);
  return response.data;
}

export async function registerOwner(
  payload: RegistrationPayload
): Promise<RegistrationResponse> {
  const response = await api.post<RegistrationResponse>(
    REGISTER_PATH,
    payload
  );
  return response.data;
}

