"""Exercicio 8 - Deteccao de anomalias com IsolationForest.

Aprendizado NAO supervisionado: nao ha rotulos: o modelo isola pontos
que se afastam do comportamento tipico. Convencao do sklearn:
  -1 = anomalia   |   1 = normal
contamination=0.25 -> espera-se ~25% (2 de 8) de anomalias.
"""

import numpy as np
from sklearn.ensemble import IsolationForest

from config import titulo

# [requisicoes_min, conexoes_simultaneas]
trafego = np.array([
    [100, 5], [120, 6], [110, 5], [105, 4], [50000, 500], [109, 5], [111, 6], [45000, 450],
])


def main():
    titulo("EXERCICIO 8 - Deteccao de anomalias (Isolation Forest)")

    modelo = IsolationForest(contamination=0.25, random_state=42)
    predicoes = modelo.fit_predict(trafego)
    scores = modelo.decision_function(trafego)  # quanto menor, mais anomalo

    for indice, (amostra, predicao, score) in enumerate(zip(trafego, predicoes, scores)):
        veredito = "ANOMALIA" if predicao == -1 else "Normal"
        print(f"Amostra {indice}: [{amostra[0]}, {amostra[1]}] -> {veredito} "
              f"(score {score:+.3f})")

    anomalias = [int(i) for i, p in enumerate(predicoes) if p == -1]
    print(f"\nTotal de anomalias: {len(anomalias)} -> indices {anomalias}")
    print("Leitura de seguranca: picos de requisicoes/min com centenas de "
          "conexoes simultaneas tem cara de DoS ou scan automatizado.")


if __name__ == "__main__":
    main()
