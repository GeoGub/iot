'use client';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

const queryClient = new QueryClient();

export default function Layout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <div className="f">
        <QueryClientProvider client={queryClient}>
          {children}
        </QueryClientProvider>
    </div>
  )
}