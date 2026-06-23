# ════════════════════════════════════════════════════════════
# Dockerfile — FinTech Nova API
# Sesión 13 - Laboratorio 3
# Integra: API + health_check.py + usuario no-root
# ════════════════════════════════════════════════════════════
# INSTRUCCIÓN 1: FROM — Imagen base
# python:3.11-slim = Python 3.11 sobre Debian mínimo (~130MB vs ~900MB completo)
FROM python:3.11-slim
# INSTRUCCIÓN 2: LABEL — Metadatos de la imagen (documentación)
LABEL maintainer="fintech-nova@empresa.com"
LABEL version="1.0.0"
LABEL description="API de evaluación crediticia FinTech Nova"
# INSTRUCCIÓN 3: ENV — Variables de entorno
# PYTHONDONTWRITEBYTECODE=1: no genera archivos .pyc (innecesarios en contenedor)
# PYTHONUNBUFFERED=1: los logs aparecen en tiempo real (sin buffering)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# INSTRUCCIÓN 4: WORKDIR — Directorio de trabajo dentro del contenedor
# Todos los COPY y CMD siguientes son relativos a este directorio
WORKDIR /app
# INSTRUCCIÓN 5: Crear usuario no-root (Principio de Mínimo Privilegio)
# Por defecto Docker corre como root — si hay un ataque exitoso, tiene acceso total
# 'appuser' tiene solo los permisos necesarios para correr la API
RUN addgroup --system appgroup && \
 adduser --system --ingroup appgroup appuser
# INSTRUCCIÓN 6: Instalar dependencias del sistema
# curl: necesario para el HEALTHCHECK
# --no-install-recommends: evita instalar paquetes opcionales (menos tamaño)
# && apt-get clean + rm: limpia la caché de apt (reduce tamaño de la imagen)
RUN apt-get update && apt-get install -y --no-install-recommends \
 curl \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*
# INSTRUCCIÓN 7: Copiar requirements.txt ANTES que el código
# Optimización de caché: si solo cambia el código (no las deps),
# Docker reutiliza la capa de pip install del build anterior (mucho más rápido)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# INSTRUCCIÓN 8: Copiar el código de la aplicación
# Incluye: main.py, health_check.py y todos los archivos del proyecto
# (excepto los listados en .dockerignore)
COPY . .
# INSTRUCCIÓN 9: Asignar propietario de los archivos al usuario no-root
# Sin esto, los archivos serían de 'root' y appuser no podría modificarlos
RUN chown -R appuser:appgroup /app
# INSTRUCCIÓN 10: Cambiar al usuario no-root para el resto del build y ejecución
USER appuser
# INSTRUCCIÓN 11: Documentar el puerto que usa la aplicación
# EXPOSE no abre el puerto — es solo documentación
# El puerto real se mapea con -p al ejecutar docker run
EXPOSE 8000
# INSTRUCCIÓN 12: HEALTHCHECK — Docker verifica la salud automáticamente
# --interval=30s: verificar cada 30 segundos
# --timeout=10s: si no responde en 10s, falla
# --retries=3: después de 3 fallos consecutivos, marcar como 'unhealthy'
# Este HEALTHCHECK aprovecha el endpoint /health que implementamos en el Bloque 2
HEALTHCHECK --interval=30s --timeout=10s --retries=3 \
 CMD curl -f http://localhost:8000/health || exit 1
# INSTRUCCIÓN 13: CMD — El comando que ejecuta el contenedor al iniciar
# --host 0.0.0.0: escuchar en todas las interfaces (necesario en Docker)
# Sin 0.0.0.0, el servidor solo escucharía dentro del contenedor y sería inaccesible
CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]
