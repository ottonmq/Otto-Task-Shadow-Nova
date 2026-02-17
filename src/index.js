import { serve } from '@hono/node-server'
import app from './app.js'

console.log('🏮 Otto-Task Engine v2.0 Activated');
console.log('🚀 Accede en: http://localhost:3000');

serve({
  fetch: app.fetch,
  port: 3000
})
