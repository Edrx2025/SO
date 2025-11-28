#include "memoria.h"
#include "cpu.h"

//--Variables globales--
int algoritmo_actual=FIRST_FIT;
BloqueMemoria memoria[MAX_BLOQUES];
int total_bloques=0;
int id_bloque=1;

//--Métodos propios--
int buscarMemoria(int tam_proceso){
    int elegido=-1;

    if(algoritmo_actual==FIRST_FIT){
        for(int i=0;i<total_bloques;i++){
            if(memoria[i].pid==-1 && memoria[i].tam>=tam_proceso){
                return i;
            }
        }   
    }

    if(algoritmo_actual==BEST_FIT){
        int primero=0;
        int dif_menor,dif_aux;

        for(int i=0;i<total_bloques;i++){
            if(memoria[i].pid==-1 && memoria[i].tam>=tam_proceso){
                dif_aux=memoria[i].tam-tam_proceso;
                if(primero==0){
                    dif_menor=dif_aux;
                    elegido=i;
                    primero++;
                }

                else{
                    if(dif_menor>dif_aux){
                        dif_menor=dif_aux;
                        elegido=i;
                    }
                }
            }
        }
    }

    if(algoritmo_actual==WORST_FIT){
        int primero=0;
        int dif_mayor=0,dif_aux=0;

        for(int i=0;i<total_bloques;i++){
            if(memoria[i].pid==-1 && memoria[i].tam>=tam_proceso){
                dif_aux=memoria[i].tam-tam_proceso;
                if(primero==0){
                    primero++;
                    dif_mayor=dif_aux;
                    elegido=i;
                }
                else{
                    if(dif_mayor<dif_aux){
                        dif_mayor=dif_aux;
                        elegido=i;
                    }
                }
            }
        }
    }
    
    return elegido;

}

//--Implementación de métodos del archivo de cabecera--
void initMemoria(int tama_total){
    memoria[0].id=id_bloque;
    memoria[0].inicio=0;
    memoria[0].tam=tama_total;
    memoria[0].pid=-1;
    total_bloques++;
    id_bloque++;
}

void setAlgoritmAsigMem(int algoritm){
    algoritmo_actual=algoritm;
}

int asignarMemoria(int pid, int tam){
    //Averiguando si hay memoria disponible
    int indice=buscarMemoria(tam);
    if(indice<0){
        printf("\nNo hay memoria disponible");
        return -1;
    }

    BloqueMemoria* p=&memoria[indice];
    int dirBase=p->inicio;

    //-Si el tamaño del proceso coincide con el tamaño del bloque-
    if(p->tam==tam){
        p->pid=pid;
        return dirBase;
    }

    //-Si el tamaño del proceso es menor que el bloque-
    //-> Creamos un bloque nuevo (Para el lado izquierdo)
    BloqueMemoria nuevo;
    nuevo.inicio=p->inicio;
    nuevo.tam=tam;
    nuevo.pid=pid;
    nuevo.id=p->id;


    //->Partimos el bloque original y el espacio libre queda en la derecha
    p->inicio+=tam;
    p->tam-=tam;
    p->id=id_bloque;
    id_bloque++;

    //-> Introducimos el bloque nuevo, desplazando los demás bloques a la derecha.
    for(int i=total_bloques;i>indice;i--){
        memoria[i]=memoria[i-1];
    }
    memoria[indice]=nuevo;
    total_bloques++;

    return dirBase;
}

void liberarMemoria(int pid) {
    for(int i = 0; i < total_bloques; i++) {
        if(memoria[i].pid == pid) {
            memoria[i].pid = -1;  // Marcamos como bloque de memoria libre

            // Intentar fusionar con el anterior
            if(i>0 && memoria[i-1].pid==-1) {
                memoria[i-1].tam += memoria[i].tam;

                for(int j=i;j<total_bloques-1; j++){
                    memoria[j] = memoria[j+1];
                }

                total_bloques--;
                i--; // Reprocesar el índice fusionado
            }

            // Intentar fusionar con el siguiente
            if(i<total_bloques-1 && memoria[i+1].pid == -1) {
                memoria[i].tam += memoria[i+1].tam;

                for(int j = i+1; j<total_bloques-1; j++){
                    memoria[j] = memoria[j+1];
                }
                
                total_bloques--;
            }

            return;
        }
    }
}

BloqueMemoria* getBloquesMemoria(int *out){
    if(out){
        *out=total_bloques;
    }
    return memoria;
}

int getTotalBloques(){
    return total_bloques;
}