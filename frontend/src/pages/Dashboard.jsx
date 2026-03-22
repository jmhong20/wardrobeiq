import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import {
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer,
} from 'recharts'
import {
  getSummary, getByCategory, getByStyle,
  getNeverWorn, getMostWorn, getGaps,
  getWearCalendar, exportWardrobe,
} from '../api/stats'
import WearCalendar from '../components/WearCalendar'

const STYLE_COLORS = ['#4f46e5', '#7c3aed', '#db2777', '#ea580c', '#ca8a04', '#16a34a', '#0891b2']

function StatCard({ label, value, sub }) {
  return (
    <div className="stat-card">
      <p className="stat-value">{value}</p>
      <p className="stat-label">{label}</p>
      {sub && <p className="stat-sub">{sub}</p>}
    </div>
  )
}

function Section({ title, children }) {
  return (
    <section className="dash-section">
      <h2 className="dash-section-title">{title}</h2>
      {children}
    </section>
  )
}

function StyleBreakdown({ styles }) {
  if (!styles.length) return <p className="muted">Tag your items with style tags to see this.</p>
  const max = Math.max(...styles.map((s) => s.count))
  return (
    <div className="style-breakdown">
      {styles.map((s, i) => (
        <div key={s.style} className="style-row">
          <span className="style-name">{s.style}</span>
          <div className="style-bar-track">
            <div
              className="style-bar-fill"
              style={{ width: `${(s.count / max) * 100}%`, background: STYLE_COLORS[i % STYLE_COLORS.length] }}
            />
          </div>
          <span className="style-count">{s.count}</span>
        </div>
      ))}
    </div>
  )
}

export default function Dashboard() {
  const [summary, setSummary] = useState(null)
  const [categories, setCategories] = useState([])
  const [styles, setStyles] = useState([])
  const [neverWorn, setNeverWorn] = useState([])
  const [mostWorn, setMostWorn] = useState([])
  const [gaps, setGaps] = useState([])
  const [calendar, setCalendar] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      getSummary(),
      getByCategory(),
      getByStyle(),
      getNeverWorn(),
      getMostWorn(),
      getGaps(),
      getWearCalendar(),
    ]).then(([s, cat, sty, nw, mw, g, cal]) => {
      setSummary(s.data)
      setCategories(cat.data)
      setStyles(sty.data)
      setNeverWorn(nw.data)
      setMostWorn(mw.data)
      setGaps(g.data)
      setCalendar(cal.data)
    }).finally(() => setLoading(false))
  }, [])

  const handleExport = async (format) => {
    const res = await exportWardrobe(format)
    const url = URL.createObjectURL(res.data)
    const a = document.createElement('a')
    a.href = url
    a.download = `wardrobe.${format}`
    a.click()
    URL.revokeObjectURL(url)
  }

  if (loading) return <div className="page-center">Loading dashboard…</div>

  return (
    <div className="page">
      <div className="page-header">
        <h1>Dashboard</h1>
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button className="btn-ghost" onClick={() => handleExport('json')}>Export JSON</button>
          <button className="btn-ghost" onClick={() => handleExport('csv')}>Export CSV</button>
        </div>
      </div>

      <div className="stat-grid">
        <StatCard label="Total items" value={summary.total_items} />
        <StatCard label="Items worn" value={summary.total_worn} sub={`${summary.total_never_worn} never worn`} />
        <StatCard label="Total wears" value={summary.total_wears} />
        <StatCard label="Avg. favorability" value={`${summary.avg_favorability} ★`} />
      </div>

      <div className="dash-charts-row">
        <Section title="By Category">
          {categories.length === 0
            ? <p className="muted">No data yet.</p>
            : (
              <ResponsiveContainer width="100%" height={200}>
                <BarChart data={categories} margin={{ top: 4, right: 8, left: -20, bottom: 0 }}>
                  <XAxis dataKey="category" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} allowDecimals={false} />
                  <Tooltip />
                  <Bar dataKey="count" fill="#4f46e5" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            )
          }
        </Section>

        <Section title="By Style">
          <StyleBreakdown styles={styles} />
        </Section>
      </div>

      {gaps.length > 0 && (
        <Section title="⚠️ Wardrobe Gaps">
          <div className="gaps-list">
            {gaps.map((g, i) => (
              <div key={i} className="gap-item">
                <span className="gap-category">{g.category}</span>
                <span className="gap-msg">{g.message}</span>
                <Link to="/wardrobe/add" className="btn-primary gap-cta">Add</Link>
              </div>
            ))}
          </div>
        </Section>
      )}

      {mostWorn.length > 0 && (
        <Section title="Most Worn">
          <div className="item-row">
            {mostWorn.map((item) => (
              <Link key={item.id} to={`/wardrobe/${item.id}`} className="mini-card">
                <div className="mini-card-img">
                  {item.image_path ? <img src={item.image_path} alt={item.name} /> : <span>👔</span>}
                </div>
                <p className="mini-card-name">{item.name}</p>
                <p className="mini-card-sub">{item.wear_count}× worn</p>
              </Link>
            ))}
          </div>
        </Section>
      )}

      {neverWorn.length > 0 && (
        <Section title={`Never Worn (${neverWorn.length})`}>
          <div className="item-row">
            {neverWorn.slice(0, 6).map((item) => (
              <Link key={item.id} to={`/wardrobe/${item.id}`} className="mini-card mini-card--unworn">
                <div className="mini-card-img">
                  {item.image_path ? <img src={item.image_path} alt={item.name} /> : <span>👔</span>}
                </div>
                <p className="mini-card-name">{item.name}</p>
                <p className="mini-card-sub">{item.category}</p>
              </Link>
            ))}
          </div>
        </Section>
      )}

      <Section title="Wear History (last 90 days)">
        {calendar.length === 0
          ? <p className="muted">No wears logged yet — hit "Log a Wear" on any item.</p>
          : <WearCalendar data={calendar} />
        }
      </Section>
    </div>
  )
}
