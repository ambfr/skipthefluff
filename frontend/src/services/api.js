import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
})

export const rankVideos = async (query, intent = 'beginner') => {
  const response = await api.get('/rank', {
    params: { query, intent }
  })
  return response.data
}

export default api
