from datetime import datetime, timedelta

################################################################
###################### CRIAR USUÁRIO ###########################
################################################################

def criar_usuario_e_conta(cpf, nome, senha, data_nascimento, logradouro, numero, bairro, cidade, uf, agencia, tipo_conta):
    """
    Cria um novo usuário com uma conta associada.
    Agora o tipo da conta pode ser 'corrente' ou 'poupanca'.
    """
    usuario = {
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": {
            "logradouro": logradouro,
            "numero": numero,
            "bairro": bairro,
            "cidade": cidade,
            "uf": uf
        },
        "senha": senha,
        "contas": []  # Lista que pode ter várias contas vinculadas a esse usuário
    }

    conta = {
        "tipo": tipo_conta,  # Adicionado tipo da conta
        "numero": "1001",
        "agencia": agencia,
        "saldo": 0.0,
        "extrato": [],
        "saques": [],
        "depositos": [],
        "datetime": [],
        "limite_transacao": 10,
        "limite_valor_saques": 500
    }

    usuario["contas"].append(conta)  # Vincula a conta criada ao usuário

    print(f"Usuário {nome} criado com sucesso!")
    print(f"Conta {conta['numero']} ({conta['tipo']}) criada na agência {agencia}.")

    return usuario

################################################################
########### RESETA LIMITE DIÁRIO SE PASSOU UM DIA ##############
################################################################

def resetar_limite_se_necessario(conta):
    """
    Reseta o limite de transações diárias se já passou 1 dia desde a primeira transação.
    """
    agora = datetime.now()
    if conta["datetime"]:
        primeira_operacao = conta["datetime"][0]
        if agora - primeira_operacao >= timedelta(days=1):
            conta['limite_transacao'] = 10
            conta["datetime"].clear()  # limpa o histórico para reiniciar a contagem do dia

################################################################
########################## DEPÓSITO ############################
################################################################

def deposito(conta):
    """
    Realiza depósito em uma conta, se respeitar os limites diários.
    """
    resetar_limite_se_necessario(conta)

    if conta['limite_transacao'] <= 0:
        print('Limite de transações diárias atingido, tente novamente amanhã!')
        return

    entrada = input("Digite o valor para depositar: ")

    if not entrada.replace('.', '', 1).isdigit():
        print("Valor inválido.")
        return

    valor = float(entrada)
    agora = datetime.now()
    conta["saldo"] += valor
    conta["depositos"].append(f"Depósito: +R$ {valor:.2f}")
    conta["extrato"].append(f"Depósito: +R$ {valor:.2f}")
    conta["datetime"].append(agora)
    conta['limite_transacao'] -= 1

    print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")
    print(f"Você ainda pode fazer {conta['limite_transacao']} transações hoje.")

################################################################
############################ SAQUE #############################
################################################################

def saque(conta):
    """
    Realiza saque, validando saldo, limites por valor e quantidade de transações.
    """
    resetar_limite_se_necessario(conta)

    if conta['limite_transacao'] <= 0:
        print('Limite de transações diárias atingido, tente novamente amanhã!')
        return

    entrada = input("Digite o valor para sacar: ")

    if not entrada.replace('.', '', 1).isdigit():
        print("Valor inválido.")
        return

    valor = float(entrada)

    if valor > conta['limite_valor_saques']:
        print("Seu limite por saque é de R$500,00. Insira um valor igual ou menor.")
        return

    if valor > conta["saldo"]:
        print("Saldo insuficiente.")
        return

    agora = datetime.now()
    conta["saldo"] -= valor
    conta["saques"].append(f"Saque: -R$ {valor:.2f}")
    conta["extrato"].append(f"Saque: -R$ {valor:.2f}")
    conta["datetime"].append(agora)
    conta['limite_transacao'] -= 1

    print(f"Saque de R$ {valor:.2f} realizado com sucesso.")
    print(f"Você ainda pode fazer {conta['limite_transacao']} transações hoje.")

################################################################
########################### EXTRATO ############################
################################################################

def extrato(conta):
    """
    Exibe o extrato da conta, listando todas as transações com data e hora.
    """
    resetar_limite_se_necessario(conta)

    if conta['limite_transacao'] <= 0:
        print('Limite de transações diárias atingido, tente novamente amanhã!')
        return

    agora = datetime.now()
    conta["extrato"].append("Operação extrato realizada")
    conta["datetime"].append(agora)

    print(f"\nExtrato da conta {conta['numero']} ({conta['tipo']}):")
    for item, momento in zip(conta["extrato"], conta['datetime']):
        print(f"{item} - Data e hora: {momento.strftime('%d/%m/%Y, %H:%M:%S')}")

    print(f"Saldo atual: R$ {conta['saldo']:.2f}\n")

    conta['limite_transacao'] -= 1
    print(f"Você ainda pode fazer {conta['limite_transacao']} transações hoje.")
