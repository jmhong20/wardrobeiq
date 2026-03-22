import { useEffect, useState } from 'react'
import client from '../api/client'

export default function Home() {
  const [status, setStatus] = useState(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    client
      .get('/health')
      .then((res) => setStatus(res.data))
      .catch((err) => setError(err.message))
  }, [])

  return (
    <main style={{ padding: '2rem', maxWidth: '640px', margin: '0 auto' }}>
      <h1>👔 WardrobeIQ</h1>
      <p style={{ marginTop: '0.5rem', color: '#555' }}>
        Intelligent wardrobe management &amp; outfit recommendations.
      </p>

      <section style={{ marginTop: '2rem', padding: '1rem', border: '1px solid #ddd', borderRadius: '8px' }}>
        <h2 style={{ fontSize: '1rem', marginBottom: '0.5rem' }}>API Status</h2>
        {error && <p style={{ color: 'red' }}>Error: {error}</p>}
        {!status && !error && <p style={{ color: '#888' }}>Connecting to backend…</p>}
        {status && (
          <pre style={{ background: '#f5f5f5', padding: '0.75rem', borderRadius: '4px' }}>
            {JSON.stringify(status, null, 2)}
          </pre>
        )}
      </section>

      <nav style={{ marginTop: '2rem' }}>
        <p style={{ color: '#888', fontSize: '0.9rem' }}>
          Phase 0 skeleton — more coming in Phase 1.
        </p>
      </nav>
    </main>
  )
}
