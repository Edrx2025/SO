#include "stdio.h"
#include "scheduler.h"

//--Variables globales--
//-> Politica inicial
int politica_actual=FCFS;

//->Quantum inicial
int quantum_rr=3;
int contador_rr=0;

//--Implementación de métodos--
void setPolitica(int politica){
    politica_actual=politica;
}

int getPolitica(){
    return politica_actual;
}

void setQuantum(int q){
    if(q>0){
        quantum_rr=q;    
    }
}

//-- Politica FIRST COME FIRST SEVERD --
PCB* schedulerFCFS(){
   return obtenerSiguienteReady();
}

//-- Política SH0RTEST JOB FIRST --
PCB* schedulerSJF(){
    int mejor=0;
    int size_ready=getSizeReady();

    for(int i=1;i<size_ready;i++){
        PCB* p=getReady(i);
        PCB* p_mejor=getReady(mejor);

        if(p_mejor->tiempo_restante>p->tiempo_restante){
            mejor=i;
        }
    }

    //Sacamos de la cola de procesos listos al proceso que tenga el menor tiempo restante.
    return sacar_de_cola_ready(mejor);
}

//-- Politica ROUND ROBIN --
PCB* schedulerRR(){
    contador_rr=0;
    return obtenerSiguienteReady();
}

//Unidad de tiempo (tick)
void rr_tick(PCB* proceso_actual){

    if(!proceso_actual){
        return;
    }

    contador_rr++;

    //Si el contador llega al time quantum, el proceso regresa a la cola ready (al final)
    if(contador_rr>=quantum_rr){
        contador_rr=0;
        proceso_actual->estado=READY;
        agregar_a_cola_ready(proceso_actual);
    }
}

PCB* schedulerNextProceso(){
    if(politica_actual==FCFS){
        return schedulerFCFS();
    }

    if(politica_actual==SJF){
        return schedulerSJF();
    }

    if(politica_actual==RR){
        return schedulerRR();
    }

    return NULL;
}