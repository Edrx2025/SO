"""
Módulo de Memoria
Contiene los algoritmos de asignación de memoria, búsqueda de memoria disponible,
asignación y liberación de memoria para procesos
"""

from constantes import MEMORIA_DEFAULT


class GestorMemoria:
    """
    Gestiona la memoria del sistema con diferentes algoritmos de asignación
    """
    def __init__(self, total_size=MEMORIA_DEFAULT, estrategia="First Fit"):
        """
        Inicializa el gestor de memoria
        
        Args:
            total_size: Tamaño total de la memoria en KB
            estrategia: Algoritmo de asignación ("First Fit", "Best Fit", "Worst Fit")
        """
        self.total_size = total_size
        self.mapa_memoria = [{"start": 0, "size": total_size, "estado": "LIBRE", "pid": None}]
        self.estrategia = estrategia

    def reiniciar_memoria(self, nuevo_tamano):
        """
        Reinicia la memoria con un nuevo tamaño
        """
        self.total_size = nuevo_tamano
        self.mapa_memoria = [{"start": 0, "size": nuevo_tamano, "estado": "LIBRE", "pid": None}]
        self.compactar_memoria()

    def buscar_memoria_disponible(self, tamano_requerido):
        """
        Busca bloques de memoria disponibles que puedan alojar el tamaño requerido
        
        Returns:
            Lista de índices de bloques libres que cumplen con el tamaño
        """
        bloques_libres = [i for i, b in enumerate(self.mapa_memoria) if
                          b["estado"] == "LIBRE" and b["size"] >= tamano_requerido]
        return bloques_libres

    def asignar_memoria(self, proceso):
        """
        Asigna memoria a un proceso según la estrategia configurada
        
        Args:
            proceso: Objeto PCB del proceso que necesita memoria
            
        Returns:
            True si se asignó memoria, False si no hay espacio disponible
        """
        tamano_requerido = proceso.size
        bloques_libres = self.buscar_memoria_disponible(tamano_requerido)

        if not bloques_libres:
            return False

        # Seleccionar bloque según la estrategia
        idx = -1
        if self.estrategia == "First Fit":
            # Primer bloque que cumpla con el tamaño
            idx = bloques_libres[0]
        elif self.estrategia == "Best Fit":
            # Bloque más pequeño que cumpla con el tamaño
            bloques_libres.sort(key=lambda i: self.mapa_memoria[i]["size"])
            idx = bloques_libres[0]
        elif self.estrategia == "Worst Fit":
            # Bloque más grande disponible
            bloques_libres.sort(key=lambda i: self.mapa_memoria[i]["size"], reverse=True)
            idx = bloques_libres[0]

        bloque = self.mapa_memoria[idx]

        # Asignar memoria
        if bloque["size"] > tamano_requerido:
            # Dividir el bloque si es más grande
            nuevo_bloque = {
                "start": bloque["start"],
                "size": tamano_requerido,
                "estado": "OCUPADO",
                "pid": proceso.pid
            }
            bloque["start"] += tamano_requerido
            bloque["size"] -= tamano_requerido
            self.mapa_memoria.insert(idx, nuevo_bloque)
            proceso.base_address = nuevo_bloque["start"]
        else:
            # Usar todo el bloque
            bloque["estado"] = "OCUPADO"
            bloque["pid"] = proceso.pid
            proceso.base_address = bloque["start"]

        return True

    def liberar_memoria(self, proceso):
        """
        Libera la memoria asignada a un proceso cuando ha finalizado
        
        Args:
            proceso: Objeto PCB del proceso que terminó
        """
        for bloque in self.mapa_memoria:
            if bloque["pid"] == proceso.pid:
                bloque["estado"] = "LIBRE"
                bloque["pid"] = None
                self.compactar_memoria()
                return

    def compactar_memoria(self):
        """
        Compacta la memoria uniendo bloques libres adyacentes
        """
        i = 0
        while i < len(self.mapa_memoria) - 1:
            actual = self.mapa_memoria[i]
            siguiente = self.mapa_memoria[i + 1]
            if actual["estado"] == "LIBRE" and siguiente["estado"] == "LIBRE":
                actual["size"] += siguiente["size"]
                self.mapa_memoria.pop(i + 1)
            else:
                i += 1

