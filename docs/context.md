## Context

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


## Actualización v1.1

1. Leer los datos desde un archivo
   1. El archivo trae 7 columnas, y la que vamos a usar son: 
2. Los resultados deberan mandarse a un archivo de salida


## Actualización v1.2
Problema:
El programa depende de rutas fijas (hardcoded)

Nuevo requisito:
El programa debe recibir 2 argumentos, el archivo de entrada y el archivo de salida

## Actualización v1.3

Problema:
La salida incluye todos los factores de transcripción (TF), independientemente del número de genes que regulan, lo que puede generar resultados extensos con TFs poco relevantes.

Nuevo requisito:
Agregar un argumento `--min_genes` que permita filtrar los resultados para incluir únicamente TFs que regulan al menos el número especificado de genes, facilitando el análisis de reguladores más activos.


