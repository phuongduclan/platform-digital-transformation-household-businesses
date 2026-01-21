"use client";

import {
  createContext,
  useContext,
  useState,
  type ReactNode,
  useMemo
} from "react";
import type { RegistrationPayload } from "@/lib/api";

type HouseholdForm = RegistrationPayload["household"];
type OwnerForm = RegistrationPayload["owner_account"];

type RegistrationState = {
  planId: number | null;
  household: HouseholdForm;
  owner: OwnerForm & { confirmPassword?: string };
};

type RegistrationContextValue = {
  state: RegistrationState;
  setPlanId: (id: number) => void;
  updateHousehold: (data: Partial<HouseholdForm>) => void;
  updateOwner: (data: Partial<OwnerForm & { confirmPassword?: string }>) => void;
  reset: () => void;
};

const RegistrationContext = createContext<RegistrationContextValue | undefined>(
  undefined
);

const defaultState: RegistrationState = {
  planId: null,
  household: {
    name: "",
    tax_code: "",
    phone: "",
    address: "",
    description: ""
  },
  owner: {
    user_name: "",
    password: "",
    confirmPassword: "",
    email: "",
    description: ""
  }
};

export function RegistrationProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<RegistrationState>(defaultState);

  const value = useMemo<RegistrationContextValue>(
    () => ({
      state,
      setPlanId: id => setState(prev => ({ ...prev, planId: id })),
      updateHousehold: data =>
        setState(prev => ({ ...prev, household: { ...prev.household, ...data } })),
      updateOwner: data =>
        setState(prev => ({ ...prev, owner: { ...prev.owner, ...data } })),
      reset: () => setState(defaultState)
    }),
    [state]
  );

  return (
    <RegistrationContext.Provider value={value}>
      {children}
    </RegistrationContext.Provider>
  );
}

export function useRegistration() {
  const ctx = useContext(RegistrationContext);
  if (!ctx) {
    throw new Error("useRegistration must be used within RegistrationProvider");
  }
  return ctx;
}

