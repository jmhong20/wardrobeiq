import client from './client'

export const logWear = (data) => client.post('/wear-logs/', data)
export const getWearHistory = (limit = 50) => client.get('/wear-logs/', { params: { limit } })
