"""Exercicio 1 - Modelagem e CRUD SQL (MySQL).

Tabela ativos(id PK AUTO_INCREMENT, nome, ip UNIQUE, tipo,
              criticidade ENUM('baixa','media','alta'), status)

Cobre: CREATE, INSERT, SELECT filtrado, UPDATE, DELETE e tratamento
do erro de UNIQUE ao tentar inserir um IP repetido.
"""

from mysql.connector import IntegrityError

from config import get_mysql_connection, titulo

DDL_ATIVOS = """
CREATE TABLE IF NOT EXISTS ativos (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    nome        VARCHAR(60)  NOT NULL,
    ip          VARCHAR(45)  NOT NULL UNIQUE,
    tipo        VARCHAR(30)  NOT NULL,
    criticidade ENUM('baixa','media','alta') NOT NULL DEFAULT 'baixa',
    status      VARCHAR(20)  NOT NULL DEFAULT 'ativo'
)
"""

ativos = [
    ("SRV-WEB01", "192.168.1.10", "servidor", "alta", "ativo"),
    ("PC-RH03", "192.168.1.45", "estacao", "baixa", "ativo"),
    ("SW-CORE01", "192.168.1.1", "switch", "media", "inativo"),
]


def main():
    conexao = get_mysql_connection()
    cursor = conexao.cursor()

    titulo("EXERCICIO 1 - CRUD SQL na tabela 'ativos'")

    # --- CREATE -------------------------------------------------------
    # DROP antes do CREATE so para o script ser reexecutavel em laboratorio.
    cursor.execute("DROP TABLE IF EXISTS ativos")
    cursor.execute(DDL_ATIVOS)
    print("Tabela 'ativos' criada.")

    # --- INSERT (sempre parametrizado, nunca concatenando) ------------
    cursor.executemany(
        "INSERT INTO ativos (nome, ip, tipo, criticidade, status) "
        "VALUES (%s, %s, %s, %s, %s)",
        ativos,
    )
    conexao.commit()
    print(f"{cursor.rowcount} ativos inseridos.\n")

    # --- READ com filtro ---------------------------------------------
    print("Listar tipo='servidor':")
    cursor.execute(
        "SELECT nome, ip, criticidade, status FROM ativos WHERE tipo = %s",
        ("servidor",),
    )
    for nome, ip, criticidade, status in cursor.fetchall():
        print(f"  {nome} | {ip} | {criticidade} | {status}")

    # --- UPDATE -------------------------------------------------------
    cursor.execute(
        "UPDATE ativos SET status = %s WHERE nome = %s",
        ("ativo", "SW-CORE01"),
    )
    conexao.commit()
    print(f"\n{cursor.rowcount} registro atualizado (SW-CORE01 -> ativo)")

    # --- UNIQUE violado ----------------------------------------------
    try:
        cursor.execute(
            "INSERT INTO ativos (nome, ip, tipo, criticidade, status) "
            "VALUES (%s, %s, %s, %s, %s)",
            ("SRV-CLONE", "192.168.1.10", "servidor", "alta", "ativo"),
        )
        conexao.commit()
    except IntegrityError as erro:
        conexao.rollback()
        print(f"\n[UNIQUE] IP 192.168.1.10 duplicado recusado pelo banco: {erro.msg}")

    # --- DELETE -------------------------------------------------------
    cursor.execute("DELETE FROM ativos WHERE nome = %s", ("PC-RH03",))
    conexao.commit()
    print(f"\n{cursor.rowcount} registro removido (PC-RH03)")

    # --- Estado final -------------------------------------------------
    cursor.execute("SELECT id, nome, ip, tipo, criticidade, status FROM ativos ORDER BY id")
    print("\nInventario final:")
    for linha in cursor.fetchall():
        print("  ", " | ".join(str(campo) for campo in linha))

    cursor.close()
    conexao.close()


if __name__ == "__main__":
    main()
