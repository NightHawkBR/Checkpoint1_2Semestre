"""Exercicio 7 - Classificador de trafego (RandomForestClassifier).

Features: [bytes, porta, duracao]  |  Rotulo: 0 = normal, 1 = malicioso
random_state fixo em 42 no split e no modelo -> resultado reprodutivel.
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split

from config import titulo

X = np.array([
    [500, 80, 0.1], [1200, 80, 0.5], [64, 22, 0.02], [64000, 4444, 10.0], [45000, 8080, 15.0],
    [60000, 31337, 20.0], [800, 443, 0.3], [300, 53, 0.05], [55000, 9999, 18.0], [200, 25, 0.2],
])
y = np.array([0, 0, 0, 1, 1, 1, 0, 0, 1, 0])
caso_novo = [[58000, 4444, 16.0]]

ROTULOS = {0: "Normal", 1: "Malicioso"}


def main():
    titulo("EXERCICIO 7 - Classificador de trafego (Random Forest)")

    X_treino, X_teste, y_treino, y_teste = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    print(f"Amostras: {len(X)} total -> {len(X_treino)} treino / {len(X_teste)} teste")

    modelo = RandomForestClassifier(n_estimators=100, random_state=42)
    modelo.fit(X_treino, y_treino)

    y_predito = modelo.predict(X_teste)
    print(f"\nAcuracia no teste: {accuracy_score(y_teste, y_predito):.2f}")
    print("\nRelatorio por classe:")
    print(classification_report(y_teste, y_predito, zero_division=0))

    # --- Classificacao de um caso novo -------------------------------
    predicao = int(modelo.predict(caso_novo)[0])
    confianca = modelo.predict_proba(caso_novo)[0][predicao]
    print(f"Caso novo {caso_novo[0]} -> {ROTULOS[predicao]} ({predicao}) "
          f"| confianca {confianca:.2f}")

    # Bonus: qual feature mais pesou na decisao
    nomes = ["bytes", "porta", "duracao"]
    print("\nImportancia das features:")
    for nome, peso in zip(nomes, modelo.feature_importances_):
        print(f"  {nome:8s} {peso:.3f}")


if __name__ == "__main__":
    main()
