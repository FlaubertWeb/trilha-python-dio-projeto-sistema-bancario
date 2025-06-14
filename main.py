from datetime import datetime
from funcoes_conta.cliente import PessoaFisica
from funcoes_conta.conta import ContaCorrente
from funcoes_conta.transacoes import Deposito, Saque

clientes = []
AGENCIA_SAO_PAULO = "0001"

def gerar_proximo_numero_conta():
    maior = 1000
    for cliente in clientes:
        for conta in cliente.contas:
            if conta.numero > maior:
                maior = conta.numero
    return maior + 1

def operacao():
    cpf = input("Informe seu CPF: ")
    cliente = next((c for c in clientes if c.cpf == cpf), None)

    if cliente:
        tentativas = 3
        while tentativas > 0:
            senha = input("Informe sua senha: ")
            if cliente.senha == senha:
                break
            tentativas -= 1
            print(f"Senha incorreta. Tentativas restantes: {tentativas}")
        else:
            print("Número máximo de tentativas atingido. Encerrando operação.")
            return

        print(f"\nBem-vindo(a), {cliente.nome}!")

        if len(cliente.contas) > 1:
            print("\nVocê possui mais de uma conta. Qual deseja acessar?")
            for i, conta in enumerate(cliente.contas, 1):
                print(f"{i} - Conta {conta.numero} - Agência {conta.agencia}")
            try:
                idx = int(input("Escolha o número da conta: ")) - 1
                conta = cliente.contas[idx]
            except (ValueError, IndexError):
                print("Seleção inválida. Encerrando.")
                return
        else:
            conta = cliente.contas[0]

        while True:
            opcao = input("\n(1) Depósito\n(2) Saque\n(3) Extrato\n(4) Sair\n-> ")
            if opcao == "1":
                try:
                    valor = float(input("Digite o valor para depósito: "))
                    cliente.realizar_transacao(conta, Deposito(valor))
                except ValueError:
                    print("Valor inválido.")
            elif opcao == "2":
                try:
                    valor = float(input("Digite o valor para saque: "))
                    cliente.realizar_transacao(conta, Saque(valor))
                except ValueError:
                    print("Valor inválido.")
            elif opcao == "3":
                print("\nEXTRATO:")
                conta.extrato()
            elif opcao == "4":
                print("Logout feito com sucesso.")
                break
            else:
                print("Opção inválida.")
    else:
        print("Usuário não encontrado.")
        if input("Deseja se cadastrar? (s/n): ").lower() == "s":
            nome = input("Nome completo: ")
            data_nasc = input("Data de nascimento (dd/mm/aaaa): ")
            endereco = input("Endereço completo: ")
            senha = input("Crie uma senha: ")

            try:
                data_formatada = datetime.strptime(data_nasc, "%d/%m/%Y").date()
            except ValueError:
                print("Data inválida. Encerrando cadastro.")
                return

            novo_cliente = PessoaFisica(cpf=cpf, nome=nome, data_nascimento=data_formatada, endereco=endereco)
            novo_cliente.senha = senha

            numero_conta = gerar_proximo_numero_conta()
            nova_conta = ContaCorrente(cliente=novo_cliente, numero=numero_conta, agencia=AGENCIA_SAO_PAULO)
            novo_cliente.adicionar_conta(nova_conta)

            clientes.append(novo_cliente)
            print("Cadastro realizado com sucesso.\n")
            operacao()
        else:
            print("Operação encerrada.")

if __name__ == "__main__":
    operacao()
