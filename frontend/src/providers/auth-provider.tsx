"use client";

import React from "react";

interface AuthProviderProps {
  children: React.ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  // Better Auth handles its own context via hooks
  // This provider is a placeholder for additional auth-related context if needed
  return <>{children}</>;
}
