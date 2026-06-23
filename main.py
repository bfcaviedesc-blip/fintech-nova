from fastapi import FastAPI, HTTPException

app = FastAPI(title="API de Predicción de Datos", version="1.0")

# Base de datos simulada
datos_usuarios = {"user1": "Activo", "user2": "Inactivo"}

@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de Análisis. El sistema está en línea."}

@app.get("/status")
def health_check():
    return {"status": "ok", "servicios": "operativos"}

# Endpoint intencionalmente vulnerable (sin autenticación) para la Unidad 2
@app.get("/datos-sensibles/{usuario}")
def obtener_datos_privados(usuario: str):
    if usuario in datos_usuarios:
        return {"usuario": usuario, "estado": datos_usuarios[usuario], "datos_financieros": "Confidencial"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")