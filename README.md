# Obligatorio 2 - Sistemas Multiagente

Implementación y experimentación de algoritmos multiagente en juegos alternados e información imperfecta.

**Autor:** Juan Irabedra (212375)

## Algoritmos

- MiniMax
- Monte Carlo Tree Search (MCTS)
- Counterfactual Regret Minimization (CFR)
- Information Set MCTS (ISMCTS)

## Ambientes

| Juego | Algoritmos | Notebook |
|---|---|---|
| Tic-Tac-Toe | MiniMax, MCTS | `TicTacToe.ipynb` |
| Nocca-Nocca | MiniMax, MCTS | `Nocca_Nocca.ipynb` |
| Kuhn Poker (2p) | CFR, MCTS, ISMCTS | `cfr/KuhnPoker.ipynb` |
| Kuhn Poker (3p) | CFR, ISMCTS | `cfr/KuhnPoker_ThreePlayer.ipynb` |
| Leduc Hold'em | CFR, ISMCTS | `cfr/Leduc.ipynb` |

## Setup

Requiere Python 3.11. Con [uv](https://docs.astral.sh/uv/):

```bash
uv sync
```

Kernel de Jupyter:

```bash
uv run python -m ipykernel install --user --name alternating-games --display-name "Python (alternating-games)"
```

## Documentación

Informe de experimentos en `documentacion_entrega/entrega_alternativa.md`.
