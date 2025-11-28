#include "stdio.h"
#include "cpu.h"

//Variable global
PCB* cpu_proceso_running=NULL;

//-- IMPLEMENTACION DE METODOS --

//->Obtener el proceso en ejecución
PCB* cpu_getProceso(){
    return cpu_proceso_running;
}

//->Libera la CPU
void cpu_liberar(){
    cpu_proceso_running=NULL;
}

//->Tick del CPU
void cpu_tick(){
    //Si no se ha asignado un proceso al recurso CPU
    if(!cpu_proceso_running){
        cpu_proceso_running = schedulerNextProceso();
        if(cpu_proceso_running){
            cpu_proceso_running->estado=RUNNING;
        }
    }

    //Si no hay procesos en la cola de procesos listos
    if(!cpu_proceso_running){
        printf("\n[CPU]: No hay procesos para ejecutar\n");
        return;
    }

    //Reducimos el tiempo restante del proceso que se está ejecutando
    cpu_proceso_running->tiempo_restante--;

    
    //Si el proceso terminó, CPU queda libre
    if(cpu_proceso_running->tiempo_restante<=0){
        printf("\n[CPU]: Proceso PID %i ha terminado\n",cpu_proceso_running->pid);
        terminarProcesoPorPuntero(cpu_proceso_running); //Movemos ese proceso a la cola de terminados y liberamos memoria
        cpu_liberar();
        return;
    }
    
    //RR: Avisando que ocurrió un tick 
    if(getPolitica()==RR){
        rr_tick(cpu_proceso_running);    
    }
    
    //Si el RR lo devolvio al estado READY, CPU queda libre
    if(getPolitica()==RR && cpu_proceso_running->estado==READY){
        printf("\n[CPU]: Proceso PID %i volvió al estado READY por Round Robinb\n",cpu_proceso_running->pid);
        cpu_liberar();
        return;
    }
}

//-> Ejecución de N Ticks
void cpu_run(int n){
    for(int i=0;i<n;i++){
        printf("\n===== TICK %d =====\n", i + 1);
        cpu_tick();
        mostrarColas();
    }
}

//-> Mostrar estado del proceso en RUNNING
void cpu_reporteEstado(){
    if(!cpu_proceso_running){
        printf("[CPU]: Estoy libre\n");
        return;
    }
 
    printf("[CPU]:Proceso PID %i | (Tiempo restante: %i)\n",cpu_proceso_running->pid,cpu_proceso_running->tiempo_restante);
}
