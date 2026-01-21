"use client";

import { RegistrationProvider } from "@/context/registration-context";
import type { ReactNode } from "react";

export function RegisterProviders({ children }: { children: ReactNode }) {
  return <RegistrationProvider>{children}</RegistrationProvider>;
}

