import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "AutoExam LK",
  description:
    "Model exam papers and marking schemes for Sri Lankan examinations",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
