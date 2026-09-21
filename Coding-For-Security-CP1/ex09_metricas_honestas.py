"""Exercicio 9 - Metricas honestas em dataset desbalanceado.

y_true: 8 normais (0) e 2 ataques (1)
y_pred: o modelo acertou os 8 normais, pegou 1 ataque e PERDEU 1 ataque.

POR QUE A ACURACIA SOZINHA ENGANA AQUI (comentario pedido):
  A base tem 80% de trafego normal. Um modelo que chutasse "normal"
  para tudo teria 0.80 de acuracia sem detectar um unico ataque. Os
  0.90 obtidos mascaram o que importa em seguranca: o recall de 0.50
  significa que METADE dos ataques passou (falso negativo = incidente
  nao detectado). Em deteccao, olhe recall e F1 da classe positiva.
"""

from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)

from config import titulo

y_true = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]  # 8 normais, 2 ataques
y_pred = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]  # perdeu 1 ataque


def main():
    titulo("EXERCICIO 9 - Metricas honestas (base desbalanceada)")

    matriz = confusion_matrix(y_true, y_pred)
    print(f"Matriz: {matriz.tolist()}")
    vn, fp, fn, vp = matriz.ravel()
    print(f"  Verdadeiro Negativo={vn}  Falso Positivo={fp}")
    print(f"  Falso Negativo={fn}       Verdadeiro Positivo={vp}")

    acuracia = accuracy_score(y_true, y_pred)
    precisao = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)

    print(f"\nAcuracia: {acuracia:.2f} | Precisao: {precisao:.2f} | "
          f"Recall: {recall:.2f} | F1: {f1:.2f}")

    # Baseline burro: classificar tudo como normal
    baseline = accuracy_score(y_true, [0] * len(y_true))
    print(f"\nBaseline 'chutar sempre normal': acuracia {baseline:.2f} e recall 0.00")

    print(f"\nComentario: acuracia {acuracia:.2f} mascara que METADE dos ataques "
          f"passou (recall {recall:.2f}). {fn} ataque(s) virou falso negativo.")


if __name__ == "__main__":
    main()
