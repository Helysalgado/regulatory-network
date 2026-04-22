
-----
## context.md

Quiero actualizar la documentación del proyecto `regulon_summary`.

Ya existen estas secciones en `context.md`:
- Context
- Actualización v1.1
- Actualización v1.2
- Actualización v1.3

Con base en los cambios recientes del código (validaciones, manejo de errores, uso de try/except, distinción entre error/advertencia/resultado vacío), necesito que agregues una nueva sección:

## Actualización v1.4

Requisitos:
- Mantén el mismo estilo de redacción que las versiones anteriores
- Usa el formato:
  Problema:
  Nuevo requisito:
- No modifiques las versiones previas
- No inventes funcionalidades que no estén en el código actual

Toma en cuenta que ahora el programa:
- valida `--min_genes`
- maneja errores de lectura (archivo inexistente, permisos, etc.)
- maneja errores de escritura
- distingue entre error, advertencia y resultado vacío
- descarta registros inválidos
- evita duplicados
- centraliza el manejo de excepciones en `main()`

Agregalo al final en `context.md`, sin modificar el texto ya descrito.


----

Ahora quiero actualizar `design.md` con base en los cambios recientes del proyecto.

Agrega una nueva sección que describa:

- Estrategia de manejo de errores
- Diferencia entre validación y excepciones
- Uso de `raise` en funciones (contrato)
- Uso de `try/except` en `main()`
- Propagación de errores
- Separación de responsabilidades (funciones vs main)

Requisitos:
- No repitas el código completo
- Explica decisiones de diseño, no implementación línea por línea
- Usa lenguaje claro y técnico
- Mantén consistencia con el resto del documento


Agregalo al final en `design.md`, formato markdown, sin modificar el texto ya descrito.


----

Quiero actualizar `test_cases.md` con base en los cambios recientes del programa.

Agrega nuevos casos de prueba para:

1. Archivo de entrada inexistente
2. Sin permisos de lectura
3. Error en escritura (permiso o directorio)
4. `--min_genes` negativo
5. Archivo válido pero sin interacciones
6. Filtro que deja el regulon vacío
7. Registros inválidos en el archivo

Para cada caso incluye:
- Descripción
- Entrada
- Comportamiento esperado

No modifiques los casos existentes.
Agregalo al final, en formato markdown



