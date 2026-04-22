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

## Actualización v1.4

### Estrategia de Manejo de Errores

Se adopta una estrategia de manejo de errores que prioriza la robustez y la claridad en la comunicación de problemas. Los errores se clasifican en tres categorías: errores críticos que impiden la ejecución, advertencias que permiten continuar pero notifican anomalías, y resultados vacíos que indican ausencia de datos válidos sin ser fallos fatales. Esta clasificación permite al usuario distinguir entre situaciones que requieren intervención inmediata y aquellas que son informativas.

### Diferencia entre Validación y Excepciones

La validación se refiere a la verificación preventiva de entradas y estados antes de procesar datos, enfocada en asegurar la integridad de los parámetros y registros. Las excepciones, por otro lado, manejan condiciones excepcionales durante la ejecución, como fallos de I/O o errores de sistema. La validación se realiza de manera síncrona y previene problemas, mientras que las excepciones capturan y responden a fallos inesperados, permitiendo una recuperación controlada o terminación ordenada.

### Uso de `raise` en Funciones (Contrato)

Las funciones utilizan `raise` para establecer contratos claros: si una función recibe parámetros inválidos o encuentra un estado inconsistente, lanza una excepción específica en lugar de retornar valores erróneos o silenciar el problema. Esto fuerza a los llamadores a manejar explícitamente las condiciones de error, mejorando la confiabilidad del código al evitar comportamientos indefinidos. Por ejemplo, una función de validación lanza `ValueError` para parámetros incorrectos, dejando la decisión de cómo proceder al contexto superior.

### Uso de `try/except` en `main()`

La función `main()` centraliza el manejo de excepciones mediante bloques `try/except`, actuando como punto único de captura para errores de todo el programa. Esto separa la lógica de negocio de las preocupaciones de error, permitiendo que las funciones auxiliares se concentren en su propósito sin diluirse en manejo de excepciones. Los bloques `except` específicos capturan tipos de error particulares (como `FileNotFoundError` o `PermissionError`), proporcionando mensajes informativos y salidas ordenadas, mientras que un bloque general maneja excepciones inesperadas.

### Propagación de Errores

Los errores se propagan desde las funciones de bajo nivel hacia `main()`, permitiendo que cada capa maneje solo los errores que puede resolver. Las funciones auxiliares propagan excepciones sin capturarlas, manteniendo la separación de responsabilidades y evitando el enmascaramiento de problemas. Esta propagación ascendente asegura que los errores críticos lleguen al nivel superior para una resolución adecuada, mientras que los errores recuperables se manejan localmente.

### Separación de Responsabilidades (Funciones vs main)

Las funciones auxiliares se encargan exclusivamente de la lógica de negocio y validación, delegando el manejo de excepciones a `main()`. Esto mantiene el código modular: las funciones retornan resultados válidos o lanzan excepciones claras, sin preocuparse por la presentación de errores o la interacción con el usuario. `main()` actúa como coordinador, manejando la CLI, invocando funciones y traduciendo excepciones en mensajes apropiados, asegurando que la interfaz del programa sea consistente y amigable.

## Actualización v1.5

### Uso de Conjuntos para Genes Únicos

Se modifica la estructura de datos en `build_regulon()` para utilizar conjuntos (`set`) en lugar de listas y contadores simples. Los campos `genes`, `activados` y `reprimidos` ahora son conjuntos que almacenan genes únicos, eliminando duplicados automáticamente. Esto asegura que:

- El total de genes regulados se calcula como `len(genes)`, representando genes únicos.
- Los contadores de activados y reprimidos se basan en genes únicos con cada tipo de efecto, no en interacciones repetidas.
- La lista de salida incluye genes únicos ordenados, sin repeticiones.

Esta decisión mejora la precisión del análisis al enfocarse en genes regulados únicos en lugar de contar interacciones múltiples, manteniendo la eficiencia computacional con operaciones de conjunto.

