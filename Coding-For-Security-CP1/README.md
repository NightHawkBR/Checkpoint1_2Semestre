# CP1 — Coding for Security (2º Semestre)

Resolução dos 10 exercícios do [cp1_2semestre.md](cp1_2semestre.md).

## Ambiente

```powershell
# 1. Subir os bancos
docker compose up -d

# 2. Instalar dependências (de preferência num venv)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Credenciais padrão: MySQL `root`/`root` em `127.0.0.1:3306`, MongoDB em `localhost:27017`.
Ambos os bancos usam o database `cp1_seguranca`. Para mudar, defina variáveis de ambiente
antes de rodar (ver [config.py](config.py)):

```powershell
$env:MYSQL_PASSWORD = "senha123"
$env:MONGO_URI = "mongodb://localhost:27018/"
```

## Como rodar

```powershell
python ex01_crud_mysql.py     # um exercício
python run_all.py             # todos os 10 em sequência
python run_all.py 7 8 9       # só os indicados
python run_all.py ml          # só os de ML (não precisam de banco)
```

Todos os scripts limpam suas tabelas/coleções no início, então podem ser reexecutados
quantas vezes quiser sem duplicar dados.

## Exercícios

| # | Arquivo | Tema | Requer |
|---|---------|------|--------|
| 1 | [ex01_crud_mysql.py](ex01_crud_mysql.py) | CRUD SQL, `ENUM`, `UNIQUE` tratado | MySQL |
| 2 | [ex02_crud_pymongo.py](ex02_crud_pymongo.py) | CRUD com PyMongo | MongoDB |
| 3 | [ex03_agregacao_top_ips.py](ex03_agregacao_top_ips.py) | Aggregation pipeline — top 3 IPs com FAIL | MongoDB |
| 4 | [ex04_sql_injection.py](ex04_sql_injection.py) | Query insegura vs parametrizada | MySQL |
| 5 | [ex05_transacao_rollback.py](ex05_transacao_rollback.py) | Transação com `rollback` | MySQL |
| 6 | [ex06_indice_desempenho.py](ex06_indice_desempenho.py) | 1000 eventos, índice em `ip`, `explain()` | MongoDB |
| 7 | [ex07_classificador_trafego.py](ex07_classificador_trafego.py) | `RandomForestClassifier` | — |
| 8 | [ex08_deteccao_anomalias.py](ex08_deteccao_anomalias.py) | `IsolationForest` | — |
| 9 | [ex09_metricas_honestas.py](ex09_metricas_honestas.py) | Acurácia vs recall em base desbalanceada | — |
| 10 | [ex10_pipeline_siem.py](ex10_pipeline_siem.py) | Pipeline log → MongoDB → ML | MongoDB |

O exercício 10 lê [data/auth.log](data/auth.log) — 23 linhas no formato
`TIMESTAMP TIPO usuario=NOME ip=IP`, com as contagens que o enunciado espera
(10 / 5 / 3 FAILs). Se você tiver o `auth.log` original da GS do 1º semestre,
basta substituir o arquivo.

## Notas de correção

- **Queries parametrizadas** (`%s` + tupla) em todos os exercícios de MySQL. A única
  concatenação existe em `buscar_inseguro()` do exercício 4, que é o alvo da demonstração.
- **Erros de conexão** tratados em [config.py](config.py): tanto MongoDB quanto MySQL
  falham com mensagem clara em vez de stack trace.
- **`random_state=42`** fixo em todo split e todo modelo, para reprodutibilidade.
- **Agregação no banco** (`$match`/`$group`/`$sort`/`$limit`) nos exercícios 3 e 10,
  em vez de contagem com laço em Python.
- O exercício 5 usa `ENGINE=InnoDB` explicitamente — MyISAM não suporta transação.

## Status de validação

Exercícios 7, 8 e 9 foram executados e a saída bate com a esperada no enunciado
(acurácia 1.00, anomalias nos índices 4 e 7, matriz `[[8,0],[1,1]]` com
0.90 / 1.00 / 0.50 / 0.67). O parsing do `auth.log` e a previsão do exercício 10
foram validados offline (23 eventos, 10/5/3 FAILs, IP com 8 falhas → suspeito).
Os exercícios que dependem de MySQL/MongoDB (1–6 e a parte de banco do 10) ainda
precisam ser rodados com os containers de pé.
