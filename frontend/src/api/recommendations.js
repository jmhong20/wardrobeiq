import client from './client'

export const getSuggestions = (limit = 5, season = null) =>
  client.get('/recommendations/suggest', { params: { limit, ...(season && { season }) } })

export const getItemMatches = (itemId) =>
  client.get(`/recommendations/match/${itemId}`)
