from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import uuid
from datetime import datetime

#Prueba despliegue

app = FastAPI(
    title="FinTech Nova API",
    description="API de operaciones financieras - Demo CI/CD DevSecOps",
    version="1.0.0"
)

db_cuentas = {
    "ACC-001": {"titular": "María García",  "saldo": 5000.00,  "moneda": "USD"},
    "ACC-002": {"titular": "Carlos López",  "saldo": 3200.50,  "moneda": "USD"},
    "ACC-003": {"titular": "Ana Martínez",  "saldo": 12800.75, "moneda": "USD"},
}
db_transacciones = []

class Transferencia(BaseModel):
    cuenta_origen:  str   = Field(..., example="ACC-001")
    cuenta_destino: str   = Field(..., example="ACC-002")
    monto:          float = Field(..., gt=0, example=100.00)
    descripcion:    Optional[str] = None

@app.get('/')
def raiz():
    return {
        "servicio":  "FinTech Nova API",
        "version":   "1.0.0",
        "estado":    "operacional",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get('/health')
def health_check():
    return {
        "status":                  "healthy",
        "cuentas_registradas":     len(db_cuentas),
        "transacciones_procesadas":len(db_transacciones)
    }

@app.get('/cuentas/{id_cuenta}')
def obtener_cuenta(id_cuenta: str):
    if id_cuenta not in db_cuentas:
        raise HTTPException(status_code=404, detail=f'Cuenta {id_cuenta} no encontrada')
    cuenta = db_cuentas[id_cuenta].copy()
    cuenta['id'] = id_cuenta
    return cuenta

@app.get('/cuentas')
def listar_cuentas():
    return [{'id':k,'titular':v['titular'],'moneda':v['moneda']} for k,v in db_cuentas.items()]

@app.post('/transferencias', status_code=201)
def crear_transferencia(transferencia: Transferencia):
    if transferencia.cuenta_origen not in db_cuentas:
        raise HTTPException(status_code=404, detail=f'Cuenta origen no encontrada')
    if transferencia.cuenta_destino not in db_cuentas:
        raise HTTPException(status_code=404, detail=f'Cuenta destino no encontrada')
    saldo = db_cuentas[transferencia.cuenta_origen]['saldo']
    if saldo < transferencia.monto:
        raise HTTPException(status_code=400, detail=f'Saldo insuficiente. Disponible: ${saldo:.2f}')
    db_cuentas[transferencia.cuenta_origen]['saldo'] -= transferencia.monto
    db_cuentas[transferencia.cuenta_destino]['saldo'] += transferencia.monto
    id_tx = f'TX-{str(uuid.uuid4())[:8].upper()}'
    ts = datetime.utcnow().isoformat()
    db_transacciones.append({'id':id_tx,'origen':transferencia.cuenta_origen,
        'destino':transferencia.cuenta_destino,'monto':transferencia.monto,'timestamp':ts})
    return {'id_transaccion':id_tx,'estado':'completada','timestamp':ts,
            'monto':transferencia.monto,'cuenta_origen':transferencia.cuenta_origen,
            'cuenta_destino':transferencia.cuenta_destino}

@app.get('/transacciones')
def listar_transacciones():
    return {'total':len(db_transacciones),'transacciones':db_transacciones}
