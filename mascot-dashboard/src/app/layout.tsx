import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Orbit 🤖 Senior Principal Mascot Director | HSF Dashboard',
  description: 'Robotic Command Console, Autonomous Design Pattern & Frontend Aesthetic Engine, and 5-Person Squad Orchestrator',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#070a0f] text-slate-100 min-h-screen antialiased selection:bg-[#00f59b] selection:text-[#070a0f]">
        {children}
      </body>
    </html>
  );
}
