# Context

Este proyecto analiza una red de regulación genética.

Los datos contienen interacciones entre factores de transcripción (TF) y genes.

Formato de los datos:

TF gene effect

Ejemplo:

```txt
AraC araA + 
AraC araB - 
LexA recA -
````

**Objetivo del programa:**

Generar una tabla que indique para cada TF:

- Nombre del TF (esta columna debe estar ordenada)
- total de genes regulados
- lista de genes regulado (ordenada) 
  
  