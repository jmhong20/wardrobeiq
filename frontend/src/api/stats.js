import client from './client'

export const getSummary = () => client.get('/stats/summary')
export const getByCategory = () => client.get('/stats/by-category')
export const getByStyle = () => client.get('/stats/by-style')
export const getNeverWorn = () => client.get('/stats/never-worn')
export const getMostWorn = (limit = 5) => client.get('/stats/most-worn', { params: { limit } })
export const getGaps = () => client.get('/stats/gaps')
export const getWearCalendar = (days = 90) => client.get('/stats/wear-calendar', { params: { days } })
export const exportWardrobe = (format = 'json') =>
  client.get('/stats/export', { params: { format }, responseType: 'blob' })
