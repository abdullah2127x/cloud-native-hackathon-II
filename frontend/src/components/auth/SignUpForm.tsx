"use client";

import React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { signUpSchema, type SignUpInput } from "@/lib/validations/auth";
import { signUp, fetchAndStoreJwt } from "@/lib/auth-client";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import Link from "next/link";

export function SignUpForm() {
  const router = useRouter();
  const [error, setError] = React.useState<string>("");
  const [isLoading, setIsLoading] = React.useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SignUpInput>({
    resolver: zodResolver(signUpSchema),
    mode: "onBlur", // Validate on blur to show errors earlier
  });

  const onSubmit = async (data: SignUpInput) => {
    try {
      setIsLoading(true);
      setError("");

      const result = await signUp.email(
        {
          email: data.email,
          password: data.password,
          name: data.name,
        },
        {
          onSuccess: async () => {
            // Fetch and store JWT for API calls
            await fetchAndStoreJwt();
            toast.success("Account created successfully");
            router.push("/dashboard");
          },
          onError: (ctx) => {
            const errorMessage = ctx.error.message || "Failed to create account";
            const statusCode = ctx.error.status;
            const errorCode = (ctx.error as { code?: string })?.code;

            // Handle specific error cases
            if (
              errorCode === "USER_ALREADY_EXISTS" ||
              statusCode === 422 ||
              errorMessage.toLowerCase().includes("already exists") ||
              errorMessage.toLowerCase().includes("user already exists")
            ) {
              setError("An account with this email already exists.");
              toast.error("Account already exists", {
                description: "Would you like to sign in instead?",
                action: {
                  label: "Sign In",
                  onClick: () => {
                    toast.dismiss();
                    router.push("/sign-in");
                  },
                },
                duration: 5000,
              });
            } else if (errorMessage.toLowerCase().includes("invalid email")) {
              setError("Please enter a valid email address.");
              toast.error("Invalid email");
            } else if (errorMessage.toLowerCase().includes("password")) {
              setError("Password must be at least 8 characters long.");
              toast.error("Invalid password");
            } else {
              setError(errorMessage);
              toast.error("Sign up failed", {
                description: errorMessage,
              });
            }
          },
        }
      );
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to create account";
      setError(errorMessage);
      toast.error("An unexpected error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <Input
        // label="Name"
        {...register("name")}
        // error={errors.name?.message}
        disabled={isLoading}
      />

      <Input
        // label="Email"
        type="email"
        {...register("email")}
        // error={errors.email?.message}
        disabled={isLoading}
      />

      <Input
        // label="Password"
        type="password"
        {...register("password")}
        // error={errors.password?.message}
        disabled={isLoading}
        placeholder="Minimum 8 characters"
      />

      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-3 text-sm text-red-600">
          {error}
        </div>
      )}

      <Button type="submit" className="w-full" disabled={isLoading}>
        {isLoading ? "Creating account..." : "Create account"}
      </Button>

      <p className="text-center text-sm text-gray-600">
        Already have an account?{" "}
        <Link href="/sign-in" className="font-medium text-blue-600 hover:text-blue-500">
          Sign in
        </Link>
      </p>
    </form>
  );
}
