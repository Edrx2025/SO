"""
Módulo del Planificador
Selecciona el próximo proceso a ejecutarse según la política de planificación
"""


class Planificador:
    """
    Planificador de procesos
    Selecciona el próximo proceso a ejecutarse según diferentes algoritmos
    """
    def __init__(self, algoritmo="Round Robin", quantum=3):
        """
        Inicializa el planificador
        
        Args:
            algoritmo: Algoritmo de planificación ("Round Robin", "FCFS", "SJF", "Prioridad")
            quantum: Tamaño del quantum para Round Robin
        """
        self.algoritmo = algoritmo
        self.quantum = quantum
        self.contador_quantum = 0
        self.historia_gantt = []

    def seleccionar_proximo_proceso(self, cola_listos):
        """
        Selecciona el próximo proceso a ejecutarse según el algoritmo
        
        Args:
            cola_listos: Lista de procesos listos para ejecutarse
            
        Returns:
            Proceso seleccionado o None si no hay procesos listos
        """
        if not cola_listos:
            return None

        # Ordenar la cola según el algoritmo
        self.ordenar_cola_listos(cola_listos)

        # Retornar el primer proceso (el seleccionado)
        return cola_listos[0] if cola_listos else None

    def ordenar_cola_listos(self, cola_listos):
        """
        Ordena la cola de listos según el algoritmo de planificación
        
        Args:
            cola_listos: Lista de procesos a ordenar (se modifica in-place)
        """
        if self.algoritmo == "SJF":
            # Shortest Job First: ordenar por tiempo de ejecución restante
            cola_listos.sort(key=lambda p: p.burst_time_restante)
        elif self.algoritmo == "Prioridad":
            # Prioridad: ordenar por prioridad (menor número = mayor prioridad)
            cola_listos.sort(key=lambda p: p.prioridad)
        # Para Round Robin y FCFS no se ordena (FIFO)

    def registrar_gantt(self, proceso):
        """
        Registra la ejecución de un proceso en el gráfico de Gantt
        
        Args:
            proceso: Proceso que se está ejecutando
        """
        if self.historia_gantt and self.historia_gantt[-1]["pid"] == proceso.pid:
            # Si es el mismo proceso, incrementar duración
            self.historia_gantt[-1]["duracion"] += 1
        else:
            # Nuevo proceso, agregar entrada
            self.historia_gantt.append({
                "pid": proceso.pid,
                "duracion": 1,
                "color": proceso.color
            })

    def limpiar_gantt(self):
        """
        Limpia el historial del gráfico de Gantt
        """
        self.historia_gantt = []

    def reset_quantum(self):
        """
        Resetea el contador de quantum
        """
        self.contador_quantum = 0

    def incrementar_quantum(self):
        """
        Incrementa el contador de quantum
        """
        self.contador_quantum += 1

    def quantum_agotado(self):
        """
        Verifica si el quantum se ha agotado
        
        Returns:
            True si el quantum se agotó, False en caso contrario
        """
        return self.contador_quantum >= self.quantum

