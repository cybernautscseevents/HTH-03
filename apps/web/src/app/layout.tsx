import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ClinScribe AI — Ambient Clinical Intelligence for Indian OPDs",
  description: "From Conversation to Clinical Intelligence. Ambient clinical documentation with multilingual code-mixed understanding, zero-hallucination evidence grounding, and safety guardrails.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full bg-slate-950 text-slate-100 antialiased">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet" />
      </head>
      <body className="min-h-full flex flex-col font-sans bg-slate-950 text-slate-100 selection:bg-teal-500/30 selection:text-teal-200">
        {children}
      </body>
    </html>
  );
}
