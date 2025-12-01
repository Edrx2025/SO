"""
Módulo del Despachador
Da el control de la CPU al proceso seleccionado por el planificador
"""


class Despachador:
    """
    Despachador de procesos
    Transfiere el control de la CPU al proceso seleccionado
    """
    def __init__(self):
        pass

    def despachar_proceso(self, proceso, gestor_procesos):
        """
        Despacha (asigna CPU) a un proceso
        
        Cambia el estado del proceso a EJECUCION y lo marca como proceso actual
        
        Args:
            proceso: Proceso a despachar
            gestor_procesos: Gestor de procesos que contiene las colas
            
        Returns:
            True si se despachó correctamente, False en caso contrario
        """
        if not proceso:
            return False

        # Cambiar estado del proceso a EJECUCION
        proceso.estado = "EJECUCION"
        
        # Remover de la cola de listos si está ahí
        if proceso in gestor_procesos.cola_listos:
            gestor_procesos.cola_listos.remove(proceso)
        
        # Asignar como proceso en ejecución
        gestor_procesos.proceso_ejecucion = proceso
        
        return True

    def liberar_cpu(self, proceso, gestor_procesos, nuevo_estado="LISTO"):
        """
        Libera la CPU del proceso actual
        
        Cambia el estado del proceso y lo remueve de la ejecución
        
        Args:
            proceso: Proceso que está liberando la CPU
            gestor_procesos: Gestor de procesos
            nuevo_estado: Nuevo estado del proceso ("LISTO", "BLOQUEADO", etc.)
        """
        if not proceso:
            return

        proceso.estado = nuevo_estado
        
        # Si el proceso vuelve a listos, agregarlo a la cola
        if nuevo_estado == "LISTO" and proceso not in gestor_procesos.cola_listos:
            gestor_procesos.cola_listos.append(proceso)
        
        # Liberar la CPU
        if gestor_procesos.proceso_ejecucion == proceso:
            gestor_procesos.proceso_ejecucion = None

