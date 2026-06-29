import React, { useState } from 'react'
import Header from './components/Header'
import SearchBar from './components/SearchBar'
import VideoCard from './components/VideoCard'
import StatsBar from './components/StatsBar'
import { rankVideos } from './services/api'

export default function App() {
  const [videos, setVideos] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [query, setQuery] = useState('')
  const [topScore, setTopScore] = useState(null)

  const handleSearch = async (q, intent) => {
    setLoading(true)
    setError(null)
    setQuery(q)
    try {
      const data = await rankVideos(q, intent)
      setVideos(data.results || [])
      setTopScore(data.top_score || null)
    } catch (err) {
      setError('Something went wrong. Please try again.')
      setVideos([])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#FFF0F3] flex flex-col">
      <Header />

      <main className="flex-1 max-w-2xl mx-auto w-full px-4 py-12">
        {/* Hero */}
        <div className="text-center mb-8">
          <div className="inline-flex items-center gap-1.5 bg-white border border-pink-100 text-xs text-gray-500 px-3 py-1 rounded-full mb-5">
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
              <path d="M5 1L6.2 3.8L9 4.1L7 6.1L7.5 9L5 7.5L2.5 9L3 6.1L1 4.1L3.8 3.8L5 1Z" fill="#E8294C" />
            </svg>
            AI-ranked video results
          </div>
          <h1 className="text-4xl font-bold text-gray-900 leading-tight mb-3"
            style={{fontFamily: "'Playfair Display', serif"}}>
            Find the{' '}
            <em className="text-[#E8294C] not-italic font-bold"
              style={{fontFamily: "'Playfair Display', serif", fontStyle: "italic"}}>
              best
            </em>{' '}
            video,<br />
            not just the most popular
          </h1>
          <p className="text-sm text-gray-500 max-w-sm mx-auto">
            SmartTube ranks YouTube results by quality, clarity, and credibility — not clicks.
          </p>
        </div>

        {/* Search */}
        <SearchBar onSearch={handleSearch} loading={loading} />

        {/* Results */}
        <div className="mt-8">
          {loading && (
            <div className="flex flex-col gap-3">
              {[1, 2, 3, 4].map((i) => (
                <div key={i} className="bg-white border border-pink-100 rounded-2xl p-4 flex gap-4 animate-pulse">
                  <div className="w-28 h-20 rounded-xl bg-pink-100 flex-shrink-0" />
                  <div className="flex-1 space-y-2 py-1">
                    <div className="h-3 bg-pink-100 rounded w-3/4" />
                    <div className="h-3 bg-pink-100 rounded w-1/2" />
                    <div className="h-2 bg-pink-50 rounded w-full mt-3" />
                  </div>
                </div>
              ))}
            </div>
          )}

          {error && (
            <div className="text-center py-10 text-sm text-red-500">{error}</div>
          )}

          {!loading && !error && videos.length > 0 && (
            <>
              <div className="flex items-center justify-between mb-3">
                <p className="text-xs text-gray-400">
                  Showing <span className="font-semibold text-gray-700">{videos.length} ranked results</span> for "{query}"
                </p>
                <button className="text-xs text-[#E8294C] flex items-center gap-1 font-medium">
                  <svg width="12" height="12" viewBox="0 0 12 12" fill="none">
                    <path d="M2 4h8M4 6h4M6 8h0" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
                  </svg>
                  Sort
                </button>
              </div>
              <div className="flex flex-col gap-3">
                {videos.map((video) => (
                  <VideoCard key={video.video_id} video={video} />
                ))}
              </div>
            </>
          )}

          {!loading && !error && videos.length === 0 && query && (
            <div className="text-center py-16 text-sm text-gray-400">
              No results found for "{query}". Try a different search.
            </div>
          )}
        </div>

        <StatsBar count={videos.length} query={query} topScore={topScore} />
      </main>

      <footer className="text-center text-xs text-gray-300 py-4 border-t border-pink-100">
        Powered by Groq + YouTube Data API
      </footer>
    </div>
  )
}
