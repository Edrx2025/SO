"""
Módulo de Procesos
Gestiona la creación de procesos, colas de procesos y estados
"""

from constantes import get_color_proceso


class PCB:

    def __init__(self, pid, size, burst_time, prioridad):
        self.pid = pid
        self.size = size
        self.burst_time_total = burst_time
        self.burst_time_restante = burst_time
        self.prioridad = prioridad
        self.estado = "NUEVO"
        self.base_address = -1
        self.tiempo_bloqueado_restante = 0
        self.color = get_color_proceso(pid)
        self.pc = 0  # Program Counter: 

    def __repr__(self):
        return f"P{self.pid}"


class GestorProcesos:
    """
    Gestiona las colas de procesos y sus transiciones de estado
    """
    def __init__(self):
        self.cola_nuevos = []
        self.cola_listos = []
        self.cola_bloqueados = []
        self.cola_terminados = []
        self.proceso_ejecucion = None
        self.pid_counter = 1

    def crear_proceso(self, size, burst_time, prioridad):
        """
        Crea un nuevo proceso y lo agrega a la cola de nuevos
        """
        proceso = PCB(self.pid_counter, size, burst_time, prioridad)
        self.cola_nuevos.append(proceso)
        self.pid_counter += 1
        return proceso

    def agregar_a_listos(self, proceso):
        """
        Agrega un proceso a la cola de listos
        Solo se agrega si hay memoria disponible (verificado externamente)
        """
        if proceso.estado == "NUEVO":
            proceso.estado = "LISTO"
            self.cola_listos.append(proceso)
            if proceso in self.cola_nuevos:
                self.cola_nuevos.remove(proceso)

    def agregar_a_terminados(self, proceso):
        """
        Agrega un proceso a la cola de terminados
        """
        proceso.estado = "TERMINADO"
        if proceso in self.cola_terminados:
            return
        self.cola_terminados.append(proceso)
        # Remover de otras colas
        if proceso in self.cola_listos:
            self.cola_listos.remove(proceso)
        if proceso in self.cola_bloqueados:
            self.cola_bloqueados.remove(proceso)
        if self.proceso_ejecucion == proceso:
            self.proceso_ejecucion = None

    def sacar_de_listos(self, proceso):
        """
        Saca un proceso de la cola de listos
        (Usado cuando el proceso ha culminado o pasa a ejecución)
        """
        if proceso in self.cola_listos:
            self.cola_listos.remove(proceso)

    def agregar_a_bloqueados(self, proceso):
        """
        Agrega un proceso a la cola de bloqueados (I/O)
        """
        proceso.estado = "BLOQUEADO"
        if proceso not in self.cola_bloqueados:
            self.cola_bloqueados.append(proceso)
        if self.proceso_ejecucion == proceso:
            self.proceso_ejecucion = None

    def retornar_de_bloqueados(self, proceso):
        """
        Retorna un proceso de la cola de bloqueados a la cola de listos
        """
        if proceso in self.cola_bloqueados:
            proceso.estado = "LISTO"
            self.cola_bloqueados.remove(proceso)
            self.cola_listos.append(proceso)

    def reset_total(self):
        """
        Resetea todas las colas de procesos
        """
        self.cola_nuevos = []
        self.cola_listos = []
        self.cola_bloqueados = []
        self.cola_terminados = []
        self.proceso_ejecucion = None
        self.pid_counter = 1

    def obtener_todos_procesos(self):
        """
        Retorna todos los procesos activos (no terminados)
        """
        all_procs = self.cola_nuevos + self.cola_listos + self.cola_bloqueados
        if self.proceso_ejecucion:
            all_procs.append(self.proceso_ejecucion)
        return all_procs

