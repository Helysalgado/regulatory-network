## Algoritmo

- Estructura principal: diccionario `regulon` con clave=TF y valor un diccionario con campos:
  - `genes`: lista de genes regulados
  - `activados`: contador de interacciones con efecto `+`
  - `reprimidos`: contador de interacciones con efecto `-`

- Recorrer todas las interacciones (una por línea):
  - Obtener el TF, el gene y el efecto
  - Si el TF no existe en `regulon`, inicializar su estructura
  - Agregar el gen a la lista `genes`
  - Incrementar `activados` o `reprimidos` según el efecto

- Recorrer los TF ordenados:
  - Ordenar la lista de genes del TF
  - Calcular el total de genes regulados
  - Determinar el tipo de regulador:
    - `dual` si hay activaciones y represiones
    - `activador` si sólo hay activaciones
    - `represor` si sólo hay represiones
  - Imprimir: TF, total, activados, reprimidos, tipo, lista de genes
