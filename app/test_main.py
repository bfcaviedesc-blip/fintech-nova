import pytest
from fastapi.testclient import TestClient
from app.main import app, db_cuentas, db_transacciones

client = TestClient(app)

class TestEndpointsBasicos:
    def test_raiz_retorna_200(self):
        assert client.get('/').status_code == 200

    def test_raiz_contiene_nombre_servicio(self):
        datos = client.get('/').json()
        assert datos["servicio"] == "FinTech Nova API"

    def test_health_check_retorna_healthy(self):
        resp = client.get('/health')
        assert resp.status_code == 200
        assert resp.json()["status"] == "healthy"

    def test_listar_cuentas_retorna_lista(self):
        resp = client.get('/cuentas')
        assert resp.status_code == 200
        assert len(resp.json()) > 0

class TestConsultaCuentas:
    def test_obtener_cuenta_existente(self):
        resp = client.get('/cuentas/ACC-001')
        assert resp.status_code == 200
        assert resp.json()["titular"] == "María García"

    def test_cuenta_inexistente_retorna_404(self):
        assert client.get('/cuentas/ACC-999').status_code == 404

class TestTransferencias:
    def setup_method(self):
        db_cuentas["ACC-001"]["saldo"] = 5000.00
        db_cuentas["ACC-002"]["saldo"] = 3200.50
        db_transacciones.clear()

    def test_transferencia_exitosa(self):
        resp = client.post('/transferencias', json={
            "cuenta_origen":"ACC-001","cuenta_destino":"ACC-002","monto":500.00})
        assert resp.status_code == 201
        assert resp.json()["estado"] == "completada"

    def test_descuenta_saldo_origen(self):
        client.post('/transferencias', json={
            "cuenta_origen":"ACC-001","cuenta_destino":"ACC-002","monto":200.0})
        assert db_cuentas["ACC-001"]["saldo"] == 4800.00

    def test_acredita_saldo_destino(self):
        client.post('/transferencias', json={
            "cuenta_origen":"ACC-001","cuenta_destino":"ACC-002","monto":300.0})
        assert db_cuentas["ACC-002"]["saldo"] == 3500.50

    def test_saldo_insuficiente_retorna_400(self):
        resp = client.post('/transferencias', json={
            "cuenta_origen":"ACC-001","cuenta_destino":"ACC-002","monto":99999.0})
        assert resp.status_code == 400

    def test_cuenta_origen_inexistente_retorna_404(self):
        resp = client.post('/transferencias', json={
            "cuenta_origen":"ACC-FAKE","cuenta_destino":"ACC-002","monto":100.0})
        assert resp.status_code == 404

    def test_monto_negativo_rechazado(self):
        resp = client.post('/transferencias', json={
            "cuenta_origen":"ACC-001","cuenta_destino":"ACC-002","monto":-50.0})
        assert resp.status_code == 422

    def test_transferencia_se_registra(self):
        client.post('/transferencias', json={
            "cuenta_origen":"ACC-001","cuenta_destino":"ACC-002","monto":100.0})
        assert client.get("/transacciones").json()["total"] == 1
