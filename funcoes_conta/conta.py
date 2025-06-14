from datetime import datetime, timedelta
from .historico import Historico  # import local do package

class Conta:
    def __init__(self, cliente, numero, agencia='0001'):
        self.__saldo = 0.0
        self.__numero = numero
        self.__agencia = agencia
        self.__cliente = cliente
        self.__historico = Historico()
        self.__limite_transacao = 10
        self.__limite_valor_saques = 500
        self.__horarios = []

    @property
    def numero(self):
        return self.__numero

    @property
    def agencia(self):
        return self.__agencia

    @property
    def cliente(self):
        return self.__cliente

    @property
    def saldo(self):
        return self.__saldo

    @property
    def historico(self):
        return self.__historico

    def sacar(self, valor):
        self.__resetar_limite()
        if self.__limite_transacao <= 0:
            print("Limite diário de transações atingido.")
            return False
        if valor > self.__saldo:
            print("Saldo insuficiente.")
            return False
        if valor > self.__limite_valor_saques:
            print("Limite por saque excedido.")
            return False

        self.__saldo -= valor
        self.__historico.adicionar_transacao("Saque", valor)
        self.__registrar_transacao()
        print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
        return True

    def depositar(self, valor):
        self.__resetar_limite()
        if self.__limite_transacao <= 0:
            print("Limite diário de transações atingido.")
            return False
        self.__saldo += valor
        self.__historico.adicionar_transacao("Depósito", valor)
        self.__registrar_transacao()
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
        return True

    def extrato(self):
        self.__resetar_limite()
        if self.__limite_transacao <= 0:
            print("Limite diário de transações atingido.")
            return

        for data, tipo_valor in self.__historico.transacoes:
            tipo, valor = tipo_valor
            print(f"{tipo} R$ {valor:.2f} - {data.strftime('%d/%m/%Y %H:%M:%S')}")
        print(f"Saldo atual: R$ {self.__saldo:.2f}")
        self.__limite_transacao -= 1

    def __registrar_transacao(self):
        self.__horarios.append(datetime.now())
        self.__limite_transacao -= 1

    def __resetar_limite(self):
        if self.__horarios and (datetime.now() - self.__horarios[0]) >= timedelta(days=1):
            self.__limite_transacao = 10
            self.__horarios.clear()


class ContaCorrente(Conta):
    def __init__(self, cliente, numero, agencia='0001', limite=500, limite_saques=3):
        super().__init__(cliente, numero, agencia)
        self.__limite = limite
        self.__limite_saques = limite_saques

    @property
    def limite(self):
        return self.__limite

    @property
    def limite_saques(self):
        return self.__limite_saques
