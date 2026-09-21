"""Exercicio 6 - Indice e desempenho no MongoDB.

Gera 1000 eventos, cria indice em 'ip' e consulta um IP especifico.

POR QUE O INDICE IMPORTA (comentario pedido no enunciado):
  Sem indice o MongoDB faz COLLSCAN: le os 1000 documentos um a um para
  achar o IP, custo O(n) -- com 10 milhoes de eventos, varre 10 milhoes.
  Com indice em 'ip' ele faz IXSCAN: navega uma B-tree ordenada e vai
  direto aos documentos do IP, custo ~O(log n) mais a leitura dos acertos.
"""

from config import get_mongo_db, titulo

IPS = ["185.220.101.1", "91.240.118.172", "45.33.32.156", "192.168.1.10"]
TOTAL_EVENTOS = 1000
IP_CONSULTADO = "185.220.101.1"


def main():
    db = get_mongo_db()
    colecao = db["eventos_volume"]

    titulo("EXERCICIO 6 - Indice e desempenho")

    colecao.drop()  # drop tambem apaga indices antigos

    # --- Geracao em laco + insercao em lote --------------------------
    eventos = []
    for i in range(TOTAL_EVENTOS):
        eventos.append(
            {
                "evento_id": i,
                "ip": IPS[i % len(IPS)],
                "tipo": "FAIL" if i % 3 == 0 else "OK",
                "porta": 22 if i % 2 == 0 else 443,
            }
        )
    colecao.insert_many(eventos)  # 1 ida ao banco, nao 1000
    print(f"{colecao.count_documents({})} eventos inseridos.")

    # --- Indice -------------------------------------------------------
    nome_indice = colecao.create_index("ip")
    print(f"Indice criado em 'ip' (nome: {nome_indice}).")

    # --- Consulta -----------------------------------------------------
    quantidade = colecao.count_documents({"ip": IP_CONSULTADO})
    print(f"Eventos do IP {IP_CONSULTADO}: {quantidade}")

    # --- Prova de que o planejador usa o indice ----------------------
    plano = colecao.find({"ip": IP_CONSULTADO}).explain()
    estagio = plano["queryPlanner"]["winningPlan"]
    while "inputStage" in estagio:  # desce ate o estagio de acesso aos dados
        estagio = estagio["inputStage"]
    print(f"Estagio escolhido pelo planejador: {estagio['stage']} "
          f"(IXSCAN = usou indice, COLLSCAN = varreu a colecao)")

    print("\nComentario: sem indice a busca seria O(n) (varre tudo); "
          "com indice ~O(log n) via B-tree.")


if __name__ == "__main__":
    main()
