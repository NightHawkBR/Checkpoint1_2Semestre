"""Exercicio 4 - Query parametrizada como defesa contra SQL Injection.

EXERCICIO DEFENSIVO: a funcao insegura existe apenas para demonstrar o
vazamento no banco local de laboratorio. Em codigo real, use SEMPRE a
versao parametrizada (buscar_seguro).

Diferenca:
  inseguro -> a entrada do usuario e concatenada e vira PARTE DA QUERY.
  seguro   -> a entrada viaja como PARAMETRO, tratada como texto puro.
"""

from config import get_mysql_connection, titulo

usuarios = [("admin", "admin@x.com"), ("ana", "ana@x.com"), ("bruno", "bruno@x.com")]
entrada = "' OR '1'='1"


def preparar(conexao):
    cursor = conexao.cursor()
    cursor.execute("DROP TABLE IF EXISTS usuarios")
    cursor.execute(
        """
        CREATE TABLE usuarios (
            id    INT AUTO_INCREMENT PRIMARY KEY,
            nome  VARCHAR(40) NOT NULL,
            email VARCHAR(80) NOT NULL
        )
        """
    )
    cursor.executemany("INSERT INTO usuarios (nome, email) VALUES (%s, %s)", usuarios)
    conexao.commit()
    cursor.close()


def buscar_inseguro(conexao, nome):
    """VULNERAVEL: interpola a entrada direto na string SQL."""
    cursor = conexao.cursor()
    query = f"SELECT nome, email FROM usuarios WHERE nome = '{nome}'"
    print(f"  SQL montado: {query}")
    cursor.execute(query)
    linhas = cursor.fetchall()
    cursor.close()
    return linhas


def buscar_seguro(conexao, nome):
    """SEGURO: placeholder %s + tupla de parametros (prepared statement)."""
    cursor = conexao.cursor()
    query = "SELECT nome, email FROM usuarios WHERE nome = %s"
    print(f"  SQL montado: {query}  -- parametro: {nome!r}")
    cursor.execute(query, (nome,))
    linhas = cursor.fetchall()
    cursor.close()
    return linhas


def main():
    conexao = get_mysql_connection()
    preparar(conexao)

    titulo("EXERCICIO 4 - SQL Injection: inseguro vs parametrizado")

    print(f"[INSEGURO] entrada={entrada}")
    vazados = buscar_inseguro(conexao, entrada)
    print(f"  -> {len(vazados)} usuarios (VAZAMENTO)")
    for nome, email in vazados:
        print(f"     {nome} | {email}")

    print(f"\n[SEGURO]   entrada={entrada}")
    resultado = buscar_seguro(conexao, entrada)
    print(f"  -> {len(resultado)} usuarios (defesa OK)")

    # Prova de que a versao segura continua funcionando para entradas legitimas
    print("\n[SEGURO]   entrada=ana (busca legitima)")
    for nome, email in buscar_seguro(conexao, "ana"):
        print(f"     {nome} | {email}")

    conexao.close()


if __name__ == "__main__":
    main()
