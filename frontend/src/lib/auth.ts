// Better Auth server configuration
import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";
import { Pool } from "@neondatabase/serverless";

const pool = new Pool({ connectionString: process.env.DATABASE_URL });

export const auth = betterAuth({
  database: pool,
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // Simplified for development
  },
  secret: process.env.BETTER_AUTH_SECRET || "your-secret-key-change-in-production",
  trustedOrigins: [
    process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000",
  ],
  plugins: [
    jwt({
      jwks: {
        jwksPath: "/.well-known/jwks.json",
      },
    }),
  ],
});

export type Session = typeof auth.$Infer.Session;


// src/lib/auth.ts  (or wherever you export auth)

// import { betterAuth } from "better-auth";
// import { jwt } from "better-auth/plugins";
// import { Pool } from "@neondatabase/serverless";

// const pool = new Pool({ connectionString: process.env.DATABASE_URL });

// export const auth = betterAuth({
//   database: pool,
//   emailAndPassword: {
//     enabled: true,
//     requireEmailVerification: false,
//   },
//   secret: process.env.BETTER_AUTH_SECRET || "your-secret-key-change-in-production",

//   // Keep this — very important for Origin validation
//   trustedOrigins: [
//     "http://localhost:3000",
//     "https://ai-todo-web-app.vercel.app",
//     // Add your ngrok URL here too during testing
//     // e.g. "https://xxxxxx.ngrok-free.app"
//   ],

//   plugins: [
//     jwt({
//       jwks: {
//         jwksPath: "/.well-known/jwks.json",
//       },
//     }),
//   ],

//   // ────────────────────────────────────────────────
//   //  This is the most important part you're missing
//   // ────────────────────────────────────────────────
//   advanced: {
//     // Force secure cookies even in development (ngrok is https)
//     useSecureCookies: true,

//     // This sets the default attributes for ALL cookies
//     defaultCookieAttributes: {
//       sameSite: "none",     // ← critical for cross-origin
//       secure: true,         // ← required when sameSite = none
//       httpOnly: true,
//       path: "/",
//     },

//     // Optional: override just the session cookie (more explicit)
//     cookies: {
//       session_token: {
//         attributes: {
//           sameSite: "none",
//           secure: true,
//           httpOnly: true,
//           path: "/",
//         },
//       },
//     },
//   },
// });

// export type Session = typeof auth.$Infer.Session;