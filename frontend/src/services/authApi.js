import api from './api'

export const signup = async (email, password, name) => {
  const res = await api.post('/auth/signup', { email, password, name })
  return res.data
}

export const login = async (email, password) => {
  const res = await api.post('/auth/login', { email, password })
  return res.data
}

export const googleLogin = async (idToken) => {
  const res = await api.post('/auth/google', null, {
    params: { id_token: idToken }
  })
  return res.data
}

export const getMe = async () => {
  const token = localStorage.getItem('smarttube_token')
  const res = await api.get('/auth/me', {
    headers: { Authorization: `Bearer ${token}` }
  })
  return res.data
}
