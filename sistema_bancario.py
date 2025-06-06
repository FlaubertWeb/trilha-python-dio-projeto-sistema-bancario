from datetime import datetime, timedelta 


contas = [
    {
        "conta": "1001",  # conta sem saldo p/ teste
        "id": "123456789100",
        "titular": "Ana Souza",
        "saldo": 15.0,
        "senha": "ana123",
        "extrato": [],
        "saques":[],
        "depositos":[],
        "datetime":[],
        "saques_diarios": 3,
        "limite_transacao": 10,
        "limite_valor_sac": 500           
    },
    {
        "conta": "1002",  # Conta com saldo p/ teste
        "id": "37753443810",
        "titular": "Flaubert",
        "saldo": 1500.0,
        "senha": "1234",
        "extrato": [],
        "saques":[],
        "depositos":[],
        "datetime":[],
        "saques_diarios": 3,
        "limite_transacao": 10,
        "limite_valor_sac": 500    
    }
]

def criar_conta(cpf, nome, senha, saldo=0):
    if contas:
        # ← gera automaticamente número de conta somando ao maior atual
        ultimo_numero = max(int(c["conta"]) for c in contas)
        novo_numero = str(ultimo_numero + 1)
    else:
        novo_numero = "1001"

    conta = {
        "conta": novo_numero,
        "id": cpf,
        "titular": nome,
        "saldo": saldo,
        "senha": senha,
        "extrato": [],
        "saques":[],
        "depositos":[],
        "datetime":[],
        "saques_diarios": 3,
        "limite_transacao": 10,
        "limite_valor_sac": 500    
    }
    contas.append(conta)
    print(f"Conta criada com sucesso! Número da conta: {novo_numero}")
    return conta


def deposito(conta):
    if conta['limite_transacao'] <= 0:
        print('Limite de transações diárias atingido, tente novamente amanhã!') 
        return

    agora = datetime.now()
    entrada = input("Digite o valor para depositar: ")
    
    if not entrada.replace('.', '', 1).isdigit():
        print("Valor inválido.")
        return

    valor = float(entrada)
    conta["saldo"] += valor
    conta["depositos"].append(f"Depósito: +R$ {valor:.2f}")
    conta["extrato"].append(f"Depósito: +R$ {valor:.2f}")
    conta["datetime"].append(agora)   
    conta['limite_transacao'] -= 1 

    if conta["datetime"]:
        date_first_operation = conta['datetime'][0]
        if (agora - date_first_operation >= timedelta(days=1)):
            conta['saques_diarios'] = 3
            conta['limite_transacao'] = 10

    print(f"Depósito de R$ {valor:.2f} realizado com sucesso. \nVocê ainda pode fazer {conta['limite_transacao']} transações hoje.")



def saque(conta):
    agora = datetime.now()
    entrada = input("Digite o valor para sacar: ")

    if not entrada.replace('.', '', 1).isdigit():
        print("Valor inválido.")
        return

    valor = float(entrada)

    if valor > conta['limite_valor_sac']: 
        print("Seu limite por saque é de R$500,00. Insira um valor igual ou menor.")
        return

    elif conta['limite_transacao'] <= 0:
        print('Limite de transações diárias atingido, tente novamente amanhã!') 
        return   

    elif valor <= conta["saldo"]:
        conta["saldo"] -= valor
        conta["saques"].append(f"Saque: -R$ {valor:.2f}")
        conta["extrato"].append(f"Saque: -R$ {valor:.2f}")
        conta["datetime"].append(agora)
        conta['limite_transacao'] -= 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso. \nVocê ainda pode fazer {conta['limite_transacao']} transações hoje.")
        
        if conta["datetime"]:
            date_last_operation = conta['datetime'][0]
            if (agora - date_last_operation >= timedelta(days=1)):
                conta['saques_diarios'] = 3
                conta['limite_transacao'] = 10
    else:
        print("Saldo insuficiente.")


def extrato(conta):
    if conta['limite_transacao'] <= 0:
        print('Limite de transações diárias atingido, tente novamente amanhã!')
        return

    agora = datetime.now()

    # Registro da operação extrato no extrato e datas
    conta["extrato"].append(f"Operação extrato realizada")
    conta["datetime"].append(agora)

    print(f"\nExtrato da conta {conta['conta']} - {conta['titular']}:")
    if not conta["extrato"]:
        print("Nenhuma movimentação.")
    else:
        for item, momento in zip(conta["extrato"], conta['datetime']):
            print(f"{item} - Data e hora: {momento.strftime('%d/%m/%Y, %H:%M:%S')}")

    print(f"Saldo atual: R$ {conta['saldo']:.2f}\n")

    conta['limite_transacao'] -= 1
    print(f"Você ainda pode fazer {conta['limite_transacao']} transações hoje.")

    # Reset de limite diário (ainda da pra otimizar depois)
    if conta["datetime"]:
        date_first_operation = conta['datetime'][0]
        if (agora - date_first_operation >= timedelta(days=1)):
            conta['saques_diarios'] = 3
            conta['limite_transacao'] = 10


def operacao():
    verificacao = input("Você possui conta? Escolha um número:\n (1) Sim\n (2) Não: ")
    
    if verificacao == "1":
        cpf = input('Informe seu CPF para acessar sua conta: ') 
        senha = input('Informe sua senha: ')
        
        for conta in contas:
            if conta["id"] == cpf and conta["senha"] == senha:
                print(f"\nBem-vindo(a), {conta['titular']}! Conta nº {conta['conta']}")
                while True:  # ← mantido no menu até o usuário sair
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
                break  # ← sai do loop for após login bem-sucedido
        else:
            return "Desculpe, CPF ou senha inválidos. Tente novamente."  # ← else do for, executa se nenhum for válido

    elif verificacao == "2":
        print("\nCriando sua conta:")
        cpf = input("Digite o CPF: ")
        nome = input("Digite o nome: ")
        senha = input("Crie uma senha: ")
        return criar_conta(cpf, nome, senha)

    else:
        return "Opção inválida."
    




print(operacao())

