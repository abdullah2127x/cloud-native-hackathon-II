"use client";

import React from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { signInSchema, type SignInInput } from "@/lib/validations/auth";
import { signIn, fetchAndStoreJwt } from "@/lib/auth-client";
import { Button } from "@/components/ui/Button";
import { Input } from "@/components/ui/Input";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import Link from "next/link";

export function SignInForm() {
  const router = useRouter();
  const [error, setError] = React.useState<string>("");
  const [isLoading, setIsLoading] = React.useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SignInInput>({
    resolver: zodResolver(signInSchema),
  });

  const onSubmit = async (data: SignInInput) => {
    try {
      setIsLoading(true);
      setError("");

      const result = await signIn.email(
        {
          email: data.email,
          password: data.password,
        },
        {
          onSuccess: async () => {
            // Fetch and store JWT for API calls
            await fetchAndStoreJwt();
            toast.success("Signed in successfully");
            router.push("/dashboard");
          },
          onError: (ctx) => {
            const errorMessage = ctx.error.message || "Failed to sign in";
            const statusCode = ctx.error.status;
            const errorCode = (ctx.error as { code?: string })?.code;

            // Handle specific error cases
            if (
              errorMessage.toLowerCase().includes("credential account not found") ||
              errorMessage.toLowerCase().includes("account not found") ||
              errorMessage.toLowerCase().includes("user not found")
            ) {
              setError("No account found with this email. Please sign up first.");
              toast.error("Account not found", {
                description: "Would you like to create an account?",
                action: {
                  label: "Sign Up",
                  onClick: () => {
                    toast.dismiss();
                    router.push("/sign-up");
                  },
                },
                duration: 5000,
              });
            } else if (
              errorMessage.toLowerCase().includes("invalid password") ||
              errorMessage.toLowerCase().includes("incorrect password")
            ) {
              setError("Incorrect password. Please try again.");
              toast.error("Invalid password");
            } else if (errorMessage.toLowerCase().includes("invalid email")) {
              setError("Please enter a valid email address.");
              toast.error("Invalid email");
            } else if (statusCode === 401) {
              setError("Invalid email or password.");
              toast.error("Authentication failed", {
                description: "Please check your credentials and try again.",
              });
            } else {
              setError(errorMessage);
              toast.error("Sign in failed", {
                description: errorMessage,
              });
            }
          },
        }
      );
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to sign in";
      setError(errorMessage);
      toast.error("An unexpected error occurred");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
      <Input
        // label="Email"
        placeholder="abdullah2127x@gmail.com"
        type="email"
        {...register("email")}
        // error={errors.email?.message}
        disabled={isLoading}
      />

      <Input
        // label="Password"
        placeholder="Your password"
        type="password"
        {...register("password")}
        // error={errors.password?.message}
        disabled={isLoading}
      />

      {error && (
        // T011: Use semantic error color variables instead of hardcoded red
        <div
          className="rounded-lg border p-3 text-sm"
          style={{
            borderColor: "var(--error-border)",
            backgroundColor: "var(--error-bg)",
            color: "var(--error-text)",
          }}
        >
          {error}
        </div>
      )}

      <Button type="submit" className="w-full cursor-pointer" disabled={isLoading}>
        {isLoading ? "Signing in..." : "Sign in"}
      </Button>

      <p className="text-center text-sm" style={{ color: "var(--foreground)" }}>
        Don&apos;t have an account?{" "}
        {/* T013: Use semantic link color variables */}
        <Link
          href="/sign-up"
          className="font-medium"
          style={{
            color: "var(--link-text)",
            textDecoration: "none",
          }}
          onMouseEnter={(e) => {
            (e.target as HTMLElement).style.color = "var(--link-text-hover)";
          }}
          onMouseLeave={(e) => {
            (e.target as HTMLElement).style.color = "var(--link-text)";
          }}
        >
          Sign up
        </Link>
      </p>
    </form>
  );
}
