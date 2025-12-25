import type React from "react"
import type { Metadata } from "next"
import { Comfortaa } from "next/font/google"
import { Analytics } from "@vercel/analytics/next"
import "./globals.css"

const _comfortaa = Comfortaa({ subsets: ["latin", "cyrillic"], weight: ["400", "700"] })

export const metadata: Metadata = {
  title: "№59 Мектеп - Гимназия",
  description: "Белім Мектебі - білік беру, ынамдылық және жетістік",
  icons: {
    icon: [
      {
        url: "/icon-light-32x32.png",
        media: "(prefers-color-scheme: light)",
      },
      {
        url: "/icon-dark-32x32.png",
        media: "(prefers-color-scheme: dark)",
      },
      {
        url: "/icon.svg",
        type: "image/svg+xml",
      },
    ],
    apple: "/apple-icon.png",
  },
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="kk">
      <body className={`font-sans antialiased`}>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
