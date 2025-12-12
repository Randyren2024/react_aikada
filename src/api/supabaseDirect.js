import { createClient } from '@supabase/supabase-js'

const VITE_SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL
const VITE_SUPABASE_ANON_KEY = import.meta.env.VITE_SUPABASE_ANON_KEY

export const isSupabaseDirectEnabled = Boolean(VITE_SUPABASE_URL && VITE_SUPABASE_ANON_KEY)

const supabase = isSupabaseDirectEnabled ? createClient(VITE_SUPABASE_URL, VITE_SUPABASE_ANON_KEY) : null

export const uploadImageDirect = async (file, userId) => {
  if (!isSupabaseDirectEnabled) throw new Error('Supabase direct not configured')
  const ext = file.name && file.name.includes('.') ? `.${file.name.split('.').pop()}` : ''
  const path = `image/${userId}/${crypto.randomUUID()}${ext}`
  const { error } = await supabase.storage.from('image').upload(path, file, { contentType: file.type, upsert: true })
  if (error) throw new Error(error.message)
  const { data } = supabase.storage.from('image').getPublicUrl(path)
  return { url: data.publicUrl, path }
}

export const getSecretsDirect = async (userId, page = 1, pageSize = 10) => {
  if (!isSupabaseDirectEnabled) throw new Error('Supabase direct not configured')
  const offset = (page - 1) * pageSize
  const { data, count, error } = await supabase
    .from('secrets')
    .select('*', { count: 'exact' })
    .eq('user_id', userId)
    .order('created_at', { ascending: false })
    .range(offset, offset + pageSize - 1)
  if (error) throw new Error(error.message)
  return { data, total: count, page, pageSize }
}

export const createSecretDirect = async ({ user_id, content, image_url }) => {
  if (!isSupabaseDirectEnabled) throw new Error('Supabase direct not configured')
  const now = new Date().toISOString()
  const payload = { user_id, content, image_url, created_at: now, updated_at: now }
  const { data, error } = await supabase.from('secrets').insert(payload).select().single()
  if (error) throw new Error(error.message)
  return { data }
}
