"""Exercicio 2 - CRUD com PyMongo na colecao 'vulnerabilidades'.

Create  -> insert_many
Read    -> find({"severidade": "Alta"})
Update  -> update_one({"cve_id": ...}, {"$set": {"corrigida": True}})
Delete  -> delete_one({"cve_id": ...})
"""

from config import get_mongo_db, titulo

vulns = [
    {"cve_id": "CVE-2024-001", "tipo": "SQL Injection", "severidade": "Alta", "corrigida": False},
    {"cve_id": "CVE-2024-002", "tipo": "XSS", "severidade": "Media", "corrigida": True},
    {"cve_id": "CVE-2024-003", "tipo": "Path Traversal", "severidade": "Critica", "corrigida": False},
]


def main():
    db = get_mongo_db()
    colecao = db["vulnerabilidades"]

    titulo("EXERCICIO 2 - CRUD com PyMongo")

    # --- CREATE -------------------------------------------------------
    colecao.delete_many({})  # colecao limpa para o script ser reexecutavel
    resultado = colecao.insert_many([dict(v) for v in vulns])
    print(f"{len(resultado.inserted_ids)} vulnerabilidades inseridas.\n")

    # --- READ ---------------------------------------------------------
    print("Buscar severidade='Alta':")
    for doc in colecao.find({"severidade": "Alta"}):
        print(f"  {doc['cve_id']}: {doc['tipo']}")

    # --- UPDATE -------------------------------------------------------
    atualizado = colecao.update_one(
        {"cve_id": "CVE-2024-001"},
        {"$set": {"corrigida": True}},
    )
    print(f"\n{atualizado.modified_count} documento modificado (CVE-2024-001 corrigida=True)")

    # Quantas seguem abertas depois da correcao
    abertas = colecao.count_documents({"corrigida": False})
    print(f"Vulnerabilidades ainda abertas (corrigida=False): {abertas}")
    for doc in colecao.find({"corrigida": False}, {"_id": 0, "cve_id": 1, "severidade": 1}):
        print(f"  {doc['cve_id']} ({doc['severidade']})")

    # --- DELETE -------------------------------------------------------
    removido = colecao.delete_one({"cve_id": "CVE-2024-002"})
    print(f"\n{removido.deleted_count} documento removido (CVE-2024-002)")
    print(f"Total na colecao agora: {colecao.count_documents({})}")


if __name__ == "__main__":
    main()
