import { Hono } from 'hono'
import { html } from 'hono/html'

const app = new Hono()

// 🔑 CONFIGURACIÓN SHADOW
const TELEGRAM_TOKEN = "8342284695:AAER9lizZV19oAIky4t80JbpA9gnXUT5Jl0"
const CHAT_ID = "5368383321"
const NOMBRE_ARQUITECTO = "Otto Napoleon Mendoza Quant"

// 📡 WEBHOOK PARA GITLAB
app.post('/webhook/gitlab', async (c) => {
  try {
    const body = await c.req.json()
    const commits = body.commits || []
    const repository = body.repository?.name || "Otto-Task"
        
    for (const commit of commits) {
      const text = `🚨 <b>[SHADOW ARCHITECT ALERT]</b>\n\n👤 <b>Arquitecto:</b> ${NOMBRE_ARQUITECTO}\n📦 <b>Proyecto:</b> ${repository}\n🛠 <b>Commit:</b> <code>${commit.id.substring(0, 8)}</code>\n📝 <b>Mensaje:</b> ${commit.message}`
      
      await fetch(`https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: CHAT_ID, text: text, parse_mode: 'HTML' })
      })
    }
    return c.json({ status: 'sentinel_notified' })
  } catch (err) {
    return c.json({ error: 'Error en el pulso', details: err.message }, 500)
  }
})

// 🌐 INTERFAZ VISUAL
app.get('/', (c) => {
  return c.html(
    html`<!DOCTYPE html>
    <html>
    <head>
        <title>OTTO-TASK // SHADOW</title>
        <style>
            body { background: #050505; color: #00f3ff; font-family: 'Courier New', monospace; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; overflow: hidden; }
            .frame { border: 2px solid #00f3ff; padding: 40px; box-shadow: 0 0 20px #00f3ff; background: rgba(0,0,0,0.9); width: 80%; position: relative; }
            .scan { position: absolute; width: 100%; height: 2px; background: #00f3ff; top: 0; left: 0; animation: s 3s infinite; box-shadow: 0 0 10px #00f3ff; }
            @keyframes s { 0% { top: 0; } 100% { top: 100%; } }
            .terminal { background: #000; color: #00ff41; padding: 15px; border: 1px solid #00ff41; margin-top: 20px; height: 100px; overflow: auto; font-size: 0.8em; }
        </style>
    </head>
    <body>
        <div class="frame">
            <div class="scan"></div>
            <h1>SHADOW ARCHITECT ACTIVE</h1>
            <p>ARQUITECTO: <strong>${NOMBRE_ARQUITECTO}</strong></p>
            <div class="terminal">>> [SYSTEM] Sentinel Online...<br>>> Esperando señal de GitLab...</div>
        </div>
    </body>
    </html>`
  )
})

export default app
