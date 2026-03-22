import client from './client'

export const getItems = (params = {}) =>
  client.get('/items/', { params })

export const getItem = (id) =>
  client.get(`/items/${id}`)

export const createItem = (formData) =>
  client.post('/items/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

export const updateItem = (id, data) =>
  client.patch(`/items/${id}`, data)

export const uploadImage = (id, formData) =>
  client.post(`/items/${id}/image`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })

export const deleteItem = (id) =>
  client.delete(`/items/${id}`)
