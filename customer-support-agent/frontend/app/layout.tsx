export const metadata = {
  title: 'customer-support-agent',
  description: 'Full-stack app with Python backend and Next.js frontend.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ fontFamily: 'sans-serif', margin: 0, padding: 24 }}>{children}</body>
    </html>
  );
}
