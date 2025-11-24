// backend_simulacion.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#ifdef _WIN32
#include <windows.h>
#else
#include <unistd.h>
#endif

#include "procesos.h"
#include "scheduler.h"
#include "cpu.h"

// Buffer para logs (simulación simple de logs)
char ultimo_log[256] = "Sistema iniciado...";

void registrar_log(const char* msg) {
    snprintf(ultimo_log, 256, "%s", msg);
}

// Función auxiliar para imprimir texto del estado
const char* get_estado_str(int estado) {
    switch(estado) {
        case READY: return "READY";
        case RUNNING: return "RUNNING";
        case BLOCKED: return "BLOCKED";
        case TERMINATED: return "TERMINATED";
        default: return "UNKNOWN";
    }
}

static void json_escape_and_fprint(FILE *fp, const char *s) {
    if (!s) { fprintf(fp, ""); return; }
    fputc('"', fp);
    for (const char *p = s; *p; ++p) {
        switch (*p) {
            case '\\': fputs("\\\\", fp); break;
            case '\"': fputs("\\\"", fp); break;
            case '\n': fputs("\\n", fp); break;
            case '\r': fputs("\\r", fp); break;
            case '\t': fputs("\\t", fp); break;
            default: fputc(*p, fp); break;
        }
    }
    fputc('"', fp);
}



// Función para escribir el JSON
void exportar_estado_json() {
    FILE *fp = fopen("estado.temp", "w");
    if (fp == NULL) return;

    PCB *running = cpu_getProceso();

    fprintf(fp, "{\n");

    // 1) PROCESOS array (running + ready + blocked)
    fprintf(fp, "  \"procesos\": [\n");
    int first_proc = 1;

    if (running) {
        fprintf(fp, "    {\"pid\": %d, \"estado\": \"RUNNING\", \"burst\": %d, \"prioridad\": %d}",
                running->pid, running->tiempo_restante, running->prioridad);
        first_proc = 0;
    }

    int size_ready = getSizeReady();
    for (int i = 0; i < size_ready; i++) {
        PCB *p = getReady(i);
        if (!p) continue;
        if (!first_proc) fprintf(fp, ",\n");
        fprintf(fp, "    {\"pid\": %d, \"estado\": \"READY\", \"burst\": %d, \"prioridad\": %d}",
                p->pid, p->tiempo_restante, p->prioridad);
        first_proc = 0;
    }

    int size_blocked = getSizeBlocked();
    for (int i = 0; i < size_blocked; i++) {
        PCB *p = getBlocked(i);
        if (!p) continue;
        if (!first_proc) fprintf(fp, ",\n");
        fprintf(fp, "    {\"pid\": %d, \"estado\": \"BLOCKED\", \"burst\": %d, \"prioridad\": %d}",
                p->pid, p->tiempo_restante, p->prioridad);
        first_proc = 0;
    }

    fprintf(fp, "\n  ],\n");

    // 2) COLAS (IDs)
    // Cola listos
    fprintf(fp, "  \"cola_listos\": [");
    for (int i = 0; i < size_ready; i++) {
        PCB *p = getReady(i);
        fprintf(fp, "%d%s", p->pid, (i < size_ready - 1) ? ", " : "");
    }
    fprintf(fp, "],\n");

    // Cola bloqueados
    fprintf(fp, "  \"cola_bloqueados\": [");
    for (int i = 0; i < size_blocked; i++) {
        PCB *p = getBlocked(i);
        fprintf(fp, "%d%s", p->pid, (i < size_blocked - 1) ? ", " : "");
    }
    fprintf(fp, "],\n");

    // Cola E/S (vacía por ahora — si tienes una cola ES, reemplaza)
    fprintf(fp, "  \"cola_es\": [],\n");

    // 3) PCB actual
    if (running) {
        fprintf(fp, "  \"pcb\": {\n");
        fprintf(fp, "    \"PID\": %d,\n", running->pid);
        fprintf(fp, "    \"Estado\": \"RUNNING\",\n");
        fprintf(fp, "    \"PC\": %d,\n", running->pc);
        fprintf(fp, "    \"Prioridad\": %d,\n", running->prioridad);
        fprintf(fp, "    \"Tiempo Restante\": %d,\n", running->tiempo_restante);
        fprintf(fp, "    \"Memoria Base\": %d\n", running->direccion_base);
        fprintf(fp, "  },\n");
    } else {
        fprintf(fp, "  \"pcb\": {},\n");
    }

    // 4) MEMORIA (basado en los procesos que tenemos; ejemplo simple)
    fprintf(fp, "  \"memoria\": [\n");
    int mem_first = 1;
    // incluir running como bloque 1
    if (running) {
        fprintf(fp, "    {\"id\": 1, \"inicio\": %d, \"tam\": %d, \"proceso\": %d}",
                running->direccion_base, running->tam_memoria, running->pid);
        mem_first = 0;
    }
    for (int i = 0; i < size_ready; i++) {
        PCB *p = getReady(i);
        if (!mem_first) fprintf(fp, ",\n");
        fprintf(fp, "    {\"id\": %d, \"inicio\": %d, \"tam\": %d, \"proceso\": %d}",
                i + 2, p->direccion_base, p->tam_memoria, p->pid);
        mem_first = 0;
    }
    // agregar bloqueados a memoria también
    for (int i = 0; i < size_blocked; i++) {
        PCB *p = getBlocked(i);
        if (!mem_first) fprintf(fp, ",\n");
        fprintf(fp, "    {\"id\": %d, \"inicio\": %d, \"tam\": %d, \"proceso\": %d}",
                size_ready + i + 2, p->direccion_base, p->tam_memoria, p->pid);
        mem_first = 0;
    }
    fprintf(fp, "\n  ],\n");

    // 5) LOGS (array)
    fprintf(fp, "  \"logs\": [");
    json_escape_and_fprint(fp, ultimo_log);
    fprintf(fp, "]\n");

    fprintf(fp, "}\n");
    fclose(fp);

    // reemplazo atómico
    remove("estado.json");
    rename("estado.temp", "estado.json");
}

int main() {
    srand(time(NULL));
    registrar_log("Iniciando simulador de SO...");
    exportar_estado_json();

    // Crear procesos iniciales
    crearProceso(1, 100, 0);
    crearProceso(2, 200, 100);
    crearProceso(3, 50, 300);
    
    setPolitica(RR); // Usar Round Robin
    setQuantum(3);

    int tick = 0;

    // Bucle infinito de simulación
    while(1) {
        tick++;
        
        // Ejecutar Tick de CPU
        cpu_tick();
        
        // Lógica simple para generar logs dinámicos
        PCB* running = cpu_getProceso();
        if(running) {
            char buffer[100];
            snprintf(buffer, 100, "[Tick %d] Ejecutando PID %d (Restante: %d)", tick, running->pid, running->tiempo_restante);
            registrar_log(buffer);
        } else {
            registrar_log("[Tick] CPU Ociosa - Esperando procesos...");
            
            // Simular llegada de nuevos procesos aleatorios
            if(tick % 10 == 0) {
                crearProceso(rand()%5, 100, tick*10);
                registrar_log("¡Nuevo proceso creado!");
            }
        }

        // Exportar estado para Python
        exportar_estado_json();

        // Pausa para que la visualización sea apreciable (500ms)
        #ifdef _WIN32
            Sleep(1000); 
        #else
            usleep(1000000); 
        #endif
    }

    return 0;
}
