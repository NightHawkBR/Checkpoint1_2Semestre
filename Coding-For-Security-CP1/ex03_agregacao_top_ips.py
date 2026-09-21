"""Exercicio 3 - Agregacao: Top 3 IPs com mais eventos FAIL.

A contagem e feita pelo aggregation pipeline do MongoDB (e nao por um
laco em Python): o banco filtra, agrupa e ordena, devolvendo so 3 docs.
"""

from config import get_mongo_db, titulo

eventos = [
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "OK", "ip": "192.168.1.10"},
    {"tipo": "FAIL", "ip": "91.240.118.172"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
    {"tipo": "FAIL", "ip": "91.240.118.172"},
    {"tipo": "FAIL", "ip": "45.33.32.156"},
    {"tipo": "FAIL", "ip": "185.220.101.1"},
]

PIPELINE_TOP_FAILS = [
    {"$match": {"tipo": "FAIL"}},                          # so as falhas
    {"$group": {"_id": "$ip", "total": {"$sum": 1}}},      # conta por IP
    {"$sort": {"total": -1}},                              # maior primeiro
    {"$limit": 3},                                         # top 3
]


def main():
    db = get_mongo_db()
    colecao = db["eventos_auth"]

    titulo("EXERCICIO 3 - Top 3 IPs com mais FAIL (aggregation)")

    colecao.delete_many({})
    colecao.insert_many([dict(e) for e in eventos])
    print(f"{colecao.count_documents({})} eventos inseridos.\n")

    print("Top 3 IPs por falhas de autenticacao:")
    for posicao, doc in enumerate(colecao.aggregate(PIPELINE_TOP_FAILS), start=1):
        print(f"  {posicao}. {doc['_id']} -> {doc['total']}")


if __name__ == "__main__":
    main()
