import { Stack } from '@chakra-ui/react';
import type { Metadata } from 'next';
// import { Geist, Geist_Mono } from 'next/font/google';
import './globals.css';
import React from 'react';

import Providers from '@/components/providers';

// const geistSans = Geist({
//   variable: '--font-geist-sans',
//   subsets: ['latin'],
// });

// const geistMono = Geist_Mono({
//   variable: '--font-geist-mono',
//   subsets: ['latin'],
// });

export const metadata: Metadata = {
  title: 'Temp',
  description: 'Hum',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning={true}>
      <body className={`antialiased`}>
        <Providers>
          <Stack
            p={{
              base: '40px 50px',
              md: '40px 100px',
              lg: '40px 200px',
            }}
            minH="100vh"
            h="100%"
          >
            {children}
          </Stack>
        </Providers>
      </body>
    </html>
  );
}