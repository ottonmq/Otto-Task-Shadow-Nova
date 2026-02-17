# views.py - El Agente reportando su trabajo
def dashboard(request):
    # Esto simula lo que el Agente de GitLab ya analizó en tu código
    logs_del_agente = [
        {"timestamp": "18:45", "accion": "Escaneo de settings.py completado.", "resultado": "Vulnerabilidad detectada."},
        {"timestamp": "18:46", "accion": "Aplicando parche SECURITY_HSTS.", "resultado": "EXITO"},
        {"timestamp": "18:47", "accion": "Inyectando SOCIALACCOUNT_LOGIN_ON_GET = True.", "resultado": "SISTEMA BLINDADO"},
        {"timestamp": "18:50", "accion": "Vigilancia activa en túnel Cloudflare.", "resultado": "SIN INTRUSIONES"},
    ]
    
    context = {
        'logs': logs_del_agente,
        'agente_id': 'SHADOW_ARCHITECT_01',
        'arquitecto': 'OTTO NAPOLEON MENDOZA QUANT'
    }
    return render(request, 'dashboard.html', context)
