# Obligatorio 2 - Sistemas Multiagente
- Agustina Disiot 221025
- Juan Irabedra 212375


## Resumen del documento

Este documento lo estructuramos por juego/ambiente. Para cada juego que se pide: TicTacToe, Nocca Nocca, Khun2, Khun3 y Leduc, vamos a presentar los experimentos que hicimos, los resultados que obtuvimos y otros supuestos o conclusiones que sacamos de cada uno.

## TicTacToe

Primero, nos familiarizamos con el estilo de impresión de tableros en la notebook:

![image](./ticatactoe/tablero.png)

Luego, dejamos agentes Random jugar 10 juegos entre ellos. Obtuvimos:

```
Agent X average reward: 0.2 over 10 games

Agent X rewards: [0, 1, 0, -1, -1, 0, 0, 1, 1, 1]

Agent O average reward: -0.2 over 10 games

Agent O rewards: [0, -1, 0, 1, 1, 0, 0, -1, -1, -1]
```

Esto nos confirma que el juego se está comportando como suma 0, lo cual es correcto en TicTacToe.

Luego validamos con pruebas cortas MiniMax y nuestra implementación de MCTS.

![image](./ticatactoe/val%20mcts%20minimax.png)

Lo que concluimos de esta primera prueba es que todas nuestras versiones de agentes MCTS y Minimax le ganan siempre a Random. No siempre le ganan por la misma distancia. Vemos que los Minimax con menor profundidad así como los MCTS con menos cantidad de simulaciones y rollouts ganan por menos diferencia a Random que los Minimax y MCTS con profundidad mayor (2, por ejemplo) o simulaciones/rollouts mayores (50/5). 

También influye qué agente juega primero; pero en cualquier escenario, comparando mismo orden de comienzo, la profundidad mayor o mayor configuración de simulaciones/rollouts de MCTS dan ventaja superior contra el agente Random.

## Minimax vs MCTS

En el siguiente heatmap vamos a ver las rewards promedio de algunas configuraciones de Minimax contra configuraciones de MCTS:

![image](./ticatactoe/mctsvsminimax.png)

En este heatmap vemos las rewards promedio de el primer agente que juega. En el heatmap de la izquierda es MCTS. En el heatmap de la derecha es Minimax. 

Vemos que cuando empieza MCTS, le va mejor cuando el minimax tiene poca profundida. A medida que Minimax tiene mayor profundidad, no siempre podemos concluir que MCTS mejora estrictamente, porque vemos en Minimax(2) contra MCTS tanto 25/3 como 50/5 que la utilidad esperada no es tan alta. Sin embargo, contra Minimax con profundidad max. 4, vemos una mejora para los MCTS mejor tuneados.

Cuando empieza minimax, vemos una tendencia mucho más fácil de interpretar: mayor profundidad de minimax nos garantiza mayor utilidad esperada contra MCTS idénticos. Es decir, si leemos verticalmente el heatmap, las columnas siempre con crecentes a medida que aumenta la complejidad del minimax. Esto se verifica para todos los MCTS que probamos.

No estamos seguros por qué, pero minimax es más predecible contra MCTS cuando empieza a jugar.

## Experimentos con Minimax

El siguiente gráfico se puede leer de la siguiente forma: la primera fila usa solamente la función de evaluación original de TicTacToe (la que cuenta líneas aún disponibles para ganar). La segunda fila usa otra función de evaluación (la base + un escalar por tener ocupada la casilla del centro + un escalar por esquinas ocupadas).

Además, compara la utilidad esperada en el heatmap de la izquierda de dos Minimaxes jugando con diferentes combinaciones de profundidades, y a la derecha, para la misma combinación de profundidades se muestra cuánto tiempo toda calcular la utilidad. 

![image](./ticatactoe/minimaxvsminimax.png)

Lo primer que se observa sin esfuerzo es que a mayor profundidad, mayor tiempo de ejecución. Es decir, a medida que bajamos por el heatmap y nos acercamos a la dereha, el tiempo de ejecución crece. Crece para ambas funciones de evaluación. Vemos que la función de evaluación original es un poco más lenta computacionalmente que la segunda que probamos. 

Lo interesante acá son las utilidades. Vemos que hay una tendencia a empatar, o estar cerca del empate. Esto tiene sentido porque los agentes intentarán converger a un equilibrio, porque Minimax nos garantiza eso: un equilibrio Minimax. Sin embargo vevmos que hay algunos casos anómalos como Minimax(4) vs Minimax(5) con la evaluación original o Minimax(5) vs Minimax(5) con la función de evaluación alternativa. Esto puede tener que ver con el orden de jugadores.


## Comparación de agentes

En esta sección jugamos diferentes agentes en diferente orden y calculamos la utilidad promedio. Jugaron 50 veces cada combinación de agentes para nosotros calcular la utilidad esperada.  

Esta gráfica se lee: viendo los x_ticks del plot podemos ver qué agente juega X y qué agente juega O. Además, vemos una barra con la recompensa esperada para el agente que juega X. Es decir, si la barra tiene altura positiva, entonces ganó en promedio X, si no, ganó el agente que jugó O.

![image](./ticatactoe/comparacionagentes1.png)

Una primera observación valiosa es que nunca gana Random. Luego, cuando juega Minimax(2) contra MCTS(25/3), gana Minimax. Cuando juega Minimax(4) contra MCTS(50/5) gana quien jugó primero. Esto confirma el comportamiento que vimos en el primer heatmap, donde no es tan fácil asegurar si gana MCTS o Minimax sin saber quién juega primero. 

## Experimento para encontrar equilibrio Minimax o de Nash

Por último pusimos a prueba el equilibrio que conocemos de TicTacToe. Para esto hicimos 3 experimentos:


- Pusimos a jugar Minimax(9) vs Minimax(9). En 10 juegos tuvimos 10 empates. Es decir, convergieron al equilibrio. 
- Pusimos a jugar un Minimax(9) contra un Minimax(3). El Minimax(9) nunca necesitó cambiar su estrategia para ganar. Ganó siempre.
- Hicimos la matriz de rewards y encontramos que cuando permitimos profundidades altas de ambos Minimax, siempre empatan. 

Entonces, explicamos que logramos probar que con agentes Minimax con profundidad máxima para este juego, tenemos un equilibrio.

![image](./ticatactoe/equilibrio%20minimax.png)

## Nocca Nocca

Primero, me familiaricé con el formato de impresión del tablero:

![image](./noccanocca/tablero%20nocca.png)

Luego, validé un par de juegos:

```
MiniMax depth=1 vs Random {'Black': np.float64(1.0), 'White': np.float64(-1.0)}
p0: Random vs MiniMax depth=1 {'Black': np.float64(-1.0), 'White': np.float64(1.0)}
p0: MiniMax depth=2 vs Random {'Black': np.float64(1.0), 'White': np.float64(-1.0)}
p0: Random vs MiniMax depth=2 {'Black': np.float64(-1.0), 'White': np.float64(1.0)}
p0: MCTS sim=5, rollouts=1 vs Random {'Black': np.float64(0.0), 'White': np.float64(0.0)}
p0: Random vs MCTS sim=5, rollouts=1 {'Black': np.float64(-0.2), 'White': np.float64(0.2)}
p0: MCTS sim=10, rollouts=2 vs Random {'Black': np.float64(1.0), 'White': np.float64(-1.0)}
p0: Random vs MCTS sim=10, rollouts=2 {'Black': np.float64(-0.6), 'White': np.float64(0.6)}
p1: MiniMax depth=1 vs Random {'Black': np.float64(1.0), 'White': np.float64(-1.0)}
p1: Random vs MiniMax depth=1 {'Black': np.float64(-1.0), 'White': np.float64(1.0)}
p1: MiniMax depth=2 vs Random {'Black': np.float64(1.0), 'White': np.float64(-1.0)}
p1: Random vs MiniMax depth=2 {'Black': np.float64(-1.0), 'White': np.float64(1.0)}
p1: MCTS sim=5, rollouts=1 vs Random {'Black': np.float64(0.2), 'White': np.float64(-0.2)}
p1: Random vs MCTS sim=5, rollouts=1 {'Black': np.float64(0.2), 'White': np.float64(-0.2)}
p1: MCTS sim=10, rollouts=2 vs Random {'Black': np.float64(1.0), 'White': np.float64(-1.0)}
p1: Random vs MCTS sim=10, rollouts=2 {'Black': np.float64(-0.6), 'White': np.float64(0.6)}
p0: MiniMax depth=1 con eval movilidad {'Black': np.float64(0.2), 'White': np.float64(-0.2)}
```

Revisé que el juego se comporte realmente como suma 0 y jugué con las funciones de evaluación. 

### Funciones de evaluación

#### Componentes individuales

Tres métricas base definidas en `nocca_nocca.py`, todas en [0, 1]:

- **`_eval_progress`**: progreso promedio normalizado de todas las piezas propias hacia la fila meta/del oponente.
- **`_eval_closest_to_goal`**: progreso normalizado de la pieza propia más avanzada. Es interesa porque refleja la condición de victoria: que una pieza llegue a la meta del otro.
- **`_eval_blocked`**: fracción de piezas propias con una pieza rival encima en la misma pila (bloqueadas).

#### Funciones de evaluación usadas

| Nombre | Fórmula | Notas |
|---|---|---|
| **`eval_base`** (default) | `0.5 · progress − 0.5 · blocked` | Evalúa solo al agente propio |
| **`eval_closest`** | `closest` | Solo la pieza más avanzada; ignora las demás |
| **`eval_progress_closest`** | `0.5 · progress + 0.5 · closest` | Pondera avance global y avance de la que mejor va |
| **`eval_progress_closest_blocked`** | `0.35 · progress + 0.45 · closest − 0.20 · blocked` | Agrega penalización por bloqueo |
| **`eval_relative`** | `score(agente) − score(rival)` con pesos `closest=0.45, progress=0.35, blocked=0.20` | Diferencial respecto al rival; suma-cero natural |
| **`NoccaNoccaRelativeEval.eval`** | `own_score − opp_score + 0.20 · mobility` | `own_score = 0.50·closest + 0.30·progress − 0.20·blocked`; `mobility = (movs_propios − movs_rival) / (movs_propios + movs_rival)` ∈ [−1, 1] |

En todas tuve que elegir ponderadores para cada componente. Los elegí cercanos a 1/n siendo n la cantidad de componentes. No hice tuneo de estos componentes porque me pareció que era mejor experimentar con agentes que con finetuning de parámetros de funciones de evaluación.


### Evaluación de Minimax

Primero, puse a jugar Minimaxes entre ellos con diferentes profundidades hasta 2. Usé dos evaluaciones: la base y la de comparación relativa con el rival.

![image](./noccanocca/minimax%20comparison.png)

El problema con Nocca Nocca es que hacer el minimax con profundidades altas se vuelve infactible. Al final de la notebook menciono alphabeta pruning como mejora; la implementé pero también me encontré con que explota para profundidades altas (4, 5 ya se vuelve imposible).

A pesar de la experimentación, no veo patrones que pueda extraer de la experimentación hasta profundidad 2, con ninguna de las funciones de evaluación. Me hace sentido por la poca profundidad del árbol que estoy usando.

### Evaluación de Minimax, MCTS y Random

Hice una corrida de Minimaxes, MCTS y Randoms entre ellos. Al ser agentes poco poderosos en el sentido de que o bien tienen pocos rollouts/sims o bien tienen poca depth, hubo partidas truncadas en 80 steps. Eso explica por qué algunas configuraciones no llegan a reward 1. Fuera de esto, no hay mucho para concluir a partir de esta gráfica.

![image](./noccanocca/minimax%20mcts%20random.png)

### Evaluación de Minimax vs MCTS

Luego, largué 3 juegos para cada configuración de par de agentes. De nuevo 80 pasos. Siempre comenza Black.

![image](./noccanocca/mctsvsminimax.png)

Con los parámetros que fui probando, Minimax siempre desempeña mejor que MCTS para Nocca Nocca cuando juegan entre ellos. Y en general, los modelos más simples son mucho más rápidos.

A diferencia de TicTacToe, acá quien empieza no cambia mucho. Aunque Black y White cambien de lugar, siempre gana el mismo algoritmo (Minimax).


### Heatmap Minimax de Nocca Nocca

Finalmente hice el heatmap de rewards promedio de Nocca Nocca Minimax. Veo que ningún juego se trunca, entonces siempre gana o siempre pierde, entonces obtiene rewards 1 o -1. No tengo más ideas para extraer de este experimento.

![image](./noccanocca/heatmap%20nocca%20minimax.png)


### Alpha Beta pruning en Nocca Nocca

Armé con Claude un ejemplo de implementación de Alpha Beta Pruning. Esto es porque quería acercarme a alguna prueba de un equilibrio de Nash o equilibrio Minimax en Nocca Nocca. No estaba 100% seguro cuánto podía mejorar con Alpha-Beta. Al final, concluí que también es inviable calcular el equilibrio de esta manera. Así que no terminé implementando formas empíricas de calcular o encontrar el equilibrio en este juego 


## Khun Poker para 2 jugadores

Primero probé hacer render de jugadas del juego:

```
agent_0 K 
agent_1 J 
Agent agent_0
Action 0 - move p
agent_0 K p
agent_1 J p
Agent agent_1
Action 1 - move b
agent_0 K pb
agent_1 J pb
Agent agent_0
Action 1 - move b
agent_0 K pbb
agent_1 J pbb
Reward agent_0 = 2
Reward agent_1 = -2
```

