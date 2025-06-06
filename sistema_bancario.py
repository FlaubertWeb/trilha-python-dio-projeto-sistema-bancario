from datetime import datetime, timedelta 


contas = [
    {
        "conta": "1001",
        "cpf": "12345678901",
        "nome": "Ana Souza",
        "data_nascimento": "10/05/1990",
        "logradouro": "Rua das Flores",
        "numero": "123",
        "bairro": "Jardim América",
        "cidade": "São Paulo",
        "uf": "SP",
        "senha": "ana123",
        "saldo": 15.0,
        "extrato": [],
        "saques": [],
        "depositos": [],
        "datetime": [],
        # "saques_diarios": 0,
        "limite_transacao": 10,
        "limite_valor_saques": 500
    },
    {
        "conta": "1002",
        "cpf": "37753443810",
        "nome": "Flaubert Silva",
        "data_nascimento": "13/02/1985",
        "logradouro": "Av. Brasil",
        "numero": "456",
        "bairro": "Centro",
        "cidade": "Rio de Janeiro",
        "uf": "RJ",
        "senha": "1234",
        "saldo": 1500.0,
        "extrato": [],
        "saques": [],
        "depositos": [],
        "datetime": [],
        # "saques_diarios": 3,
        "limite_transacao": 10,
        "limite_valor_saques": 500
    }
]

# any([False, False, True])     # True  ← porque tem um True
# any([0, "", None])            # False ← todos são "falsy"
# any([0, "ok", None])          # True  ← "ok" é considerado True



def criar_conta(cpf, nome, senha, data_nascimento, logradouro, numero, bairro, cidade, uf, saldo=0):
    
    if contas:
        ultimo_numero = max(int(c["conta"]) for c in contas)    
        novo_numero = str(ultimo_numero + 1)
    else:
        novo_numero = "1001"
    conta = {
        "conta": novo_numero,
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "logradouro": logradouro,
        "numero": numero,
        "bairro": bairro,
        "cidade": cidade,
        "uf": uf,
        "saldo": saldo,
        "senha": senha,
        "extrato": [],
        "saques": [],
        "depositos": [],
        "datetime": [],
        # "saques_diarios": 3,          
        "limite_transacao": 10,      
        "limite_valor_saques": 500
    }

    contas.append(conta)
    print("____________________________________________________________")
    print(f"Conta criada com sucesso! Número da conta: {novo_numero}")
    print("____________________________________________________________")
    print(f"DADOS DE CASTRADOS:")
    print("____________________________________________________________")
    for chave, valor in list(conta.items())[:10]:
        
        print(f"- {chave}:{valor}")
        
    return ''



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

    if valor > conta['limite_valor_saques']: 
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

    print(f"\nExtrato da conta {conta['conta']} - {conta['nome']}:")
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
    cpf = input("Informe seu CPF: ")
    conta_encontrada = next((c for c in contas if c["cpf"] == cpf), None)

    if conta_encontrada:
        senha = input("Informe sua senha: ")

        if conta_encontrada["senha"] == senha:
            print(f"\nBem-vindo(a), {conta_encontrada['nome']}! Conta nº {conta_encontrada['conta']}")

            while True:
                selection = input("\nEscolha a operação:\n (1) Depósito\n (2) Saque\n (3) Extrato\n (4) Sair\n-> ")

                if selection == "1":
                    deposito(conta_encontrada)
                elif selection == "2":
                    saque(conta_encontrada)
                elif selection == "3":
                    extrato(conta_encontrada)
                elif selection == "4":
                    return "Logout feito com sucesso"
                else:
                    print("Opção inválida. Tente de novo.")
        else:
            return "Senha incorreta. Tente novamente."

    else:
        print("Você não possui cadastro:\nDeseja se cadastrar?\n(1) Sim\n(2) Não")
        escolha = input("-> ")

        if escolha == "1":
            print("\nCriando sua conta:")

            if any(c["cpf"] == cpf for c in contas):
                print("Este CPF já está cadastrado em nossa base de dados")
                return

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

            return criar_conta(cpf, nome, senha, data_nascimento, logradouro, numero, bairro, cidade, uf)

        elif escolha == "2":
            return "Cadastro cancelado."

        else:
            return "Opção inválida."








print(operacao())

