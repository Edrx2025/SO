//Guardas de inclusión
#ifndef PROCESOS_H
#define PROCESOS_H

    //Constantes
    #define MAX_PROCESOS 1000
    #define READY 0
    #define RUNNING 1
    #define BLOCKED 2
    #define TERMINATED 3

    //Estructura del Process Control Block
    typedef struct{
        int pid;
        int estado;
        int prioridad;
        int pc; //Program Counter
        int tiempo_total;
        int tiempo_restante;
        int tam_memoria;
        int direccion_base;
    }PCB;

    //Declaración de métodos
    PCB* crearProceso(int,int);
    PCB* obtenerSiguienteReady();
    void bloquearProceso(int);
    void desbloquearProceso(int);
    void terminarProceso(int);
    PCB* buscarProceso(int);
    void mostrarColas();
    
    int getSizeReady();
    PCB* getReady(int);
    int getSizeBlocked();
    PCB* getBlocked(int);
    PCB* sacar_de_cola_ready(int);
    void agregar_a_cola_ready(PCB*);
    void terminarProcesoPorPuntero(PCB*);


#endif