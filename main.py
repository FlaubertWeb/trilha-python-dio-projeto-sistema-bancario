from datetime import datetime, timedelta
from usuarios import usuarios
from funcoes_conta import criar_usuario_e_conta, deposito, saque, extrato

AGENCIA_SAO_PAULO = "0001"

def operacao():
    cpf = input("Informe seu CPF: ")
    usuario = next((u for u in usuarios if u["cpf"] == cpf), None)

    if usuario:
        while True:
            senha = input("Informe sua senha: ")
            if usuario["senha"] == senha:
                print(f"\nBem-vindo(a), {usuario['nome']}!")

                # Se tiver mais de uma conta, pergunta qual acessar
                if len(usuario["contas"]) > 1:
                    print("\nVocê possui mais de uma conta. Qual deseja acessar?")
                    for i, conta in enumerate(usuario["contas"], start=1):
                        print(f"{i} - {conta['tipo'].capitalize()} (Agência {conta['agencia']} Número {conta['numero']})")

                    while True:
                        escolha = input("Digite o número da conta desejada: ")
                        if escolha.isdigit() and 1 <= int(escolha) <= len(usuario["contas"]):
                            conta = usuario["contas"][int(escolha) - 1]
                            break
                        else:
                            print("Opção inválida, tente novamente.")
                else:
                    conta = usuario["contas"][0]

                print(f"CONTA {conta['tipo'].capitalize()}")    

                while True:
                    selection = input("\nEscolha a operação:\n (1) Depósito\n (2) Saque\n (3) Extrato\n (4) Sair\n-> ")

                    if selection == "1":
                        deposito(conta)
                    elif selection == "2":
                        saque(conta)
                    elif selection == "3":
                        extrato(conta)
                    elif selection == "4":
                        return "Logout feito com sucesso"
                    else:
                        print("Opção inválida. Tente de novo.")
            else:
                print("Senha incorreta. Tente novamente.")

    else:
        print("Você não possui cadastro:\nDeseja se cadastrar?\n(1) Sim\n(2) Não")
        escolha = input("-> ")

        if escolha == "1":
            print("\nCriando sua conta:") 
            
            while True:

                print("Escolha o tipo de conta:")
                print("(1) Corrente")
                print("(2) Poupança")
                print("(3) cancelar")

                escolha = input("Digite o número correspondente: ")

                if escolha == "1":
                    tipo = "corrente"
                    break
                elif escolha == "2":
                    tipo = "poupança"
                    break
                elif escolha == "3":
                    print("Operação cancelada") 

                    exit() 
                else:
                    print("Opção inválida. Tente novamente.\n")

            primeiro_nome = input("Digite o primeiro nome: ")
            sobre_nome = input("Digite o sobrenome: ")
            nome = f"{primeiro_nome} {sobre_nome}"
            data_nascimento = input("Data de nascimento (dd/mm/aaaa): ")
            logradouro = input("Informe seu logradouro: ")
            numero = input("Número da residência: ")
            bairro = input("Bairro: ")
            cidade = input("Qual a sua cidade? ")
            uf = input("Estado (UF): ")
            senha = input("Crie uma senha: ")
            


            novo_usuario = criar_usuario_e_conta(
                cpf=cpf,
                nome=nome,
                senha=senha,
                data_nascimento=data_nascimento,
                logradouro=logradouro,
                numero=numero,
                bairro=bairro,
                cidade=cidade,
                uf=uf,
                agencia=AGENCIA_SAO_PAULO,
                tipo_conta = tipo
            ) 

            if novo_usuario is None:
                print("Falha na criação do usuário. Tente novamente.")
                return

            usuarios.append(novo_usuario)
            print("Cadastro realizado com sucesso!\nEntrando na conta...")

            # Seleciona a primeira conta criada (ou única)
            conta = novo_usuario["contas"][0]

            while True:
                selection = input("\nEscolha a operação:\n (1) Depósito\n (2) Saque\n (3) Extrato\n (4) Sair\n-> ")

                if selection == "1":
                    deposito(conta)
                elif selection == "2":
                    saque(conta)
                elif selection == "3":
                    extrato(conta)
                elif selection == "4":
                    return "Logout feito com sucesso"
                else:
                    print("Opção inválida. Tente de novo.")

        elif escolha == "2":
            return "Cadastro cancelado."

        else:
            return "Opção inválida."

if __name__ == "__main__":
    operacao()
