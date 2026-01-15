import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "2025 연말정산 계산기",
  description: "2025년 개정 세법 반영 연말정산 세액 계산기",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="ko">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
