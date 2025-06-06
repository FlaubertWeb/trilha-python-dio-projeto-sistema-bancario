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
        "saques_diarios": 0         
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
        "saques_diarios": 0 
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
        "saques_diarios": 0 
    }
    contas.append(conta)
    print(f"Conta criada com sucesso! Número da conta: {novo_numero}")
    return conta


def deposito(conta):
    agora  = datetime.now()
    valor = float(input("Digite o valor para depositar: "))
    conta["saldo"] += valor
    conta["depositos"].append(f"Depósito: +R$ {valor:.2f}")
    conta["extrato"].append(f"Depósito: +R$ {valor:.2f}")
    conta["datetime"].append(agora)
    print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")


def saque(conta):
    agora  = datetime.now()
   # data_e_hora = datetime.strftime("%d/%m/%Y, %H:%M:%S")

    valor = float(input("Digite o valor para sacar: "))

    limite = 500

    if valor > limite: 
        print("Seu limite por saque é de R$500,00 por favor insira um valor abaixo ou igual do limite")
        return

    if conta['saques_diarios']>= 3:
        print('Limite de saque diário atingido, tente noamente em amnhã!') 
        return   

    if valor <= conta["saldo"]:
        conta["saldo"] -= valor
        conta["saques"].append(f"Saque: -R$ {valor:.2f}")
        conta["extrato"].append(f"Saque: -R$ {valor:.2f}")
        conta["datetime"].append(agora)
        print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
        conta['saques_diarios'] += 1
        date_last_operation =  conta['datetime'][0]

            
        if(agora - date_last_operation >= timedelta(days=1)):
            conta['saques_diarios'] = 0




    else:
        print("Saldo insuficiente.")

  
            


def extrato(conta):
    print(f"\nExtrato da conta {conta['conta']} - {conta['titular']}:")
    if not conta["extrato"]:
        print("Nenhuma movimentação.")
    else:
        for item, momento in zip(conta["extrato"], conta['datetime']):
            print(f"{item} - Data e hora: {momento.strftime('%d/%m/%Y, %H:%M:%S')}")
      

    print(f"Saldo atual: R$ {conta['saldo']:.2f}\n")


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

