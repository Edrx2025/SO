# Simulador del Sistema Operativo - Estructura Modular

Este documento explica la estructura modular del simulador del sistema operativo, diseñada para facilitar la explicación en exposiciones.

## Estructura de Módulos

### 📦 `constantes.py`
**Propósito**: Contiene todas las constantes, colores y configuraciones del simulador.

**Contenido**:
- Constantes de memoria (MEMORIA_DEFAULT, BLOQUE_MEMORIA)
- Paleta de colores del tema oscuro futurista
- Función `get_color_proceso()` para asignar colores únicos a procesos

---

### ⚙️ `modulo_cpu.py` - Módulo de CPU
**Propósito**: Gestiona la unidad de tiempo (tick) y la ejecución de procesos.

**Clase Principal**: `CPU`

**Funcionalidades**:
- `ejecutar_tick()`: Ejecuta un tick (unidad de tiempo) del proceso actual
  - Reduce el tiempo de ejecución restante
  - Maneja diferentes algoritmos de planificación
  - Detecta terminación de procesos
  - Maneja agotamiento de quantum (Round Robin)
  - Maneja bloqueos por I/O
- `obtener_tick_count()`: Retorna el número de ticks ejecutados
- `reset()`: Resetea el contador de ticks

**Uso en la exposición**: Explicar cómo la CPU ejecuta instrucciones en unidades de tiempo discretas (ticks).

---

### 🔄 `modulo_procesos.py` - Módulo de Procesos
**Propósito**: Gestiona la creación de procesos, colas de procesos y sus transiciones de estado.

**Clases Principales**:
- `PCB` (Process Control Block): Representa un proceso con toda su información
- `GestorProcesos`: Gestiona las colas de procesos

**Funcionalidades**:
- `crear_proceso()`: Crea un nuevo proceso y lo agrega a la cola de nuevos
- `agregar_a_listos()`: Agrega proceso a cola de listos (si hay memoria disponible)
- `agregar_a_terminados()`: Agrega proceso a cola de terminados
- `sacar_de_listos()`: Saca proceso de la cola de listos
- `agregar_a_bloqueados()`: Agrega proceso a cola de bloqueados (I/O)
- `retornar_de_bloqueados()`: Retorna proceso de bloqueados a listos
- `obtener_todos_procesos()`: Obtiene todos los procesos activos

**Estados de Proceso**:
- NUEVO: Proceso recién creado
- LISTO: Proceso listo para ejecutarse (en memoria)
- EJECUCION: Proceso ejecutándose en CPU
- BLOQUEADO: Proceso esperando I/O
- TERMINADO: Proceso que ha finalizado

**Uso en la exposición**: Explicar el ciclo de vida de un proceso y las diferentes colas.

---

### 🧠 `modulo_memoria.py` - Módulo de Memoria
**Propósito**: Contiene los algoritmos de asignación de memoria, búsqueda de memoria disponible, asignación y liberación.

**Clase Principal**: `GestorMemoria`

**Funcionalidades**:
- `buscar_memoria_disponible()`: Busca bloques libres que puedan alojar un proceso
- `asignar_memoria()`: Asigna memoria a un proceso según la estrategia:
  - **First Fit**: Primer bloque que cumpla con el tamaño
  - **Best Fit**: Bloque más pequeño que cumpla con el tamaño
  - **Worst Fit**: Bloque más grande disponible
- `liberar_memoria()`: Libera memoria cuando un proceso termina
- `compactar_memoria()`: Une bloques libres adyacentes
- `reiniciar_memoria()`: Reinicia la memoria con un nuevo tamaño

**Estructura de Memoria**:
- Mapa de memoria con bloques que tienen: inicio, tamaño, estado (LIBRE/OCUPADO), PID

**Uso en la exposición**: Explicar cómo se gestiona la memoria, los diferentes algoritmos de asignación y la fragmentación.

---

### 📋 `modulo_planificador.py` - Módulo del Planificador
**Propósito**: Selecciona el próximo proceso a ejecutarse según la política de planificación.

**Clase Principal**: `Planificador`

**Funcionalidades**:
- `seleccionar_proximo_proceso()`: Selecciona el próximo proceso según el algoritmo:
  - **Round Robin**: FIFO con quantum
  - **FCFS** (First Come First Served): FIFO simple
  - **SJF** (Shortest Job First): Ordena por tiempo de ejecución restante
  - **Prioridad**: Ordena por prioridad (menor número = mayor prioridad)
- `ordenar_cola_listos()`: Ordena la cola según el algoritmo
- `registrar_gantt()`: Registra ejecución en el gráfico de Gantt
- `limpiar_gantt()`: Limpia el historial de Gantt
- Gestión de quantum para Round Robin

**Uso en la exposición**: Explicar los diferentes algoritmos de planificación y cómo seleccionan procesos.

---

### 🚀 `modulo_despachador.py` - Módulo del Despachador
**Propósito**: Da el control de la CPU al proceso seleccionado por el planificador.

**Clase Principal**: `Despachador`

**Funcionalidades**:
- `despachar_proceso()`: Asigna CPU a un proceso
  - Cambia estado a "EJECUCION"
  - Remueve de cola de listos
  - Marca como proceso actual
- `liberar_cpu()`: Libera la CPU del proceso actual
  - Cambia estado del proceso
  - Lo devuelve a la cola correspondiente

**Uso en la exposición**: Explicar el cambio de contexto (context switch) y cómo se transfiere el control de CPU.

---

### 🎯 `coordinador.py` - Coordinador del Sistema
**Propósito**: Integra todos los módulos y coordina su funcionamiento.

**Clase Principal**: `CoordinadorSO`

**Funcionalidades**:
- `ejecutar_ciclo()`: Ejecuta un ciclo completo del sistema operativo:
  1. Carga procesos nuevos a memoria
  2. Maneja retorno de I/O
  3. Ejecuta tick en CPU
  4. Despacha próximo proceso
- `agregar_proceso()`: Crea y agrega un nuevo proceso
- `terminar_proceso()`: Termina un proceso (libera memoria)
- Métodos de configuración (algoritmo, quantum, estrategia de memoria)

**Uso en la exposición**: Explicar cómo todos los módulos trabajan juntos en cada ciclo del sistema.

---

### 🖥️ `interfaz.py` - Módulo de Interfaz Gráfica
**Propósito**: Interfaz gráfica del simulador.

**Clase Principal**: `SimuladorApp`

**Componentes**:
- Panel de configuración
- Tabla de procesos
- Visualización de memoria
- Gráfico de Gantt
- Log de eventos

**Uso en la exposición**: Mostrar visualmente el funcionamiento del sistema.

---

### 🎬 `main.py` - Archivo Principal
**Propósito**: Punto de entrada del programa. Inicializa y ejecuta la aplicación.

---

## Flujo de Ejecución

1. **Usuario crea proceso** → `modulo_procesos.py` (crear_proceso)
2. **Sistema intenta cargar a memoria** → `modulo_memoria.py` (asignar_memoria)
3. **Si hay memoria disponible** → Proceso pasa a cola de listos
4. **Planificador selecciona proceso** → `modulo_planificador.py` (seleccionar_proximo_proceso)
5. **Despachador asigna CPU** → `modulo_despachador.py` (despachar_proceso)
6. **CPU ejecuta tick** → `modulo_cpu.py` (ejecutar_tick)
7. **Proceso termina/bloquea/quantum agotado** → Libera CPU y vuelve al paso 4

---

## Cómo Usar en la Exposición

1. **Módulo de CPU**: Explicar que cada tick representa una unidad de tiempo
2. **Módulo de Procesos**: Mostrar cómo se crean y gestionan los procesos
3. **Módulo de Memoria**: Demostrar los algoritmos de asignación
4. **Módulo de Planificador**: Comparar diferentes algoritmos
5. **Módulo de Despachador**: Explicar el cambio de contexto
6. **Coordinador**: Mostrar cómo todo funciona en conjunto

---

## Ejecución

Para ejecutar el simulador:

```bash
python main.py
```

Todos los módulos deben estar en el mismo directorio.

