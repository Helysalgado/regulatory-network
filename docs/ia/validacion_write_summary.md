# Justificación de Validaciones en `write_summary()`

## Principio Fundamental: Fail-Fast

El objetivo es **detectar errores lo más temprano posible** (en validación de entrada) en lugar de fallar silenciosamente o después (durante ejecución). Esto asegura:

- **Integridad**: El archivo TSV nunca será parcialmente escrito o corrupto
- **Debugging rápido**: Mensajes de error claros en la validación de entrada
- **Prevención > Reacción**: Una validación costosa una vez es mejor que debuggear un TSV corrupto

---

## Fase 0: Validación de Parámetros (ANTES DE TODO)

Estas validaciones se hacen INMEDIATAMENTE al entrar en `write_summary()`. Si fallan, no se procesa nada.

### 1. `regulon is not None`
- **Por qué es importante**: Detectar llamadas accidentales con `None` en lugar de un diccionario
- **Riesgo si falta**: 
  - `TypeError: 'NoneType' object is not iterable` cuando intenta hacer `for TF in regulon:`
  - Stack trace confuso que no señala el real problema de entrada
  - Archivo posiblemente creado con solo encabezado (falso positivo)
- **Excepción**: `ValueError("regulon no puede ser None")`
- **Debugging**: El error está lo más cerca posible de donde se LLAMÓ la función incorrectamente

### 2. `isinstance(regulon, dict)`
- **Por qué es importante**: Garantizar que tiene la estructura esperada (diccionario con pares TF:datos)
- **Riesgo si falta**: 
  - Si `regulon` es una lista o string, `for TF in regulon:` iteraría sobre elementos incorrectos
  - Con string: iteraría sobre caracteres en lugar de TFs
  - Escribiría datos completamente inválidos en el TSV
- **Excepción**: `TypeError("regulon debe ser un diccionario")`
- **Ejemplo de error si falta**:
  ```python
  # Si alguien pasa regulon = "hola"
  for TF in regulon:  # Itera: "h", "o", "l", "a"
      # Intenta acceder regulon["h"]["genes"]  → Error KeyError, muy confuso
  ```

### 3. `len(regulon) > 0` (regulon no está vacío)
- **Por qué es importante**: Detectar si el pipeline anterior falló (load_interactions, build_regulon, filtrado)
- **Riesgo si falta**:
  - Crea archivo TSV con solo encabezado (0 datos)
  - Código sigue como si fuera exitoso "sin errores"
  - Downstream procesos asumen datos y fallan más tarde (difícil de debuggear)
  - False positives: "el script corrió bien pero no hay datos" (confusión)
- **Excepción**: `ValueError("regulon está vacío - revisar load_interactions() o filtrado min_genes")`
- **Ventaja**: Deja claro EN DONDE falla el problema (fase anterior)

### 4. `output_file is not None` y `isinstance(output_file, str)`
- **Por qué es importante**: Evitar usar rutas inválidas (None, números, etc.)
- **Riesgo si falta**:
  - `os.path.dirname(None)` → `TypeError: expected str, bytes or os.PathLike object`
  - `open(None, ...)` → Error sin sentido
  - Archivo creado con nombre literal `"None"` en el directorio actual
- **Excepción**: `ValueError/TypeError correspondiente`

### 5. `len(output_file.strip()) > 0` (ruta no es vacía ni espacios)
- **Por qué es importante**: Rechazar caminos vacíos o cadenas solo de espacios
- **Riesgo si falta**:
  - Si `output_file = ""`, `os.path.dirname("")` retorna `""`
  - `os.makedirs("", exist_ok=True)` intenta crear directorio actual (sin error)
  - `open("", "w")` → error ambiguo: `FileNotFoundError: [Errno 2] No such file or directory: ''`
- **Excepción**: `ValueError("output_file no puede estar vacío")`

---

## Fase 1: Validación de Estructura Interna (dentro del loop)

Estas validaciones ocurren para CADA TF en el regulon. Se verifican que los datos tengan la estructura esperada.

### 6. `TF` es string no vacío
- **Por qué es importante**: Las claves deben ser nombres válidos de factores de transcripción
- **Riesgo si falta**:
  - Si TF = None, se escribe literal `"None"` en el TSV
  - Si TF = 123 (número), se escribe `"123"` (confuso con datos de genes)
  - Imposible de distinguir en análisis downstream
- **Acción**: **Advertencia + Filtrar** (no es error fatal)
- **Ejemplo**:
  ```
  ⚠️ TF inválido (None o vacío): saltando...
  ⚠️ TF inválido (tipo 123): saltando...
  ```

### 7. `regulon[TF]` es diccionario
- **Por qué es importante**: Garantizar estructura consistente ({TF: {genes: [...], activados: N, reprimidos: M}})
- **Riesgo si falta**:
  - Si `regulon[TF] = [...]` (lista en lugar de dict), `regulon[TF]["genes"]` → `TypeError`
  - Archivo parcialmente escrito antes del crash
- **Excepción**: `TypeError(f"regulon[{TF}] debe ser diccionario, recibido {type(...)}")`

### 8. Presencia de claves: `"genes"`, `"activados"`, `"reprimidos"`
- **Por qué es importante**: Detectar cambios en estructura desde `build_regulon()` o corrupción de datos
- **Riesgo si falta**:
  - `regulon[TF]["genes"]` → `KeyError` (sin especificar qué clave falta)
  - Archivo parcialmente escrito
  - Difícil debuggear qué salió mal
- **Excepción**: 
  ```python
  raise KeyError(
      f"TF '{TF}': clave faltante. Esperado: "
      "'genes', 'activados', 'reprimidos'. "
      f"Recibido: {list(regulon[TF].keys())}"
  )
  ```
- **Ventaja**: Mensaje descriptivo que señala exactamente qué está mal

### 9. `regulon[TF]["genes"]` es lista
- **Por qué es importante**: Garantizar que `sorted()` y `", ".join()` funcionarán correctamente
- **Riesgo si falta**:
  - Si genes = "gene1,gene2" (string), `sorted(string)` devuelve lista de caracteres
  - Si genes = None, `sorted(None)` → `TypeError: 'NoneType' object is not iterable`
  - TSV contiene datos errados
- **Excepción**: `TypeError(f"regulon[{TF}]['genes'] debe ser lista, recibido {type(...)}")`

### 10. `"activados"` y `"reprimidos"` son int ≥ 0
- **Por qué es importante**: Campos de conteo deben ser numéricos, no negativos (no puede haber -5 activaciones)
- **Riesgo si falta**:
  - Si `activados = "5"` (string), formatea correctamente pero es inconsistente con tipo esperado
  - Si `activados = -3`, escribir valor negativo sin sentido biológico
  - Si `activados = 1.5`, problemas de redondeo y formato
- **Excepción**: `ValueError(f"'{TF}': 'activados' debe ser int ≥ 0, recibido {activados}")`

### 11. Cada gen en genes es string no vacío
- **Por qué es importante**: Evitar escribir "None", números o strings vacíos en el TSV
- **Riesgo si falta**:
  - Genes = ["geneA", None, "geneB"] → Escribe "geneA, None, geneB" (inválido)
  - Genes = ["geneA", "", "geneB"] → Escribe "geneA, , geneB" (ambiguo)
  - Imposible de parsear o analizar después
- **Acción**: **Filtrar** genes inválidos + advertencia
  ```python
  genes_validos = [g for g in genes if isinstance(g, str) and len(g.strip()) > 0]
  if len(genes_validos) < len(genes):
      print(f"⚠️ {TF}: {len(genes) - len(genes_validos)} genes inválidos filtrados")
  genes = genes_validos
  ```

---

## Fase 2: Validación de Consistencia

Estas validaciones verifican que los datos sean **lógicamente consistentes** entre sí.

### 12. `total_genes == len(genes)` (coherencia interna)
- **Por qué es importante**: El total debe coincidir con la cantidad actual de genes
- **Riesgo si falta**:
  - `total_genes = 5` pero `genes = ["a", "b"]` (2 elementos)
  - Escribe datos contradictores: "TF   5   2   1   ..." (inconsistencia matemática)
  - Impossibilita análisis downstream
- **Acción**: **Advertencia + Usar len(genes) como fuente de verdad**
  ```python
  if total != len(genes):
      print(f"⚠️ {TF}: inconsistencia - total={total}, len(genes)={len(genes)}")
      # Usar len(genes) como valor correcto
  ```

### 13. `activados + reprimidos ≤ total`
- **Por qué es importante**: Validar lógica biológica (la suma de genes activados+reprimidos no puede exceder el total)
- **Riesgo si falta**:
  - Datos ilógicos: TF tiene 5 genes totales, pero 4 activados + 3 reprimidos = 7 (¡más del total!)
  - Sugiere error en `build_regulon()` (contar un gen dos veces)
  - Análisis biológico incorrecto downstream
- **Acción**: **Advertencia** (alerta que hay error en etapa anterior)
  ```python
  if activados + reprimidos > total:
      print(f"⚠️ {TF}: activados({activados}) + reprimidos({reprimidos}) > total({total})")
      print(f"   Revisar build_regulon() - posible gen contado múltiples veces")
  ```

---

## Fase 3: Ejecución con Manejo de Errores I/O

Solo después de que TODAS las validaciones anteriores pasen, se ejecuta I/O.

### 14. Try-catch en `os.makedirs()`
- **Por qué es importante**: El directorio padre podría no existir o no tener permisos
- **Manejo**:
  ```python
  try:
      os.makedirs(os.path.dirname(output_file), exist_ok=True)
  except PermissionError:
      raise RuntimeError(f"Permisos insuficientes para crear directorio: {os.path.dirname(output_file)}")
  except OSError as e:
      raise RuntimeError(f"Error al crear directorio: {e}")
  ```

### 15. Try-catch en `open()` y escritura
- **Por qué es importante**: El archivo podría estar bloqueado, ruta inválida o permisos insuficientes
- **Manejo**:
  ```python
  try:
      with open(output_file, "w") as out:
          # escribir datos
  except PermissionError:
      raise RuntimeError(f"Permisos insuficientes para escribir: {output_file}")
  except IOError as e:
      raise RuntimeError(f"Error de I/O al escribir archivo: {e}")
  except OSError as e:
      raise RuntimeError(f"Error del sistema al escribir: {e}")
  ```

---

## Resumen: ¿Por qué este orden?

| Fase | Qué valida | Costo | Beneficio |
|------|-----------|-------|----------|
| **Fase 0** | Parámetros entrada | Muy rápido (~1ms) | Detecta errores en código que LLAMA a función |
| **Fase 1** | Estructura datos | Rápido (loop simple) | Detecta corrupción desde etapas anteriores |
| **Fase 2** | Consistencia lógica | Muy rápido | Detecta bugs en `build_regulon()` |
| **Fase 3** | I/O | Más lento | Solo se ejecuta si todo arriba pasó |

**Ventaja**: Si hay error, se detecta y reporta EN LA UBICACIÓN CORRECTA del problema.

---

## Ejemplo: Beneficio de este enfoque

### Escenario sin validaciones:
```
$ python regulon_summary.py data.tsv results/summary.tsv --min_genes 10
# ... Código procesa y abre archivo...
# ... Escribe 50 líneas...
Traceback (most recent call last):
  File "write_summary.py", line 143
    TypeError: cannot unpack non-sequence
    # ¿Qué secuencia? ¿Dónde? 😞
```

### Escenario CON validaciones (Fase 0):
```
$ python regulon_summary.py data.tsv results/summary.tsv --min_genes 10
Traceback (most recent call last):
  File "write_summary.py", line 10
    raise ValueError("regulon está vacío - revisar load_interactions() o filtrado")
ValueError: regulon está vacío - revisar load_interactions() o filtrado
# ¡Claro! El problema está en min_genes=10 → data.tsv tiene pocos genes/TF ✓
```

El archivo TSV NUNCA fue creado/corrupto. El error es obvio y actionable.

---

## Conclusión

Las validaciones **prioritarias** antes de I/O aseguran:
1. **Integridad**: TSV nunca corrupto
2. **Debugging rápido**: Errores claros y cerca de raíz
3. **Confiabilidad**: Garantía de que si éxito → datos válidos
