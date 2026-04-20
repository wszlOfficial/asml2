import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ASML 2",
  description: "De website van ASML 2",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`font-sans h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
