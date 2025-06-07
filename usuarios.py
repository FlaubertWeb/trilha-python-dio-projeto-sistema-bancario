from datetime import datetime, timedelta

# ----------------------------
# DADOS
# ----------------------------

usuarios = [
    {
        "cpf": "12345678901",
        "nome": "Ana Souza",
        "data_nascimento": "10/05/1990",
        "endereco": {
            "logradouro": "Rua das Flores",
            "numero": "123",
            "bairro": "Jardim América",
            "cidade": "São Paulo",
            "uf": "SP"
        },
        "senha": "ana123",
        "contas": [
            {
                "tipo": "corrente",
                "agencia": "0001",
                "numero": "1001",
                "saldo": 15.0,
                "extrato": [],
                "saques": [],
                "depositos": [],
                "datetime": [],
                "limite_transacao": 10,
                "limite_valor_saques": 500
            }
        ]
    },
    {
        "cpf": "37753443810",
        "nome": "Flaubert Silva",
        "data_nascimento": "13/02/1985",
        "endereco": {
            "logradouro": "Av. Brasil",
            "numero": "456",
            "bairro": "Centro",
            "cidade": "Rio de Janeiro",
            "uf": "RJ"
        },
        "senha": "1234",
        "contas": [
            {
                "tipo": "poupanca",
                "agencia": "0001",
                "numero": "1002",
                "saldo": 1500.0,
                "extrato": [],
                "saques": [],
                "depositos": [],
                "datetime": [],
                "limite_transacao": 10,
                "limite_valor_saques": 500
            },
            {
                "tipo": "corrente",
                "agencia": "0001",
                "numero": "1003",
                "saldo": 3500.0,
                "extrato": [],
                "saques": [],
                "depositos": [],
                "datetime": [],
                "limite_transacao": 10,
                "limite_valor_saques": 500
            }
        ]
    }
]
