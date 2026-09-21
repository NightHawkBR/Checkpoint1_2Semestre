"""Exercicio 10 (Desafio) - Mini-pipeline SIEM: log -> MongoDB -> ML.

Etapas:
  1. Le data/auth.log e normaliza cada linha em um documento.
  2. Insere todos no MongoDB (insert_many).
  3. Agregacao conta FAILs por IP (trabalho feito no banco).
  4. Dataset [qtd_fails] rotulado por regra: >= 5 falhas -> suspeito (1).
  5. Treina classificador e preve o rotulo de um IP novo com 8 falhas.
"""

import re
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
from sklearn.ensemble import RandomForestClassifier

from config import get_mongo_db, titulo

CAMINHO_LOG = Path(__file__).parent / "data" / "auth.log"
LIMIAR_SUSPEITO = 5
FALHAS_IP_NOVO = 8

# TIMESTAMP TIPO usuario=NOME ip=IP
PADRAO_LINHA = re.compile(
    r"^(?P<data>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+"
    r"(?P<tipo>FAIL|OK)\s+"
    r"usuario=(?P<usuario>\S+)\s+"
    r"ip=(?P<ip>\S+)$"
)

PIPELINE_FAILS_POR_IP = [
    {"$match": {"tipo": "FAIL"}},
    {"$group": {"_id": "$ip", "fails": {"$sum": 1}}},
    {"$sort": {"fails": -1}},
]


def ler_e_normalizar(caminho):
    """Etapa 1: cada linha do log vira um dicionario estruturado."""
    if not caminho.exists():
        sys.exit(f"[ERRO] Log nao encontrado: {caminho}")

    documentos, ignoradas = [], 0
    with caminho.open(encoding="utf-8") as arquivo:
        for linha in arquivo:
            linha = linha.strip()
            if not linha:
                continue
            achado = PADRAO_LINHA.match(linha)
            if not achado:
                ignoradas += 1  # linha malformada nao derruba o pipeline
                continue
            campos = achado.groupdict()
            documentos.append(
                {
                    "timestamp": datetime.strptime(campos["data"], "%Y-%m-%d %H:%M:%S"),
                    "tipo": campos["tipo"],
                    "usuario": campos["usuario"],
                    "ip": campos["ip"],
                }
            )
    if ignoradas:
        print(f"[AVISO] {ignoradas} linha(s) fora do formato foram ignoradas.")
    return documentos


def main():
    titulo("EXERCICIO 10 - Mini-pipeline SIEM (log -> MongoDB -> ML)")

    # --- 1 e 2: normalizar e inserir ---------------------------------
    documentos = ler_e_normalizar(CAMINHO_LOG)
    db = get_mongo_db()
    colecao = db["siem_auth"]
    colecao.delete_many({})
    colecao.insert_many(documentos)
    print(f"Eventos inseridos no MongoDB: {colecao.count_documents({})}")

    # --- 3: agregacao por IP -----------------------------------------
    contagem = list(colecao.aggregate(PIPELINE_FAILS_POR_IP))
    print("\nFalhas por IP (agregacao):")
    for doc in contagem:
        rotulo = 1 if doc["fails"] >= LIMIAR_SUSPEITO else 0
        print(f"  {doc['_id']:<16} -> {doc['fails']:>2} FAILs (suspeito={rotulo})")

    # --- 4: dataset rotulado -----------------------------------------
    X_log = [[doc["fails"]] for doc in contagem]
    y_log = [1 if doc["fails"] >= LIMIAR_SUSPEITO else 0 for doc in contagem]

    # Os 3 IPs do log sao pouquissimas amostras para um modelo aprender a
    # fronteira. Reforcamos o treino com exemplos sinteticos de 0 a 12
    # falhas, rotulados pela mesma regra de negocio (>= 5 -> suspeito).
    X_sintetico = [[n] for n in range(0, 13)]
    y_sintetico = [1 if n >= LIMIAR_SUSPEITO else 0 for n in range(0, 13)]

    X = np.array(X_log + X_sintetico)
    y = np.array(y_log + y_sintetico)
    print(f"\nDataset de treino: {X_log} rotulos {y_log} "
          f"(+ {len(X_sintetico)} amostras sinteticas de reforco)")

    # --- 5: treino e previsao ----------------------------------------
    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X, y)

    ip_novo = [[FALHAS_IP_NOVO]]
    predicao = int(modelo.predict(ip_novo)[0])
    confianca = modelo.predict_proba(ip_novo)[0][predicao]
    veredito = "Suspeito" if predicao == 1 else "Normal"
    print(f"\nPrevisao para IP com {FALHAS_IP_NOVO} falhas -> {veredito} ({predicao}) "
          f"| confianca {confianca:.2f}")

    # Sanity check da fronteira aprendida pelo modelo
    print("\nFronteira aprendida (qtd_fails -> rotulo previsto):")
    for n in range(0, 11):
        print(f"  {n:>2} falhas -> {int(modelo.predict([[n]])[0])}")


if __name__ == "__main__":
    main()
