import React, { useState } from 'react'

const FILTERS = ['Beginner', 'Advanced', 'Quick summary', 'Detailed', 'Review', 'News']

export default function SearchBar({ onSearch, loading }) {
  const [query, setQuery] = useState('')
  const [activeFilter, setActiveFilter] = useState('Beginner')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (query.trim()) {
      onSearch(query.trim(), activeFilter.toLowerCase())
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleSubmit(e)
  }

  return (
    <div className="w-full max-w-2xl mx-auto">
      {/* Search input */}
      <div className="relative mb-3">
        <div className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <circle cx="7" cy="7" r="5.5" stroke="currentColor" strokeWidth="1.5" />
            <path d="M11 11L14 14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
          </svg>
        </div>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Search any topic — e.g. Learn Python"
          className="w-full bg-gray-900 text-white placeholder-gray-500 rounded-xl pl-10 pr-12 py-3.5 text-sm outline-none focus:ring-2 focus:ring-[#E8294C]/40 transition"
        />
        <button
          onClick={handleSubmit}
          disabled={loading}
          className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white transition"
        >
          <svg width="18" height="18" viewBox="0 0 18 18" fill="none">
            <path d="M3 9H15M15 9L10 4M15 9L10 14" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </button>
      </div>

      {/* Filter pills */}
      <div className="flex gap-2 flex-wrap">
        {FILTERS.map((filter) => (
          <button
            key={filter}
            onClick={() => setActiveFilter(filter)}
            className={`px-4 py-1.5 rounded-full text-sm font-medium border transition-all ${
              activeFilter === filter
                ? 'bg-[#E8294C] text-white border-[#E8294C]'
                : 'bg-white text-gray-600 border-gray-200 hover:border-[#E8294C] hover:text-[#E8294C]'
            }`}
          >
            {filter}
          </button>
        ))}
      </div>
    </div>
  )
}
