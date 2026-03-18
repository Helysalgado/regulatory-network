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
```

**Objetivo del programa:**

Generar una tabla que indique para cada TF:

- Nombre del TF (esta columna debe estar ordenada)
- Total de genes regulados
- Número de genes activados (efecto `+`)
- Número de genes reprimidos (efecto `-`)
- Tipo de regulador:
  - `activador` si sólo hay activaciones
  - `represor` si sólo hay represión
  - `dual` si hay ambos tipos
- Lista de genes regulados (ordenada)

Ejemplo de salida:

```txt
TF	Total genes	Activados	Reprimidos	Tipo	Genes
AraC	2	1	1	dual	araA, araB
```
  