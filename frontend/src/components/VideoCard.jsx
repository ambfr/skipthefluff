import React from 'react'

function formatViews(views) {
  if (!views) return '—'
  if (views >= 1_000_000) return `${(views / 1_000_000).toFixed(1)}M views`
  if (views >= 1_000) return `${(views / 1_000).toFixed(1)}K views`
  return `${views} views`
}

function formatDuration(iso) {
  if (!iso) return '—'
  const match = iso.match(/PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/)
  if (!match) return '—'
  const h = parseInt(match[1] || 0)
  const m = parseInt(match[2] || 0)
  const s = parseInt(match[3] || 0)
  if (h > 0) return `${h}h ${m}m`
  return `${m}m ${s.toString().padStart(2, '0')}s`
}

export default function VideoCard({ video }) {
  const { title, channel, views, duration, thumbnail_url, video_id, score, label, rank, ai_tag } = video

  return (
    <div className={`bg-white rounded-2xl p-4 flex gap-4 transition-shadow hover:shadow-md ${
      rank === 0 ? 'border-2 border-[#E8294C]' : 'border border-pink-100'
    }`}>
      {/* Thumbnail */}
      <a href={`https://youtube.com/watch?v=${video_id}`} target="_blank" rel="noopener noreferrer" className="flex-shrink-0">
        <div className="w-28 h-20 rounded-xl overflow-hidden bg-pink-100 flex items-center justify-center">
          {thumbnail_url ? (
            <img src={thumbnail_url} alt={title} className="w-full h-full object-cover" />
          ) : (
            <div className="w-full h-full bg-pink-200 flex items-center justify-center">
              <div className="w-8 h-8 rounded-full bg-[#E8294C] flex items-center justify-center">
                <svg width="10" height="12" viewBox="0 0 10 12" fill="none">
                  <path d="M1 1L9 6L1 11V1Z" fill="white" />
                </svg>
              </div>
            </div>
          )}
        </div>
      </a>

      {/* Info */}
      <div className="flex-1 min-w-0">
        {/* Title + label */}
        <div className="flex items-start justify-between gap-2 mb-1">
          <a href={`https://youtube.com/watch?v=${video_id}`} target="_blank" rel="noopener noreferrer"
            className="text-sm font-semibold text-gray-900 leading-snug hover:text-[#E8294C] transition line-clamp-2"
            style={{fontFamily: "'Playfair Display', serif"}}>
            {title}
          </a>
          {label && (
            <span className="flex-shrink-0 text-xs bg-pink-50 text-[#E8294C] border border-pink-200 px-2.5 py-1 rounded-full font-medium whitespace-nowrap">
              {label}
            </span>
          )}
        </div>

        {/* Meta */}
        <div className="flex items-center gap-3 text-xs text-gray-400 mb-2.5">
          <span className="flex items-center gap-1">
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
              <circle cx="5" cy="3" r="2" stroke="currentColor" strokeWidth="1.2"/>
              <path d="M1 9C1 7.343 2.343 6 4 6H6C7.657 6 9 7.343 9 9" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
            </svg>
            {channel}
          </span>
          <span className="flex items-center gap-1">
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
              <circle cx="5" cy="5" r="4" stroke="currentColor" strokeWidth="1.2"/>
              <path d="M5 3V5.5L6.5 7" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round"/>
            </svg>
            {formatDuration(duration)}
          </span>
          <span className="flex items-center gap-1">
            <svg width="10" height="10" viewBox="0 0 10 10" fill="none">
              <path d="M1 5C1 5 2.5 2 5 2C7.5 2 9 5 9 5C9 5 7.5 8 5 8C2.5 8 1 5 1 5Z" stroke="currentColor" strokeWidth="1.2"/>
              <circle cx="5" cy="5" r="1.5" stroke="currentColor" strokeWidth="1.2"/>
            </svg>
            {formatViews(views)}
          </span>
        </div>

        {/* Score bar */}
        <div className="flex items-center gap-2 mb-2">
          <span className="text-xs text-gray-400 italic">Score</span>
          <div className="flex-1 h-1.5 bg-pink-100 rounded-full overflow-hidden">
            <div
              className="h-full bg-[#E8294C] rounded-full transition-all duration-500"
              style={{width: `${Math.min(score, 100)}%`}}
            />
          </div>
          <span className="text-xs font-semibold text-gray-700">{Math.round(score)}</span>
        </div>

        {/* AI tag chip */}
        {ai_tag && (
          <div className="flex gap-1.5 flex-wrap">
            <span className="text-xs border border-pink-200 text-gray-500 px-2 py-0.5 rounded-full">
              ✓ {ai_tag}
            </span>
          </div>
        )}
      </div>
    </div>
  )
}
