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

    def validar_alta_tarjeta(self, tipo_cliente):
        limites = {
            "CLASSIC": 0,
            "GOLD": 1,
            "BLACK": 5
        }
        if self.totalTarjetasDeCreditoActualmente >= limites[tipo_cliente]:
            self.estado = "RECHAZADA"
            self.razon_rechazo = f"El cliente ya tiene el número máximo de tarjetas de crédito para su tipo de cuenta ({limites[tipo_cliente]})."

    def validar_alta_chequera(self, tipo_cliente):
        limites = {
            "CLASSIC": 0,
            "GOLD": 1,
            "BLACK": 2
        }
        if self.totalChequerasActualmente >= limites[tipo_cliente]:
            self.estado = "RECHAZADA"
            self.razon_rechazo = f"El cliente ya tiene el número máximo de chequeras para su tipo de cuenta ({limites[tipo_cliente]})."

    def validar_compra_dolar(self, tipo_cliente):
        if tipo_cliente not in ["GOLD", "BLACK"]:
            self.estado = "RECHAZADA"
            self.razon_rechazo = "El cliente no tiene permitido comprar dólares."

    def validar_transferencia_enviada(self, tipo_cliente):
        comisiones = {
            "CLASSIC": 0.01,
            "GOLD": 0.005,
            "BLACK": 0
        }
        saldo_requerido = self.monto + self.monto * comisiones[tipo_cliente]
        if self.saldoEnCuenta < saldo_requerido:
            self.estado = "RECHAZADA"
            self.razon_rechazo = "Saldo insuficiente para realizar la transferencia con la comisión aplicada."

    def validar_transferencia_recibida(self, tipo_cliente):
        limites = {
            "CLASSIC": 150000,
            "GOLD": 500000,
            "BLACK": float('inf')
        }
        if self.monto > limites[tipo_cliente]:
            self.estado = "RECHAZADA"
            self.razon_rechazo = f"El monto de la transferencia supera el límite permitido para clientes {tipo_cliente}."