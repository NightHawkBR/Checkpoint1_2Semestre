"""Roda os 10 exercicios em sequencia (util para conferir tudo de uma vez).

Uso:
    python run_all.py           # todos
    python run_all.py 7 8 9     # apenas os exercicios indicados
    python run_all.py ml        # apenas os de ML (7 a 9), sem precisar de banco
"""

import sys
import traceback

EXERCICIOS = {
    1: ("ex01_crud_mysql", "MySQL"),
    2: ("ex02_crud_pymongo", "MongoDB"),
    3: ("ex03_agregacao_top_ips", "MongoDB"),
    4: ("ex04_sql_injection", "MySQL"),
    5: ("ex05_transacao_rollback", "MySQL"),
    6: ("ex06_indice_desempenho", "MongoDB"),
    7: ("ex07_classificador_trafego", "-"),
    8: ("ex08_deteccao_anomalias", "-"),
    9: ("ex09_metricas_honestas", "-"),
    10: ("ex10_pipeline_siem", "MongoDB"),
}


def escolher(argumentos):
    if not argumentos:
        return list(EXERCICIOS)
    if argumentos[0].lower() == "ml":
        return [7, 8, 9]
    return [int(a) for a in argumentos]


def main():
    for numero in escolher(sys.argv[1:]):
        modulo_nome, dependencia = EXERCICIOS[numero]
        print(f"\n\n>>> Exercicio {numero} ({modulo_nome}.py) | requer: {dependencia}")
        try:
            modulo = __import__(modulo_nome)
            modulo.main()
        except SystemExit as erro:  # get_mongo_db/get_mysql_connection chamam sys.exit
            print(f"[PULADO] {erro}")
        except Exception:
            print(f"[FALHOU] Exercicio {numero}:")
            traceback.print_exc()


if __name__ == "__main__":
    main()
