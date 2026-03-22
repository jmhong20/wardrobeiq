/**
 * A GitHub-style contribution heatmap showing the last `days` days of wear logs.
 */
export default function WearCalendar({ data, days = 90 }) {
  const countByDate = {}
  for (const { date, count } of data) countByDate[date] = count

  // Build array of the last `days` dates
  const cells = []
  const today = new Date()
  for (let i = days - 1; i >= 0; i--) {
    const d = new Date(today)
    d.setDate(today.getDate() - i)
    const key = d.toISOString().slice(0, 10)
    cells.push({ date: key, count: countByDate[key] || 0 })
  }

  const maxCount = Math.max(...cells.map((c) => c.count), 1)

  const intensity = (count) => {
    if (count === 0) return 'var(--border)'
    const ratio = count / maxCount
    if (ratio < 0.25) return '#c7d2fe'
    if (ratio < 0.5) return '#818cf8'
    if (ratio < 0.75) return '#6366f1'
    return '#4338ca'
  }

  // Split into weeks (columns)
  const weeks = []
  for (let i = 0; i < cells.length; i += 7) {
    weeks.push(cells.slice(i, i + 7))
  }

  return (
    <div className="calendar-wrap">
      <div className="calendar-grid">
        {weeks.map((week, wi) => (
          <div key={wi} className="calendar-col">
            {week.map((cell) => (
              <div
                key={cell.date}
                className="calendar-cell"
                title={`${cell.date}: ${cell.count} wear${cell.count !== 1 ? 's' : ''}`}
                style={{ background: intensity(cell.count) }}
              />
            ))}
          </div>
        ))}
      </div>
      <div className="calendar-legend">
        <span>Less</span>
        {['var(--border)', '#c7d2fe', '#818cf8', '#6366f1', '#4338ca'].map((c) => (
          <div key={c} className="calendar-cell" style={{ background: c }} />
        ))}
        <span>More</span>
      </div>
    </div>
  )
}
