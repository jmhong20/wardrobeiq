import client from './client'

export const getSuggestions = (limit = 5, season = null) =>
  client.get('/recommendations/suggest', { params: { limit, ...(season && { season }) } })
