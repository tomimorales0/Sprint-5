"""class Cliente:
    def __init__(self, numero, nombre, apellido, dni, tipo, transacciones):
        self.numero = numero
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.tipo = tipo
        self.saldo = 0  # Inicializa el saldo del cliente
        self.transacciones = [Transaccion(**trans) for trans in transacciones]
        self.limites_retiro_diario = {"CLASSIC": 10000, "GOLD": 20000, "BLACK": 100000}
        self.limites_transferencia_recibida = {"CLASSIC": 150000, "GOLD": 500000, "BLACK": float('inf')}
        self.retiro_diario_acumulado = 0  

    def procesar_transacciones(self):
        for transaccion in self.transacciones:
            transaccion.validar(self.tipo)

    def mostrar_saldo(self):
        print(f"Saldo actual del cliente {self.nombre} {self.apellido}: ${self.saldo}")

    def deposito(self, monto):
        if monto > 0:
            self.saldo += monto
            print(f"Depósito de ${monto} realizado con éxito. Saldo actual: ${self.saldo}")
        else:
            print("El monto del depósito debe ser mayor a cero.")

    def retiro(self, monto):
        # Validar que el monto no exceda el límite diario según el tipo de cliente
        if self.retiro_diario_acumulado + monto > self.limites_retiro_diario[self.tipo]:
            print(f"Retiro rechazado. Has excedido el límite diario de ${self.limites_retiro_diario[self.tipo]} para tu tipo de cuenta ({self.tipo}).")
        elif monto > self.saldo:
            print("Fondos insuficientes para el retiro.")
        else:
            self.saldo -= monto
            self.retiro_diario_acumulado += monto  # Sumar al retiro diario
            print(f"Retiro de ${monto} realizado con éxito. Saldo actual: ${self.saldo}. Retiro diario acumulado: ${self.retiro_diario_acumulado}")

    def transferencia(self, otro_cliente, monto):
        comisiones = {
            "CLASSIC": 0.01,  # 1% comisión
            "GOLD": 0.005,    # 0.5% comisión
            "BLACK": 0        # Sin comisión
        }

        # Validar que el monto más la comisión no exceda el saldo disponible
        monto_total = monto + (monto * comisiones[self.tipo])
        if monto_total > self.saldo:
            print("Fondos insuficientes para realizar la transferencia con la comisión aplicada.")
        elif otro_cliente.tipo == "CLASSIC" and monto > 150000:
            print("La transferencia supera el límite permitido para cuentas CLASSIC (máximo $150,000 por transferencia).")
        elif otro_cliente.tipo == "GOLD" and monto > 500000:
            print("La transferencia supera el límite permitido para cuentas GOLD (máximo $500,000 por transferencia).")
        else:
            self.saldo -= monto_total
            otro_cliente.saldo += monto
            print(f"Transferencia de ${monto} realizada con éxito a {otro_cliente.nombre} {otro_cliente.apellido}. Saldo actual: ${self.saldo}")

    def resetear_retiro_diario(self):
        # Método para reiniciar el retiro diario (por ejemplo, al final del día)
        self.retiro_diario_acumulado = 0
        print("El límite diario de retiro ha sido reiniciado.")
""" #for test purposes only