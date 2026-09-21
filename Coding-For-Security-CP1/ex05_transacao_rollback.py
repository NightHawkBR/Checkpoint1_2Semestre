"""Exercicio 5 - Transacao com rollback (transferencia entre contas).

Atomicidade: debito e credito sao uma unica unidade de trabalho. Se o
credito falhar (conta destino inexistente), o rollback desfaz o debito
e o saldo da origem fica intacto.
"""

from mysql.connector import Error as MySQLError

from config import get_mysql_connection, titulo

contas = [(1, "Alice", 1000), (2, "Bob", 500)]


def preparar(conexao):
    cursor = conexao.cursor()
    cursor.execute("DROP TABLE IF EXISTS contas")
    cursor.execute(
        """
        CREATE TABLE contas (
            id      INT PRIMARY KEY,
            titular VARCHAR(40) NOT NULL,
            saldo   DECIMAL(10,2) NOT NULL
        ) ENGINE=InnoDB
        """
    )  # InnoDB e obrigatorio: MyISAM nao suporta transacao
    cursor.executemany("INSERT INTO contas (id, titular, saldo) VALUES (%s, %s, %s)", contas)
    conexao.commit()
    cursor.close()


def saldos(conexao):
    cursor = conexao.cursor()
    cursor.execute("SELECT titular, saldo FROM contas ORDER BY id")
    dados = {titular: int(saldo) for titular, saldo in cursor.fetchall()}
    cursor.close()
    return dados


def transferir(conexao, id_origem, id_destino, valor):
    """Devolve (True, None) em caso de commit ou (False, motivo) em rollback."""
    cursor = conexao.cursor()
    try:
        conexao.start_transaction()

        # Debita apenas se a origem existir E tiver saldo suficiente
        cursor.execute(
            "UPDATE contas SET saldo = saldo - %s WHERE id = %s AND saldo >= %s",
            (valor, id_origem, valor),
        )
        if cursor.rowcount == 0:
            raise ValueError("conta origem inexistente ou saldo insuficiente")

        # Credita no destino
        cursor.execute(
            "UPDATE contas SET saldo = saldo + %s WHERE id = %s",
            (valor, id_destino),
        )
        if cursor.rowcount == 0:
            raise ValueError("conta destino inexistente")

        conexao.commit()
        return True, None
    except (ValueError, MySQLError) as erro:
        conexao.rollback()  # desfaz o debito ja aplicado nesta transacao
        return False, str(erro)
    finally:
        cursor.close()


def main():
    conexao = get_mysql_connection()
    preparar(conexao)

    titulo("EXERCICIO 5 - Transacao com rollback")
    print(f"Saldos iniciais: {saldos(conexao)}\n")

    # Transferencia valida -> commit
    ok, motivo = transferir(conexao, 1, 2, 200)
    atual = saldos(conexao)
    print(f"Transferencia 1 {'OK' if ok else 'FALHOU'}. "
          f"Alice={atual['Alice']}, Bob={atual['Bob']}")

    # Transferencia para conta inexistente -> rollback
    antes = saldos(conexao)["Alice"]
    ok, motivo = transferir(conexao, 1, 99, 100)
    depois = saldos(conexao)["Alice"]
    print(f"Transferencia 2 {'OK' if ok else 'FALHOU'} ({motivo}). Rollback. Alice={depois}")
    print(f"\nProva de atomicidade: saldo de Alice antes={antes} depois={depois} "
          f"-> {'INALTERADO' if antes == depois else 'ALTERADO (bug!)'}")

    conexao.close()


if __name__ == "__main__":
    main()
