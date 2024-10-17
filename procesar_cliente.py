import json
from datetime import datetime

# Clase para clientes
class Cliente:
    def __init__(self, numero, nombre, apellido, dni, tipo, transacciones):
        self.numero = numero
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.tipo = tipo
        self.transacciones = [Transaccion(**trans) for trans in transacciones]

    def procesar_transacciones(self):
        for transaccion in self.transacciones:
            transaccion.validar(self.tipo)

# Clase para transacciones
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

    def validar(self, tipo_cliente):
        if self.estado == "ACEPTADA":
            return  # Si ya es aceptada no se valida más
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


# F para generar el reporte HTML
def generar_reporte_html(cliente):
    html = f"""
    <html>
    <head>
        <title>Reporte de Transacciones - Cliente {cliente.nombre} {cliente.apellido}</title>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            h1, h2 {{ color: #333; }}
        </style>
    </head>
    <body>
        <h1>Reporte de Transacciones del Cliente {cliente.nombre} {cliente.apellido}</h1>
        <h2>Cliente Nº: {cliente.numero} | DNI: {cliente.dni} | Tipo de Cliente: {cliente.tipo}</h2>
        <table>
            <tr>
                <th>Número de Transacción</th>
                <th>Tipo de Transacción</th>
                <th>Estado</th>
                <th>Fecha</th>
                <th>Monto</th>
                <th>Razón de Rechazo (si aplica)</th>
            </tr>
    """
    for transaccion in cliente.transacciones:
        html += f"""
        <tr>
            <td>{transaccion.numero}</td>
            <td>{transaccion.tipo}</td>
            <td>{transaccion.estado}</td>
            <td>{transaccion.fecha.strftime("%d/%m/%Y %H:%M:%S")}</td>
            <td>{transaccion.monto}</td>
            <td>{transaccion.razon_rechazo if transaccion.razon_rechazo else 'N/A'}</td>
        </tr>
        """
    
    html += """
        </table>
    </body>
    </html>
    """
    
    with open(f"reporte_cliente_{cliente.numero}.html", "w") as file:
        file.write(html)
    
    print(f"Reporte generado: reporte_cliente_{cliente.numero}.html")


# F para procesar clientes desde un JSON
def procesar_clientes(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        for cliente_data in data['clientes']:  
            print("Datos del cliente:", cliente_data)  # Línea de depuración 
            cliente = Cliente(**cliente_data)  
            cliente.procesar_transacciones()
            generar_reporte_html(cliente)

# Main
if __name__ == "__main__":
    filename = input("Ingrese el nombre del archivo JSON (con extensión): ")
    procesar_clientes(filename)
