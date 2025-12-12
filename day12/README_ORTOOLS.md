# Solución con OR-Tools CP-SAT

Esta es una versión optimizada del solver que utiliza **OR-Tools CP-SAT**, un solver de constraint programming altamente optimizado desarrollado por Google.

## 🚀 Instalación

```bash
# Opción 1: Usar el script de instalación
./install_ortools.sh

# Opción 2: Instalación manual
pip install ortools
```

## 📊 Ventajas de OR-Tools CP-SAT

1. **Alto rendimiento**: Utiliza técnicas avanzadas de constraint propagation y conflict-driven learning
2. **Optimizado en C++**: El núcleo está escrito en C++ para máximo rendimiento
3. **Paralelización**: Soporta múltiples workers para resolver problemas más rápido
4. **Heurísticas avanzadas**: Incluye muchas heurísticas y técnicas de optimización

## 🎯 Uso

```bash
# Ejecutar con OR-Tools
python3 main_ortools.py

# Comparar con la versión original
python3 main.py
```

## ⚙️ Configuración

Puedes ajustar el timeout por región en `main_ortools.py`:

```python
TIMEOUT_PER_REGION: Final[float] = 30.0  # segundos
```

## 📈 Comparación de Rendimiento

OR-Tools debería ser significativamente más rápido que el backtracking manual, especialmente para:
- Regiones grandes (40x40 o más)
- Problemas con muchas formas
- Casos donde el espacio de búsqueda es grande

## 🔧 Solución de Problemas

Si encuentras errores:

1. **OR-Tools no está instalado**: Ejecuta `pip install ortools`
2. **Errores de importación**: Asegúrate de tener Python 3.7+
3. **Timeout**: Aumenta `TIMEOUT_PER_REGION` si las regiones son muy complejas

## 📝 Notas

- OR-Tools es especialmente efectivo para problemas de constraint satisfaction
- El solver puede encontrar soluciones mucho más rápido que backtracking manual
- Para problemas muy simples, la diferencia puede no ser tan notable

