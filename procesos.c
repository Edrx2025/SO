#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "time.h"
#include "procesos.h"
#include "memoria.h"

//Variables globales
PCB* cola_ready[MAX_PROCESOS];
PCB* cola_blocked[MAX_PROCESOS];
PCB* cola_terminated[MAX_PROCESOS];

int size_ready=0;
int size_blocked=0;
int size_terminated=0;

int ultimo_pid=0;

//--Métodos propios--
void agregar_a_cola(PCB** cola,int* size,PCB* p){
    if(*size >=MAX_PROCESOS){
        return;
    }
    cola[*size]=p;
    (*size)++;
}

PCB* sacar_de_cola(PCB** cola,int* size, int indice){
    if(indice<0 || indice>= *size){
        return NULL;
    }

    //Puntero que apunta al PCB del proceso que se va a sacar de la cola
    PCB* p=cola[indice];
        
    //Reemplazamos los punteros originales
    for(int i=indice;i<(*size)-1;i++){
        cola[i]=cola[i+1];
    }

    (*size)--;

    cola[*size]=NULL;

    return p;
}

//Buscar en cualquier tipo de cola por PID
PCB* buscar_en_cola(PCB** cola,int size,int pid, int* pos){
    //Recorriendo cierto tipo de cola
    for(int i=0;i<size;i++){
        if(cola[i]->pid==pid){
            if(pos){
                *pos=i;
            }
            return cola[i];
        }
    }
    
    return NULL;
}

//--Implementación de los métodos del archivo de cabecera--

PCB* crearProceso(int prioridad,int tam_memoria){
    PCB* nuevoProceso= (PCB*) malloc(sizeof(PCB));
    
    nuevoProceso->pid=ultimo_pid;
    nuevoProceso->estado=READY;
    nuevoProceso->tiempo_total=10+rand() %20; //Tiempo aleatorio;
    nuevoProceso->tiempo_restante=nuevoProceso->tiempo_total;
    nuevoProceso->prioridad=prioridad;
    nuevoProceso->tam_memoria=tam_memoria;
    nuevoProceso->pc=0;

    //Asignación de memoria
    int direccion=asignarMemoria(ultimo_pid,tam_memoria);

    //->Si no hay memoria disponible
    if(direccion==-1){
        free(nuevoProceso);
        return NULL;
    }

    nuevoProceso->direccion_base=direccion;
    ultimo_pid++;    //Incrementamos el process id
    agregar_a_cola(cola_ready,&size_ready,nuevoProceso);

    return nuevoProceso;
}


void bloquearProceso(int pid){
    int pos;
    PCB* p=buscar_en_cola(cola_ready,size_ready,pid,&pos);
    
    if(!p){
        return;
    }

    //Cambiamos el estado de ese proceso mediante el PCB
    p->estado=BLOCKED;
    
    //Quitamos el proceso de la cola de listos
    sacar_de_cola(cola_ready,&size_ready,pos);

    //Añadimos ese proceso a la cola de bloqueados
    agregar_a_cola(cola_blocked,&size_blocked,p);
}

void desbloquearProceso(int pid){
    int pos;
    PCB* p=buscar_en_cola(cola_blocked,size_blocked,pid,&pos);

    if(!p){
        return;
    }

    //Cambiamos el estado de ese proceso mediante el PCB
    p->estado=READY;

    //Quitamos el proceso de la cola de bloqueados
    sacar_de_cola(cola_blocked,&size_blocked,pos);

    //Añadimos el proceso a ala cosa de listos
    agregar_a_cola(cola_ready,&size_ready,p);
}

void terminarProceso(int pid){
    int pos;
    PCB* p=buscar_en_cola(cola_ready,size_ready,pid,&pos);

    if(p){
       sacar_de_cola(cola_ready,&size_ready,pos);
    }
    else{
        p=buscar_en_cola(cola_blocked,size_blocked,pid,&pos);
        if(p){
            sacar_de_cola(cola_blocked,&size_blocked,pos);
        }
    }

    if(!p){
        return;
    }

    p->estado=TERMINATED;
    agregar_a_cola(cola_terminated,&size_terminated,p);
    
    liberarMemoria(pid);
}

PCB* buscarProceso(int pid){
    int pos;
    PCB* p;
    
    p=buscar_en_cola(cola_ready,size_ready,pid,&pos);
    if(p){
        return p;
    }

    p=buscar_en_cola(cola_blocked,size_blocked,pid,&pos);
    if(p){
        return p;
    }
    
    p=buscar_en_cola(cola_terminated,size_terminated,pid,&pos);
    return p;

}

PCB* obtenerSiguienteReady(){
    if(size_ready==0){
        return NULL;
    }

    return sacar_de_cola(cola_ready,&size_ready,0);
}

void mostrarColas(){
    printf("\n\n--Cola de listos--\n");
    for(int i=0;i<size_ready;i++){
        printf("PID %i | PRIORIDAD %i\n",cola_ready[i]->pid,cola_ready[i]->prioridad);
    }

    printf("\n\n--Cola de bloqueados--\n");
    for(int i=0;i<size_blocked;i++){
        printf("PID %i\n",cola_blocked[i]->pid);
    }

    printf("\n\n--Cola de terminados--\n");
    for(int i=0;i<size_terminated;i++){
        printf("PID %i\n",cola_terminated[i]->pid);
    }
}

int getSizeReady(){
    return size_ready;
}

PCB* getReady(int indice){
    if(indice<0 || indice>=size_ready){
        return NULL;
    }
    return cola_ready[indice];
}

int getSizeBlocked(){
    return size_blocked;
}

PCB* getBlocked(int indice){
    return cola_blocked[indice];
}

PCB* sacar_de_cola_ready(int indice){
    return sacar_de_cola(cola_ready,&size_ready,indice);
}

void agregar_a_cola_ready(PCB* p){
    agregar_a_cola(cola_ready,&size_ready,p);
}

void terminarProcesoPorPuntero(PCB* p){
    if(!p){
        return;
    }

    p->estado=TERMINATED;
    agregar_a_cola(cola_terminated,&size_terminated,p);
    liberarMemoria(p->pid);
}









