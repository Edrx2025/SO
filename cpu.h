#ifndef CPU_H
#define CPU_H
#include "scheduler.h"

//--Declaración de métodos--
PCB* cpu_getProceso();

void cpu_tick();
void cpu_run(int);
void cpu_liberar();
void cpu_reporteEstado();

#endif
