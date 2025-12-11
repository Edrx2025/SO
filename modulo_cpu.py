"""
Módulo de CPU
Gestiona la unidad de tiempo (tick) y la ejecución de procesos
"""

import random


class CPU:
    """
    Representa la CPU del sistema
    Gestiona la unidad de tiempo (tick) y la ejecución de procesos
    """
    def __init__(self):
        self.tick_count = 0
        self.proceso_actual = None

    def ejecutar_tick(self, proceso, algoritmo="Round Robin", quantum=3, contador_quantum=0):
        """
        Ejecuta un tick (unidad de tiempo) del proceso actual
        
        Args:
            proceso: Proceso que se está ejecutando
            algoritmo: Algoritmo de planificación actual
            quantum: Tamaño del quantum para Round Robin
            contador_quantum: Contador actual del quantum
            
        Returns:
            dict con información del tick:
            - 'proceso_terminado': True si el proceso terminó
            - 'quantum_agotado': True si se agotó el quantum (solo RR)
            - 'bloqueado_io': True si el proceso se bloqueó por I/O
            - 'tiempo_bloqueo': Tiempo de bloqueo si se bloqueó
            - 'nuevo_contador_quantum': Nuevo valor del contador
        """
        self.tick_count += 1
        resultado = {
            'proceso_terminado': False,
            'quantum_agotado': False,
            'bloqueado_io': False,
            'tiempo_bloqueo': 0,
            'nuevo_contador_quantum': contador_quantum
        }

        if not proceso:
            return resultado

        # Actualizar Program Counter (simula ejecución de instrucción)
        proceso.pc += 1
        
        # Reducir el tiempo de ejecución restante
        proceso.burst_time_restante -= 1

        # Verificar si el proceso terminó
        if proceso.burst_time_restante <= 0:
            resultado['proceso_terminado'] = True
            return resultado

        # Manejar según el algoritmo
        if algoritmo == "Round Robin":
            nuevo_contador = contador_quantum + 1
            resultado['nuevo_contador_quantum'] = nuevo_contador
            
            if nuevo_contador >= quantum:
                resultado['quantum_agotado'] = True
                return resultado
        else:
            # Para FCFS, SJF, Prioridad: posibilidad de bloqueo por I/O
            if random.random() < 0.01:  # 1% de probabilidad de bloqueo
                tiempo_bloqueo = random.randint(5, 20)
                resultado['bloqueado_io'] = True
                resultado['tiempo_bloqueo'] = tiempo_bloqueo
                return resultado

        return resultado

    def obtener_tick_count(self):
        """
        Retorna el número de ticks ejecutados
        """
        return self.tick_count

    def reset(self):
        """
        Resetea el contador de ticks
        """
        self.tick_count = 0
        self.proceso_actual = None

