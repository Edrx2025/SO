#ifndef MEMORIA_H
#define MEMORIA_H

#define FIRST_FIT 0
#define BEST_FIT 1
#define WORST_FIT 2
#define MAX_BLOQUES 100

typedef struct{
    int inicio; 
    int tam;
    int pid; //PID del proceso que ocupa el bloque de memoria
    int id; //Identificador del bloque de memoria
}BloqueMemoria;

//Declaración de métodos
void initMemoria(int);
void setAlgoritmAsigMem(int);

int asignarMemoria(int, int);
void liberarMemoria(int);

BloqueMemoria* getBloquesMemoria(int*);
int getTotalBloques();
#endif
