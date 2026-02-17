****# 🔒 Política de Seguridad - Otto-Task

## Escaneo de Seguridad Activo

Este proyecto implementa múltiples capas de escaneo de seguridad automático:

### 1. SAST (Static Application Security Testing)
- Análisis estático de código Python
- Detecta vulnerabilidades comunes (inyección SQL, XSS, etc.)
- Se ejecuta en cada commit

### 2. Dependency Scanning
- Verifica vulnerabilidades en dependencias
- Analiza `requirements.txt` y `Pipfile`
- Alerta sobre librerías desactualizadas

### 3. Secret Detection
- Detecta credenciales, tokens y claves expuestas
- Previene commits con secretos
- Excluye directorios de documentación

### 4. Container Scanning
- Analiza imágenes Docker si se utilizan
- Detecta vulnerabilidades en capas de contenedor

## Riesgos Identificados y Mitigaciones

### ⚠️ CRÍTICO: SOCIALACCOUNT_LOGIN_ON_GET = True
**Riesgo:** Permite login mediante GET requests (CSRF vulnerable)
**Acción requerida:** Cambiar a `False` en producción

```python
# ❌ INSEGURO
SOCIALACCOUNT_LOGIN_ON_GET = True

# ✅ SEGURO
SOCIALACCOUNT_LOGIN_ON_GET = False
```

### ⚠️ ALTO: Sin validación de entrada
**Recomendación:** Implementar validación de datos en todos los endpoints

### ⚠️ MEDIO: Credenciales en código
**Recomendación:** Usar variables de entorno y GitLab CI/CD secrets

## Reportes de Seguridad

Los reportes se generan automáticamente en cada pipeline:
- `gl-sast-report.json` - Vulnerabilidades de código
- `gl-dependency-scanning-report.json` - Dependencias vulnerables
- `gl-secret-detection-report.json` - Secretos expuestos
- `gl-container-scanning-report.json` - Vulnerabilidades de contenedor

## Próximos Pasos

1. ✅ Revisar y corregir `settings.py`
2. ✅ Crear `requirements.txt` con dependencias pinned
3. ✅ Implementar validación de entrada
4. ✅ Configurar branch protection rules
5. ✅ Habilitar MR approval para cambios de seguridad

---

*Última actualización: 2026-02-12*
