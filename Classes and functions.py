import json
from datetime import datetime

# Clase para clientes
class Cliente:
    def __init__ (self, numero, nombre, apellido, dni, tipo, transacciones):
        self.numero= numero
        self.nombre= nombre
        self.apellido= apellido
        self.dni= dni
        self.tipo= tipo
        self.transacciones = [Transaccion(**trans) for trans in transacciones]

    def procesar_transacciones (self):
        for transaccion in self.transacciones:
            transaccion.validar(self.tipo)

    # Clase para transacciónes
class Transaccion:
    def __init__(self, estado, tipo, cuentaNumero, cupoDiarioRestante, monto, fecha, numero, saldoEnCuenta, totalTarjetasDeCreditoActualmente, totalChequerasActualmente):
        self.estado = estado
        self.tipo = tipo
        self.cuentaNumero = cuentaNumero
        self.cupoDiarioRestante = cupoDiarioRestante
        self.monto = monto
        self.fecha = datetime.strptime(fecha, "%d/%m/%Y %H:%M:%S")
        self.numero = numero
        self.saldoEnCuenta = saldoEnCuenta
        self.totalTarjetasDeCreditoActualmente = totalTarjetasDeCreditoActualmente
        self.totalChequerasActualmente = totalChequerasActualmente
        self.razon_rechazo = ""

    def validar (self, tipo_cliente):
        if self.estado== "ACEPTADA":
            return #si ya es aceptada no se valida mas
        if self.tipo == "RETIRO_EFECTIVO_CAJERO_AUTOMATICO":
            self.validar_retiro(tipo_cliente)
        elif self.tipo == "ALTA_TARJETA_CREDITO":
            self.validar_alta_tarjeta(tipo_cliente)
        elif self.tipo == "ALTA_CHEQUERA":
            self.validar_alta_chequera(tipo_cliente)
        elif self.tipo == "COMPRAR_DOLAR":
            self.validar_compra_dolar(tipo_cliente)
        elif self.tipo == "TRANSFERENCIA_ENVIADA":
            self.validar_transferencia_enviada(tipo_cliente)
        elif self.tipo == "TRANSFERENCIA_RECIBIDA":
            self.validar_transferencia_recibida(tipo_cliente)

    def validar_retiro(self, tipo_cliente):
        limites = {
            "CLASSIC": 10000,
            "GOLD": 20000,
            "BLACK": 100000
        }
        if self.monto > limites[tipo_cliente]:
            self.estado = "RECHAZADA"
            self.razon_rechazo = f"El monto de retiro supera el límite diario para clientes {tipo_cliente}."

    