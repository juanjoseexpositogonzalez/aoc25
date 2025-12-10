# Resumen Estratégico: Advent of Code 2025 (Días 1-9)

Este documento contiene un análisis estratégico de los problemas resueltos, explicando el problema, la estrategia de solución y por qué funciona, sin incluir código.

---

## Day 1: Secret Entrance - Dial Rotation

### Problema
Un dial circular con números del 0 al 99 necesita seguir una secuencia de rotaciones (L/R + distancia). La contraseña es el número de veces que el dial apunta a 0 después de cada rotación.

### Estrategia de Resolución

**Parte 1:** Simulación directa
- Modelar el dial como un círculo usando aritmética modular (módulo 100)
- Simular cada rotación: L resta, R suma, aplicando módulo para manejar el wraparound
- Contar cuántas veces el resultado final es 0

**Parte 2:** Conteo durante el movimiento
- En lugar de solo verificar el estado final, contar cada vez que el dial pasa por 0 durante la rotación
- Para rotaciones grandes (ej: R1000), calcular cuántas veces cruza el 0 usando división entera
- Manejar casos donde la rotación cruza múltiples veces el punto 0

### Por qué Funciona
La aritmética modular es perfecta para modelar sistemas circulares. El módulo 100 garantiza que cualquier operación mantenga el valor dentro del rango válido (0-99). Para la parte 2, reconocer que una rotación grande puede cruzar el 0 múltiples veces permite calcular eficientemente sin simular cada paso individual.

---

## Day 2: Gift Shop - Invalid Product IDs

### Problema
Identificar IDs de productos inválidos en rangos dados. Un ID es inválido si está formado por una secuencia de dígitos repetida.

### Estrategia de Resolución

**Parte 1:** Patrón de repetición exacta (2 veces)
- Para cada ID en los rangos, verificar si la primera mitad es igual a la segunda mitad
- Convertir a string y comparar substrings
- Sumar todos los IDs inválidos encontrados

**Parte 2:** Patrón de repetición múltiple (2+ veces)
- Verificar todos los posibles patrones de repetición
- Para cada posible longitud de patrón (desde 1 hasta la mitad de la longitud), verificar si el ID completo está formado por repeticiones de ese patrón
- Usar divisibilidad: si la longitud total es divisible por la longitud del patrón, verificar si todas las repeticiones coinciden

### Por qué Funciona
La parte 1 es un caso especial de la parte 2. La estrategia de verificar múltiples longitudes de patrón garantiza encontrar cualquier repetición, sin importar cuántas veces se repita. La verificación de divisibilidad optimiza el proceso al evitar intentar patrones que no pueden formar el número completo.

---

## Day 3: Lobby - Battery Joltage

### Problema
Encontrar la máxima joltage posible seleccionando exactamente N baterías de cada banco, donde la joltage es el número formado por los dígitos de las baterías seleccionadas.

### Estrategia de Resolución

**Parte 1:** Selección de 2 baterías
- Para maximizar un número de 2 dígitos, seleccionar los dos dígitos más grandes disponibles
- Ordenar los dígitos y tomar los dos mayores
- Formar el número con el mayor primero

**Parte 2:** Selección de 12 baterías
- Estrategia greedy: seleccionar los dígitos más grandes disponibles
- Sin embargo, hay una restricción: debemos seleccionar exactamente 12 dígitos
- La estrategia óptima es: mantener los dígitos más grandes y eliminar los más pequeños
- Si hay muchos 1s, eliminarlos primero ya que aportan menos valor al número final

### Por qué Funciona
Para maximizar un número, queremos los dígitos más grandes en las posiciones más significativas. La estrategia greedy funciona porque cada dígito en una posición más significativa tiene más peso que cualquier dígito en posiciones menos significativas. Eliminar los dígitos más pequeños primero maximiza el valor total del número resultante.

---

## Day 4: Printing Department - Paper Roll Access

### Problema
Identificar rollos de papel accesibles por montacargas (menos de 4 rollos adyacentes) y luego calcular cuántos rollos pueden removerse iterativamente.

### Estrategia de Resolución

**Parte 1:** Conteo directo
- Para cada rollo, contar los rollos adyacentes en las 8 direcciones (incluyendo diagonales)
- Si tiene menos de 4 adyacentes, es accesible
- Contar todos los rollos accesibles

**Parte 2:** Simulación iterativa
- Proceso iterativo: identificar rollos accesibles, removerlos, recalcular accesibilidad
- Después de remover rollos, algunos que antes no eran accesibles pueden volverse accesibles
- Repetir hasta que no haya más rollos accesibles
- Contar el total de rollos removidos

### Por qué Funciona
La parte 1 es un problema de vecindad en una grilla. La parte 2 requiere simulación porque el estado del sistema cambia dinámicamente: remover un rollo puede cambiar la accesibilidad de otros rollos. Este es un problema de cascada donde cada cambio puede desencadenar más cambios. La simulación garantiza que encontremos todos los rollos que eventualmente pueden ser removidos.

---

## Day 5: Cafeteria - Ingredient Freshness

### Problema
Determinar qué IDs de ingredientes son frescos basándose en rangos de IDs frescos, y luego calcular el total de IDs frescos en todos los rangos.

### Estrategia de Resolución

**Parte 1:** Verificación de membresía en rangos
- Para cada ID disponible, verificar si está dentro de algún rango fresco
- Un ID es fresco si está en cualquier rango (los rangos pueden solaparse)
- Contar cuántos IDs disponibles son frescos

**Parte 2:** Cálculo de unión de rangos
- Calcular la unión de todos los rangos frescos
- Fusionar rangos solapados para evitar contar IDs duplicados
- Ordenar rangos por inicio, luego fusionar consecutivos que se solapan
- Calcular el total de IDs únicos en la unión de rangos

### Por qué Funciona
La parte 1 requiere verificación de membresía, que es eficiente con estructuras de datos apropiadas. La parte 2 es un problema clásico de "merge intervals": ordenar y fusionar rangos solapados es la estrategia estándar para calcular la unión de intervalos. La fusión garantiza que cada ID se cuente exactamente una vez, incluso si aparece en múltiples rangos.

---

## Day 6: Trash Compactor - Cephalopod Math

### Problema
Resolver problemas matemáticos escritos verticalmente en columnas, donde los números están apilados y las operaciones están en la parte inferior.

### Estrategia de Resolución

**Parte 1:** Lectura top-to-bottom
- Identificar columnas de problemas (separadas por columnas vacías)
- Leer cada número de arriba hacia abajo dentro de cada columna
- Aplicar la operación indicada (suma o multiplicación)
- Sumar todos los resultados

**Parte 2:** Lectura bottom-to-top (dígitos significativos invertidos)
- Leer cada número de abajo hacia arriba (dígito menos significativo primero)
- Esto invierte el orden de los dígitos: el número se forma leyendo de derecha a izquierda
- Aplicar las operaciones normalmente
- Sumar todos los resultados

### Por qué Funciona
La parte 1 es parsing directo de texto estructurado. La parte 2 introduce una variación en cómo se interpretan los números: leer de abajo hacia arriba efectivamente invierte el orden de los dígitos. Esto requiere reconstruir el número correctamente considerando que el dígito en la parte inferior es el menos significativo. La estrategia es similar pero con una transformación en la interpretación de los datos.

---

## Day 7: Laboratories - Tachyon Beam Splitting

### Problema
Simular un haz de taquiones que se divide cuando encuentra un divisor, contando divisiones o timelines resultantes.

### Estrategia de Resolución

**Parte 1:** Simulación de haz clásico
- Simular el haz moviéndose hacia abajo desde S
- Cuando encuentra un divisor (^), el haz se detiene y se crean dos nuevos haces (izquierda y derecha)
- Usar una cola o conjunto para rastrear todos los haces activos
- Contar cada vez que un haz encuentra un divisor (cada división)

**Parte 2:** Interpretación de muchos mundos (quantum)
- Un solo partícula toma ambos caminos en cada divisor
- Cada vez que encuentra un divisor, se duplica el número de timelines
- Usar programación dinámica o memoización para evitar recalcular paths
- Contar todos los timelines únicos al final del manifold

### Por qué Funciona
La parte 1 es una simulación de propagación donde cada división crea nuevos estados. La parte 2 es exponencial: cada divisor duplica las posibilidades. La clave es reconocer que no necesitamos simular cada timeline individualmente, sino contar cuántos paths únicos existen. Esto puede optimizarse usando memoización para evitar recalcular subproblemas idénticos.

---

## Day 8: Playground - Junction Box Circuits

### Problema
Conectar cajas de unión eléctricas en 3D para formar circuitos, encontrando las conexiones más cortas y calculando propiedades de los circuitos resultantes.

### Estrategia de Resolución

**Parte 1:** Algoritmo de Kruskal modificado
- Calcular todas las distancias entre pares de cajas (distancia euclidiana 3D)
- Ordenar conexiones por distancia
- Conectar las N conexiones más cortas que no formen ciclos
- Usar Union-Find para rastrear qué cajas están en el mismo circuito
- Después de N conexiones, calcular los tamaños de los circuitos y multiplicar los 3 más grandes

**Parte 2:** Minimum Spanning Tree completo
- Continuar conectando hasta que todas las cajas estén en un solo circuito
- Esto es esencialmente construir un MST completo
- Encontrar la última conexión necesaria para completar el MST
- Multiplicar las coordenadas X de las dos últimas cajas conectadas

### Por qué Funciona
Este es un problema clásico de teoría de grafos. La parte 1 es similar a construir un MST parcial, donde queremos las N conexiones más cortas. Union-Find es perfecto para rastrear componentes conectados eficientemente. La parte 2 es construir un MST completo usando el algoritmo de Kruskal, que garantiza el árbol de expansión mínimo conectando todos los nodos con el costo total mínimo.

---

## Day 9: Movie Theater - Rectangle Finding

### Problema
Encontrar el rectángulo más grande usando dos tiles rojos como esquinas opuestas, primero sin restricciones y luego solo usando tiles rojos o verdes.

### Estrategia de Resolución

**Parte 1:** Búsqueda exhaustiva optimizada
- Generar todos los pares de puntos rojos que pueden formar esquinas opuestas (diferentes x e y)
- Para cada par, calcular el área del rectángulo
- Encontrar el área máxima

**Parte 2:** Validación con polígono
- Los tiles rojos forman un polígono cuando se conectan en orden
- Los tiles verdes son el borde del polígono (líneas entre rojos consecutivos) más el interior
- Usar flood fill inverso para identificar el exterior, luego las tiles válidas son el complemento
- Precalcular rangos válidos por fila para verificación rápida
- Para cada rectángulo candidato, verificar que todas sus filas estén completamente dentro del polígono
- Ordenar candidatos por área descendente para early exit

### Por qué Funciona
La parte 1 es una búsqueda directa. La parte 2 requiere geometría computacional: determinar si un rectángulo está completamente dentro de un polígono. El flood fill inverso es eficiente para identificar el interior/exterior. Precalcular rangos por fila permite verificación O(1) por fila en lugar de verificar cada celda individualmente. El ordenamiento descendente permite early exit cuando encontramos el máximo.

---

## Predicción: Day 10

Basándome en los patrones observados en los días anteriores, aquí están mis predicciones para el día 10:

### Patrones Observados

1. **Progresión de complejidad:** Los problemas aumentan gradualmente en complejidad
2. **Temas relacionados:** Cada día continúa la narrativa del día anterior
3. **Parte 2 como extensión:** La parte 2 generalmente extiende o modifica la parte 1
4. **Estructuras de datos:** Se han usado grids, grafos, geometría, y estructuras lineales

### Predicción del Día 10

**Contexto narrativo:** Después del teatro de cine (día 9), probablemente avanzamos a otra área del Polo Norte. Posibles ubicaciones: sala de control, almacén, o área de producción.

**Tipo de problema probable:**

1. **Problema de optimización con restricciones:**
   - Similar al día 9 pero con restricciones adicionales
   - Podría involucrar encontrar patrones o secuencias óptimas
   - Posiblemente relacionado con scheduling o asignación de recursos

2. **Problema de búsqueda en espacio de estados:**
   - BFS/DFS más complejo que el día 7
   - Podría involucrar múltiples agentes o estados simultáneos
   - Posiblemente con restricciones temporales o de recursos

3. **Problema de parsing/interpretación más complejo:**
   - Similar al día 6 pero con reglas más complejas
   - Podría involucrar evaluación de expresiones o lenguajes simples
   - Posiblemente con precedencia de operadores o reglas contextuales

4. **Problema de geometría 2D/3D:**
   - Extensión del día 9 con geometría más compleja
   - Podría involucrar polígonos, intersecciones, o áreas
   - Posiblemente con transformaciones o rotaciones

### Estrategia Recomendada para el Día 10

1. **Leer cuidadosamente el problema:** Los problemas de AoC suelen tener detalles importantes en la descripción
2. **Identificar la estructura de datos principal:** ¿Es un grid? ¿Un grafo? ¿Una secuencia?
3. **Empezar con una solución simple:** Implementar primero la parte 1 de forma directa
4. **Optimizar para la parte 2:** La parte 2 generalmente requiere optimización o cambio de enfoque
5. **Considerar casos edge:** Los problemas de AoC suelen tener casos especiales

### Posibles Temas Específicos

- **Scheduling/Planning:** Asignar tareas o recursos con restricciones
- **Pathfinding avanzado:** Encontrar rutas óptimas con múltiples objetivos
- **Pattern matching:** Encontrar patrones complejos en datos
- **Simulación de sistemas:** Modelar un sistema físico o lógico con reglas complejas

---

## Conclusión

Los primeros 9 días han cubierto una amplia gama de técnicas algorítmicas:
- Aritmética modular (Día 1)
- Pattern matching (Día 2)
- Greedy algorithms (Día 3)
- Grid simulation (Día 4)
- Interval merging (Día 5)
- Parsing complejo (Día 6)
- Graph traversal (Día 7)
- Minimum Spanning Tree (Día 8)
- Geometría computacional (Día 9)

El día 10 probablemente combinará varias de estas técnicas o introducirá nuevos conceptos como programación dinámica, backtracking, o algoritmos de optimización más avanzados.

