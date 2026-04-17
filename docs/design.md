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


## Actualizacion v1.1

- Leer los datos desde un archivo
  - recorrer líneas
  - limpiar datos
  - validar
  - extraer información
  - construir interactions
generar salida a un archivo

## Actualización v1.2
El programa recibirá 2 argumentos desde la linea de comandos

Flujo:

usuario --> CLI --> main() --> funciones

## Actualización v1.3

Implementación del filtro `--min_genes`:

- Agregar el argumento `--min_genes` en el parser de argumentos CLI, con valor por defecto 0 (sin filtro).
- En la función `write_summary()`, antes de iterar sobre los TFs, filtrar el diccionario `regulon` para incluir solo aquellos TFs donde `len(regulon[tf]["genes"]) >= min_genes`.
- Mantener el resto del algoritmo sin cambios, asegurando que la salida sea consistente con el filtrado aplicado.

