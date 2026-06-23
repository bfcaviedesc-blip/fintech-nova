# API de Predicción de Datos

Esta es una API sencilla desarrollada con FastAPI para fines educativos y de práctica en análisis de vulnerabilidades, despliegue de aplicaciones y pruebas de servicios web.

## Descripción

La API incluye:

- Endpoint principal de bienvenida.
- Endpoint de verificación de estado (Health Check).
- Endpoint de consulta de datos de usuarios.
- Base de datos simulada en memoria.

> **Nota:** El endpoint `/datos-sensibles/{usuario}` fue diseñado con fines académicos para analizar posibles vulnerabilidades relacionadas con el control de acceso y la autenticación.

---

## Estructura del Proyecto

```text
.
├── main.py
├── requirements.txt
└── README.md
```

---

## Requisitos

- Python 3.9 o superior
- GitHub Codespaces (recomendado)
- Pip

---

## Dependencias

Archivo `requirements.txt`

```txt
fastapi
uvicorn
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## Ejecución en GitHub Codespaces

### Paso 1. Abrir el proyecto

1. Ingrese al repositorio de GitHub.
2. Seleccione **Code**.
3. Haga clic en **Codespaces**.
4. Cree un nuevo Codespace.

---

### Paso 2. Instalar dependencias

En la terminal ejecute:

```bash
pip install -r requirements.txt
```

---

### Paso 3. Iniciar la API

Ejecute el siguiente comando:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Si todo funciona correctamente, verá un mensaje similar a:

```text
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Endpoints Disponibles

### 1. Página Principal

**GET /**

Devuelve un mensaje de bienvenida.

Ejemplo:

```json
{
  "mensaje": "Bienvenido a la API de Análisis. El sistema está en línea."
}
```

---

### 2. Estado del Sistema

**GET /status**

Permite verificar que la API está funcionando correctamente.

Ejemplo:

```json
{
  "status": "ok",
  "servicios": "operativos"
}
```

---

### 3. Consulta de Datos de Usuario

**GET /datos-sensibles/{usuario}**

Obtiene información asociada a un usuario almacenado en la base de datos simulada.

Ejemplo:

```http
GET /datos-sensibles/user1
```

Respuesta:

```json
{
  "usuario": "user1",
  "estado": "Activo",
  "datos_financieros": "Confidencial"
}
```

---

## Usuarios Disponibles

La base de datos simulada contiene:

| Usuario | Estado |
|----------|----------|
| user1 | Activo |
| user2 | Inactivo |

---

## Documentación Automática

FastAPI genera documentación interactiva automáticamente.

Una vez ejecutada la aplicación, puede acceder a:

### Swagger UI

```text
http://localhost:8000/docs
```

### ReDoc

```text
http://localhost:8000/redoc
```

---

## Objetivo Académico

Este proyecto fue creado para:

- Comprender el funcionamiento básico de FastAPI.
- Desplegar servicios web en GitHub Codespaces.
- Realizar pruebas de APIs REST.
- Analizar controles de acceso y autenticación.
- Practicar actividades de análisis de vulnerabilidades en entornos controlados.

---

## Tecnologías Utilizadas

- Python
- FastAPI
- Uvicorn

---

## Autor

Proyecto académico para prácticas de desarrollo seguro y análisis de vulnerabilidades.
