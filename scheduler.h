#ifndef SCHEDULER_H
#define SCHEDULER_H

#include "procesos.h"

#define FCFS 0
#define SJF 1
#define RR 2

//--Declaración de metodos--
void setPolitica(int);
int getPolitica();
void setQuantum(int);
PCB* schedulerNextProceso();

//Unidad de tiempo (tick)
void rr_tick(PCB*);

#endif