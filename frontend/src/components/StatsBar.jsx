import React from 'react'

export default function StatsBar({ count, query, topScore }) {
  if (!query) return null

  return (
    <div className="w-full border-t border-pink-100 mt-8 pt-6 grid grid-cols-4 gap-4 text-center">
      {[
        { value: topScore ? Math.round(topScore) : '—', label: 'Top score' },
        { value: count || '—', label: 'Analyzed' },
        { value: '—', label: 'Comments read' },
        { value: '~3s', label: 'Analysis time' },
      ].map((stat) => (
        <div key={stat.label}>
          <div className="text-2xl font-bold text-gray-900">{stat.value}</div>
          <div className="text-xs text-gray-400 mt-0.5">{stat.label}</div>
        </div>
      ))}
    </div>
  )
}
