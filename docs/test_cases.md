
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
