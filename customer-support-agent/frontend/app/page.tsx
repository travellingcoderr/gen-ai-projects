'use client';

import { useEffect, useState } from 'react';

type Health = {
  status: string;
  environment: string;
};

export default function HomePage() {
  const [health, setHealth] = useState<Health>({ status: 'loading', environment: 'unknown' });

  useEffect(() => {
    const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

    fetch(`${apiUrl}/api/health`)
      .then((response) => {
        if (!response.ok) {
          throw new Error('backend health request failed');
        }
        return response.json() as Promise<Health>;
      })
      .then((data) => setHealth(data))
      .catch(() => setHealth({ status: 'offline', environment: 'unknown' }));
  }, []);

  return (
    <main>
      <h1>customer-support-agent</h1>
      <p>Full-stack app with Python backend and Next.js frontend.</p>
      <p>
        Backend status: <strong>{health.status}</strong>
      </p>
      <p>
        Environment: <strong>{health.environment}</strong>
      </p>
    </main>
  );
}
