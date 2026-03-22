import client from './client'

export const getOutfits = () => client.get('/outfits/')
export const createOutfit = (data) => client.post('/outfits/', data)
export const rateOutfit = (id, rating) => client.post(`/outfits/${id}/rate?rating=${rating}`)
