from .conta import Conta
class ContaCorrente(Conta):
    def __init__(self, cliente, numero, agencia='0001', limite=500, limite_saques=3):
        super().__init__(cliente, numero, agencia)
        self.__limite = limite
        self.__limite_saques = limite_saques
