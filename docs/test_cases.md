
# Casos de prueba

## Caso 1

Entrada:

```txt
AraC araA +
AraC araB -
```

Salida esperada:

```txt
TF	Total genes	Activados	Reprimidos	Tipo	Genes
AraC	2	1	1	dual	araA, araB
```



## Básico

### Archivo válido (caso feliz)

**Condición**
El archivo existe y tiene el formato esperado.

**Resultado esperado**

* Se procesa sin errores
* Se construye correctamente `interactions`
* Se genera archivo de salida

---

### Líneas de comentario

**Condición**
El archivo contiene líneas que comienzan con `#`.

**Resultado esperado**

* Se ignoran completamente
* No generan errores

---

### Encabezado presente

**Condición**
El archivo contiene encabezado.

**Resultado esperado**

* No se incluye en `interactions`

---

### Líneas vacías

**Condición**
Existen líneas vacías en el archivo.

**Resultado esperado**

* Se ignoran
* No afectan la ejecución

---

### Valor inválido en effect

**Condición**
El campo `effect` no es `+` ni `-`.

**Resultado esperado**

* La fila se descarta
* El programa continúa

---

## Intermedio

### Columnas insuficientes

**Condición**
La línea tiene menos columnas de las necesarias.

**Resultado esperado**

* Se ignora la línea
* No ocurre `IndexError`

---

### Archivo no existe

**Condición**
Ruta incorrecta.

**Resultado esperado**

* Mensaje claro de error
* Terminación controlada

---

### Sin permisos de lectura

**Condición**
Archivo sin permisos.

**Resultado esperado**

* Mensaje de error claro
* Terminación controlada

---

### Integración con programa previo

**Condición**
`interactions` generado correctamente.

**Resultado esperado**

* El programa previo funciona sin cambios
* Se obtienen métricas correctas del regulón

---

## Avanzado

### Archivo de salida generado

**Condición**
Ejecución exitosa.

**Resultado esperado**

* Archivo de salida creado
* Formato correcto

---

### Interacciones duplicadas

**Condición**
Existen filas duplicadas.

**Resultado esperado**

* Comportamiento consistente (definido por diseño)

---

### Columnas en distinto orden

**Condición**
Las columnas cambian de posición.

**Resultado esperado**

* Falla si depende de índices
* Funciona si usa nombres de columnas


## Command Line Interface (CLI)
Caso: Correr el programa con paso de argumentos

Entrada:

```bash
uv run python regulon_summary.py input.txt output.txt
uv run python regulon_summary.py NetworkRegulatorGene.tsv  tf_summary.txt
```

Resultado:
El programa lea el archivo de entrada y genere el resultado con el nombre que se le paso como argumento.

## Actualización v1.3

### Filtro por número mínimo de genes

**Condición**
Ejecutar el programa con `--min_genes 2` y datos que incluyen TFs con 1 y 2+ genes regulados.

**Entrada de ejemplo:**

```txt
AraC araA +
LexA recA -
LexA recB -
```

**Comando:**

```bash
python regulon_summary.py --min_genes 2 input.tsv output.tsv
```

**Resultado esperado**

- Solo se incluyen TFs con al menos 2 genes en la salida.
- En el ejemplo, `AraC` (1 gen) se excluye, `LexA` (2 genes) se incluye.
- Salida filtrada correcta en formato TSV.

## Actualización v1.4

### Archivo de entrada inexistente

**Descripción**  
El archivo de entrada especificado no existe en el sistema de archivos.

**Entrada**  
Comando: `python main.py nonexistent_file.txt output.txt`  
Archivo: nonexistent_file.txt (no existe)

**Comportamiento esperado**  
El programa termina con código de error, mostrando un mensaje claro indicando que el archivo de entrada no se encuentra.

---

### Sin permisos de lectura

**Descripción**  
El archivo de entrada existe pero no tiene permisos de lectura para el usuario.

**Entrada**  
Comando: `python main.py protected_file.txt output.txt`  
Archivo: protected_file.txt (sin permisos de lectura)

**Comportamiento esperado**  
El programa termina con código de error, mostrando un mensaje indicando falta de permisos para leer el archivo.

---

### Error en escritura (permiso o directorio)

**Descripción**  
No se puede escribir en el archivo de salida debido a permisos insuficientes o directorio inexistente.

**Entrada**  
Comando: `python main.py input.txt /protected/output.txt`  
Archivo de entrada: válido  
Directorio de salida: sin permisos de escritura

**Comportamiento esperado**  
El programa termina con código de error, mostrando un mensaje indicando que no se puede escribir en el archivo de salida.

---

### `--min_genes` negativo

**Descripción**  
El parámetro `--min_genes` recibe un valor negativo.

**Entrada**  
Comando: `python main.py input.txt output.txt --min_genes -1`  
Archivo de entrada: válido

**Comportamiento esperado**  
El programa termina con código de error, mostrando un mensaje indicando que `--min_genes` debe ser un número positivo o cero.

---

### Archivo válido pero sin interacciones

**Descripción**  
El archivo de entrada existe y tiene formato correcto, pero no contiene interacciones válidas (solo encabezados o líneas vacías).

**Entrada**  
Archivo input.txt:  
```txt
TF	gene	effect
```

Comando: `python main.py input.txt output.txt`

**Comportamiento esperado**  
El programa procesa sin errores, genera un archivo de salida vacío o con encabezado, y muestra una advertencia indicando que no se encontraron interacciones válidas.

---

### Filtro que deja el regulon vacío

**Descripción**  
El filtro `--min_genes` es mayor que el número máximo de genes regulados por cualquier TF, dejando el resultado vacío.

**Entrada**  
Archivo input.txt con datos válidos pero pocos genes por TF.  
Comando: `python main.py input.txt output.txt --min_genes 10` (valor alto)

**Comportamiento esperado**  
El programa procesa sin errores, genera un archivo de salida vacío o con solo encabezado, y muestra una advertencia indicando que ningún TF cumple el criterio de filtro.

## Actualización v1.5

### Genes duplicados en interacciones

**Descripción**  
El archivo contiene múltiples interacciones para el mismo gen con el mismo TF, lo que antes causaba duplicados en la lista de genes y totales inflados.

**Entrada**  
Archivo input.txt:  
```txt
TF	gene	effect
AraC	araA	+
AraC	araA	+
AraC	araB	-
```

Comando: `python main.py input.txt output.txt`

**Comportamiento esperado**  
El programa procesa las interacciones, elimina duplicados de genes, genera salida con genes únicos (araA, araB), total de genes = 2, activados = 1, reprimidos = 1, tipo = dual, y lista sin duplicados.

---

### Registros inválidos en el archivo

**Descripción**  
El archivo contiene registros con formato incorrecto (columnas insuficientes, valores inválidos).

**Entrada**  
Archivo input.txt:  
```txt
TF	gene	effect
AraC	araA	+
invalid_line
AraC	araB	-
```

Comando: `python main.py input.txt output.txt`

**Comportamiento esperado**  
El programa procesa las líneas válidas, descarta las inválidas, genera salida con los datos correctos, y muestra advertencias para los registros descartados.



