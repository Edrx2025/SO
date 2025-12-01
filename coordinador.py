"""
Módulo Coordinador
Integra todos los módulos del simulador y coordina su funcionamiento
"""

from modulo_cpu import CPU
from modulo_procesos import GestorProcesos
from modulo_memoria import GestorMemoria
from modulo_planificador import Planificador
from modulo_despachador import Despachador
import random


class CoordinadorSO:
    """
    Coordinador del Sistema Operativo
    Integra CPU, Procesos, Memoria, Planificador y Despachador
    """
    def __init__(self, memoria_total=1024, algoritmo="Round Robin", quantum=3, estrategia_mem="First Fit"):
        """
        Inicializa el coordinador con todos los módulos
        
        Args:
            memoria_total: Tamaño total de memoria en KB
            algoritmo: Algoritmo de planificación
            quantum: Tamaño del quantum
            estrategia_mem: Estrategia de asignación de memoria
        """
        self.cpu = CPU()
        self.gestor_procesos = GestorProcesos()
        self.memoria = GestorMemoria(memoria_total, estrategia_mem)
        self.planificador = Planificador(algoritmo, quantum)
        self.despachador = Despachador()

    def ejecutar_ciclo(self):
        """
        Ejecuta un ciclo completo del sistema operativo (tick)
        
        Returns:
            Lista de mensajes de log generados durante el ciclo
        """
        logs = []

        # 1. CARGAR PROCESOS NUEVOS A MEMORIA
        for proc in list(self.gestor_procesos.cola_nuevos):
            if self.memoria.asignar_memoria(proc):
                # Si hay memoria disponible, agregar a cola de listos
                self.gestor_procesos.agregar_a_listos(proc)
                logs.append(f"✔ P{proc.pid} entra en RAM.")
            # Si no hay memoria, el proceso permanece en cola_nuevos

        # 2. RETORNO DE I/O (Procesos bloqueados)
        for proc in list(self.gestor_procesos.cola_bloqueados):
            proc.tiempo_bloqueado_restante -= 1
            if proc.tiempo_bloqueado_restante <= 0:
                # El proceso vuelve de I/O
                self.gestor_procesos.retornar_de_bloqueados(proc)
                logs.append(f"⬅ P{proc.pid} vuelve de I/O.")

        # 3. EJECUCIÓN (CPU - Tick)
        if self.gestor_procesos.proceso_ejecucion:
            proc = self.gestor_procesos.proceso_ejecucion
            
            # Ejecutar tick en CPU
            resultado = self.cpu.ejecutar_tick(
                proc, 
                self.planificador.algoritmo, 
                self.planificador.quantum,
                self.planificador.contador_quantum
            )
            
            # Registrar en Gantt
            self.planificador.registrar_gantt(proc)

            # Actualizar contador de quantum para Round Robin
            if self.planificador.algoritmo == "Round Robin":
                self.planificador.contador_quantum = resultado['nuevo_contador_quantum']

            # Manejar resultados del tick
            if resultado['proceso_terminado']:
                # Proceso terminado
                self.terminar_proceso(proc)
                logs.append(f"★ P{proc.pid} TERMINADO.")
                
            elif self.planificador.algoritmo == "Round Robin" and resultado['quantum_agotado']:
                # Quantum agotado en Round Robin
                self.despachador.liberar_cpu(proc, self.gestor_procesos, "LISTO")
                self.planificador.reset_quantum()
                logs.append(f"⏱ [RR] P{proc.pid} Quantum agotado.")
                
            elif resultado['bloqueado_io']:
                # Proceso bloqueado por I/O
                proc.tiempo_bloqueado_restante = resultado['tiempo_bloqueo']
                self.gestor_procesos.agregar_a_bloqueados(proc)
                self.despachador.liberar_cpu(proc, self.gestor_procesos, "BLOQUEADO")
                logs.append(f"✋ P{proc.pid} Bloqueado por I/O.")

        # 4. DESPACHADOR - Seleccionar y despachar próximo proceso
        if not self.gestor_procesos.proceso_ejecucion and self.gestor_procesos.cola_listos:
            # El planificador selecciona el próximo proceso
            siguiente = self.planificador.seleccionar_proximo_proceso(
                self.gestor_procesos.cola_listos
            )
            
            if siguiente:
                # El despachador asigna la CPU
                self.despachador.despachar_proceso(siguiente, self.gestor_procesos)
                self.planificador.reset_quantum()

        return logs

    def terminar_proceso(self, proceso):
        """
        Termina un proceso: libera memoria y lo mueve a terminados
        """
        proceso.estado = "TERMINADO"
        self.memoria.liberar_memoria(proceso)
        self.gestor_procesos.agregar_a_terminados(proceso)
        self.despachador.liberar_cpu(proceso, self.gestor_procesos, "TERMINADO")

    def agregar_proceso(self, size, burst_time, prioridad):
        """
        Crea y agrega un nuevo proceso al sistema
        """
        return self.gestor_procesos.crear_proceso(size, burst_time, prioridad)

    def cambiar_algoritmo(self, nuevo_algoritmo):
        """
        Cambia el algoritmo de planificación
        """
        self.planificador.algoritmo = nuevo_algoritmo

    def cambiar_estrategia_memoria(self, nueva_estrategia):
        """
        Cambia la estrategia de asignación de memoria
        """
        self.memoria.estrategia = nueva_estrategia

    def cambiar_quantum(self, nuevo_quantum):
        """
        Cambia el tamaño del quantum
        """
        self.planificador.quantum = nuevo_quantum

    def reiniciar_memoria(self, nuevo_tamano):
        """
        Reinicia la memoria con un nuevo tamaño
        """
        self.memoria.reiniciar_memoria(nuevo_tamano)
        self.gestor_procesos.reset_total()
        self.cpu.reset()
        self.planificador.limpiar_gantt()
        self.planificador.reset_quantum()

    def reset_total(self):
        """
        Resetea completamente el sistema
        """
        self.reiniciar_memoria(self.memoria.total_size)

