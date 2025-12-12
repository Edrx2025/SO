"""
Módulo de Interfaz Gráfica
Interfaz del simulador del sistema operativo
"""

import tkinter as tk
from tkinter import ttk, messagebox
import time
import random

from constantes import *
from coordinador import CoordinadorSO
from modulo_procesos import PCB


class SimuladorApp:
    """
    Interfaz gráfica del simulador
    """
    def __init__(self, root):
        self.root = root
        self.root.title("🖥️ Simulador SO - Gestión de Memoria y Procesos")
        self.root.geometry("1400x950")
        self.root.configure(bg=COLOR_FONDO_PRINCIPAL)

        # Inicializar coordinador del sistema operativo
        self.coordinador = CoordinadorSO(
            memoria_total=MEMORIA_DEFAULT,
            algoritmo="Round Robin",
            quantum=3,
            estrategia_mem="First Fit"
        )

        self.simulando = False
        self.configurar_estilos()
        self.crear_interfaz()

    def configurar_estilos(self):
        """Configura los estilos de la interfaz"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', font=('Segoe UI', 10, 'bold'), 
                       background=COLOR_FONDO_SECUNDARIO, foreground=COLOR_TEXTO_DORADO)
        style.configure('Header.TLabel', font=('Segoe UI', 9, 'bold'),
                       background=COLOR_FONDO_SECUNDARIO, foreground=COLOR_TEXTO_DORADO)
        
        style.configure('TLabelframe', background=COLOR_FONDO_SECUNDARIO, 
                       foreground=COLOR_TEXTO_DORADO, borderwidth=2, relief='solid')
        style.configure('TLabelframe.Label', background=COLOR_FONDO_SECUNDARIO, 
                       foreground=COLOR_TEXTO_DORADO, font=('Segoe UI', 9, 'bold'))
        style.configure('TFrame', background=COLOR_FONDO_SECUNDARIO)
        style.configure('TEntry', fieldbackground=COLOR_FONDO_OSCURO, 
                       foreground=COLOR_TEXTO_CLARO, borderwidth=1, relief='solid')
        style.configure('TCombobox', fieldbackground=COLOR_FONDO_OSCURO, 
                       foreground=COLOR_TEXTO_CLARO, borderwidth=1)
        style.map('TCombobox', fieldbackground=[('readonly', COLOR_FONDO_OSCURO)])
        style.configure('TButton', background=COLOR_FONDO_OSCURO, 
                       foreground=COLOR_TEXTO_CLARO, borderwidth=1, relief='raised')
        style.map('TButton', background=[('active', COLOR_HOVER)])
        style.configure('Treeview', background=COLOR_FONDO_OSCURO, 
                       foreground=COLOR_TEXTO_CLARO, fieldbackground=COLOR_FONDO_OSCURO)
        style.configure('Treeview.Heading', background=COLOR_FONDO_OSCURO, 
                       foreground=COLOR_TEXTO_DORADO, font=('Segoe UI', 9, 'bold'))
        style.map('Treeview', background=[('selected', COLOR_PRIMARIO)])
        style.configure('TScrollbar', background=COLOR_FONDO_OSCURO, 
                       troughcolor=COLOR_FONDO_SECUNDARIO, borderwidth=0)
        style.configure('TSeparator', background=COLOR_BORDE)
        style.configure('Action.TButton', background=COLOR_DORADO, 
                       foreground="#000000", font=('Segoe UI', 9, 'bold'),
                       borderwidth=2, relief='raised')
        style.map('Action.TButton', 
                 background=[('active', COLOR_EJECUCION_BRILLO), ('pressed', COLOR_DORADO)])

        # Variables Tkinter
        self.var_quantum = tk.IntVar(value=3)
        self.var_mem_total = tk.IntVar(value=MEMORIA_DEFAULT)

    def crear_interfaz(self):
        """Crea todos los componentes de la interfaz"""
        main = ttk.Frame(self.root, style='TFrame')
        main.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        top_pane = ttk.Frame(main, style='TFrame')
        top_pane.pack(fill=tk.BOTH, expand=True)

        # Panel de configuración
        self.crear_panel_configuracion(top_pane)
        
        # Tabla de procesos
        self.crear_tabla_procesos(top_pane)
        
        # Visualización de memoria
        self.crear_visualizacion_memoria(top_pane)
        
        # Gráfico Gantt
        self.crear_grafico_gantt(main)
        
        # Log de eventos
        self.crear_log_eventos(main)

    def crear_panel_configuracion(self, parent):
        """Crea el panel de configuración"""
        panel = ttk.LabelFrame(parent, text="⚙️ Configuración", padding=15)
        panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Memoria total
        f_memt = ttk.Frame(panel, style='TFrame')
        f_memt.pack(pady=(0, 10), fill='x')
        ttk.Label(f_memt, text="💾 Total RAM (KB):", style='Header.TLabel').pack(anchor="w", pady=(0, 5))
        f_memt_in = ttk.Frame(f_memt, style='TFrame')
        f_memt_in.pack(fill='x')
        entry_mem = ttk.Entry(f_memt_in, textvariable=self.var_mem_total, width=10, font=('Segoe UI', 9))
        entry_mem.pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(f_memt_in, text="🔄 Cambiar", command=self.cambiar_tamano_memoria).pack(side=tk.LEFT)

        ttk.Separator(panel).pack(fill='x', pady=15)

        # Algoritmo de planificación
        ttk.Label(panel, text="🔄 Algoritmo de Planificación:", style='Header.TLabel').pack(pady=(0, 5))
        self.cb_algo = ttk.Combobox(panel, values=["Round Robin", "FCFS", "SJF", "Prioridad"], 
                                    state="readonly", font=('Segoe UI', 9), width=18)
        self.cb_algo.current(0)
        self.cb_algo.pack(pady=(0, 10), fill='x')
        self.cb_algo.bind("<<ComboboxSelected>>", self.al_cambiar_algoritmo)

        # Quantum
        self.frame_quantum = ttk.Frame(panel, style='TFrame')
        self.frame_quantum.pack(pady=(0, 10), fill='x')
        ttk.Label(self.frame_quantum, text="⏱️ Quantum:", style='Header.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        self.entry_quantum = ttk.Entry(self.frame_quantum, textvariable=self.var_quantum, width=6, font=('Segoe UI', 9))
        self.entry_quantum.pack(side=tk.LEFT, padx=(0, 5))
        self.btn_set_q = ttk.Button(self.frame_quantum, text="✓", width=3, command=self.set_quantum)
        self.btn_set_q.pack(side=tk.LEFT)

        ttk.Separator(panel).pack(fill='x', pady=15)

        # Estrategia de memoria
        ttk.Label(panel, text="🧩 Estrategia de Asignación:", style='Header.TLabel').pack(pady=(0, 5))
        self.cb_mem = ttk.Combobox(panel, values=["First Fit", "Best Fit", "Worst Fit"], 
                                   state="readonly", font=('Segoe UI', 9), width=18)
        self.cb_mem.current(0)
        self.cb_mem.pack(pady=(0, 10), fill='x')
        self.cb_mem.bind("<<ComboboxSelected>>", self.set_mem)

        ttk.Separator(panel).pack(fill='x', pady=20)

        # Botones de acción
        ttk.Button(panel, text="➕ Agregar Proceso Manual", command=self.popup_manual, 
                  style='Action.TButton').pack(fill='x', pady=5, ipady=3)
        ttk.Button(panel, text="🎲 Generar Procesos De Forma Aleatorio", command=self.generar_test,
                  style='Action.TButton').pack(fill='x', pady=5, ipady=3)
        self.btn_run = ttk.Button(panel, text="▶ INICIAR SIMULACIÓN", command=self.toggle,
                                  style='Action.TButton')
        self.btn_run.pack(fill='x', pady=(15, 0), ipady=8)

    def crear_tabla_procesos(self, parent):
        """Crea la tabla de procesos"""
        frame_tabla = ttk.LabelFrame(parent, text="📋 Cola de Procesos", padding=10)
        frame_tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        cols = ("PID", "Estado", "PC", "Burst", "Size", "Prio")
        self.tree = ttk.Treeview(frame_tabla, columns=cols, show='headings', 
                                style='Treeview', height=12)
        for c in cols:
            self.tree.heading(c, text=c, anchor="center")
            if c == "PID":
                self.tree.column(c, width=60, anchor="center")
            elif c == "Estado":
                self.tree.column(c, width=100, anchor="center")
            elif c == "PC":
                self.tree.column(c, width=60, anchor="center")
            else:
                self.tree.column(c, width=70, anchor="center")
        
        scrollbar_tabla = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_tabla.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_tabla.pack(side=tk.RIGHT, fill=tk.Y)

    def crear_visualizacion_memoria(self, parent):
        """Crea la visualización de memoria"""
        self.frame_mem = ttk.LabelFrame(parent, text=f"💾 RAM ({self.coordinador.memoria.total_size} KB)", padding=10)
        self.frame_mem.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(0, 0))
        self.canvas_mem = tk.Canvas(self.frame_mem, bg=COLOR_FONDO_CANVAS, width=220, 
                                   highlightthickness=2, highlightbackground=COLOR_BORDE_DORADO)
        self.canvas_mem.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.lbl_hover = ttk.Label(self.frame_mem, text="Pasa el mouse sobre la memoria para ver detalles", 
                                   relief="sunken", anchor="center", font=('Segoe UI', 8),
                                   background=COLOR_FONDO_OSCURO, foreground=COLOR_TEXTO_DORADO)
        self.lbl_hover.pack(fill='x', pady=(5, 0))
        self.canvas_mem.bind("<Motion>", self.on_hover_mem)

    def crear_grafico_gantt(self, parent):
        """Crea el gráfico de Gantt"""
        frame_gantt = ttk.LabelFrame(parent, text="📊 Línea de Tiempo (Gantt Chart)", padding=10)
        frame_gantt.pack(fill=tk.X, pady=(0, 10))

        toolbar_gantt = ttk.Frame(frame_gantt, style='TFrame')
        toolbar_gantt.pack(fill=tk.X, padx=5, pady=(0, 5))
        ttk.Label(toolbar_gantt, text="⚡ Uso de CPU:", font=('Segoe UI', 9, 'bold'),
                 foreground=COLOR_TEXTO_DORADO, background=COLOR_FONDO_SECUNDARIO).pack(side=tk.LEFT)
        ttk.Button(toolbar_gantt, text="🧹 Limpiar Gantt", command=self.limpiar_grafica_gantt).pack(side=tk.RIGHT)

        self.canvas_gantt = tk.Canvas(frame_gantt, bg=COLOR_FONDO_CANVAS, height=70,
                                       highlightthickness=2, highlightbackground=COLOR_BORDE_DORADO)
        self.canvas_gantt.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def crear_log_eventos(self, parent):
        """Crea el log de eventos"""
        frame_log = ttk.LabelFrame(parent, text="📝 Log de Eventos", padding=10)
        frame_log.pack(fill=tk.X, pady=(0, 0))
        
        log_frame = ttk.Frame(frame_log, style='TFrame')
        log_frame.pack(fill=tk.BOTH, expand=True)
        self.txt_log = tk.Text(log_frame, height=6, bg=COLOR_FONDO_OSCURO, fg=COLOR_TEXTO_CLARO, 
                              font=("Consolas", 9), wrap=tk.WORD, relief=tk.FLAT,
                              selectbackground=COLOR_PRIMARIO, insertbackground=COLOR_TEXTO_DORADO)
        scrollbar_log = ttk.Scrollbar(log_frame, orient="vertical", command=self.txt_log.yview)
        self.txt_log.configure(yscrollcommand=scrollbar_log.set)
        self.txt_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar_log.pack(side=tk.RIGHT, fill=tk.Y)

    # --- MÉTODOS DE CONTROL ---

    def cambiar_tamano_memoria(self):
        """Cambia el tamaño de la memoria"""
        try:
            nuevo_tamano = self.var_mem_total.get()
            if nuevo_tamano <= 0: raise ValueError

            self.simulando = False
            self.btn_run.config(text="▶ INICIAR SIMULACIÓN")
            self.coordinador.reiniciar_memoria(nuevo_tamano)

            self.frame_mem.config(text=f"RAM ({nuevo_tamano} KB)")
            self.update_ui()
            self.draw_mem()
            self.limpiar_grafica_gantt()
            self.log(f"⚠ SISTEMA REINICIADO. Nueva RAM: {nuevo_tamano} KB")

        except:
            messagebox.showerror("Error", "Ingrese un tamaño de memoria válido (>0).")

    def al_cambiar_algoritmo(self, event):
        """Cambia el algoritmo de planificación"""
        nuevo_algo = self.cb_algo.get()
        self.coordinador.cambiar_algoritmo(nuevo_algo)
        self.log(f"Algoritmo: {nuevo_algo}")
        if nuevo_algo == "Round Robin":
            self.entry_quantum.config(state="normal")
            self.btn_set_q.config(state="normal")
        else:
            self.entry_quantum.config(state="disabled")
            self.btn_set_q.config(state="disabled")

    def set_mem(self, e):
        """Cambia la estrategia de memoria"""
        self.coordinador.cambiar_estrategia_memoria(self.cb_mem.get())

    def set_quantum(self):
        """Establece el quantum"""
        try:
            self.coordinador.cambiar_quantum(self.var_quantum.get())
        except:
            pass

    def popup_manual(self):
        """Ventana para agregar proceso manualmente"""
        top = tk.Toplevel(self.root)
        top.title("➕ Agregar Proceso Manual")
        top.geometry("380x400")
        top.configure(bg=COLOR_FONDO_SECUNDARIO)
        top.resizable(False, False)
        
        top.transient(self.root)
        top.grab_set()
        
        main_frame = ttk.Frame(top, padding=20, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="➕ Agregar Nuevo Proceso", 
                 font=('Segoe UI', 11, 'bold'), foreground=COLOR_TEXTO_DORADO,
                 background=COLOR_FONDO_SECUNDARIO).pack(pady=(0, 20))
        
        # Campos de entrada
        frame_s = ttk.Frame(main_frame, style='TFrame')
        frame_s.pack(fill='x', pady=8)
        ttk.Label(frame_s, text="📦 Tamaño (KB):", font=('Segoe UI', 9),
                 foreground=COLOR_TEXTO_CLARO, background=COLOR_FONDO_SECUNDARIO).pack(anchor='w')
        e_s = ttk.Entry(frame_s, font=('Segoe UI', 9), width=25)
        e_s.pack(fill='x', pady=(5, 0))
        e_s.insert(0, "100")
        
        frame_b = ttk.Frame(main_frame, style='TFrame')
        frame_b.pack(fill='x', pady=8)
        ttk.Label(frame_b, text="⏱️ Tiempo de Ejecución (Seg):", font=('Segoe UI', 9),
                 foreground=COLOR_TEXTO_CLARO, background=COLOR_FONDO_SECUNDARIO).pack(anchor='w')
        e_b = ttk.Entry(frame_b, font=('Segoe UI', 9), width=25)
        e_b.pack(fill='x', pady=(5, 0))
        e_b.insert(0, "10")
        
        frame_p = ttk.Frame(main_frame, style='TFrame')
        frame_p.pack(fill='x', pady=8)
        ttk.Label(frame_p, text="⭐ Prioridad:", font=('Segoe UI', 9),
                 foreground=COLOR_TEXTO_CLARO, background=COLOR_FONDO_SECUNDARIO).pack(anchor='w')
        e_p = ttk.Entry(frame_p, font=('Segoe UI', 9), width=25)
        e_p.pack(fill='x', pady=(5, 0))
        e_p.insert(0, "1")

        def confirmar_proceso():
            try:
                size = int(e_s.get())
                burst = int(e_b.get())
                prio = int(e_p.get())
                if size <= 0 or burst <= 0:
                    messagebox.showerror("Error", "Los valores deben ser mayores a 0")
                    return
                
                mensaje = f"¿Confirmar agregar el siguiente proceso?\n\n" \
                         f"📦 Tamaño: {size} KB\n" \
                         f"⏱️ Tiempo de Ejecución: {burst} seg\n" \
                         f"⭐ Prioridad: {prio}"
                
                if messagebox.askyesno("Confirmar Proceso", mensaje, icon='question', default='yes'):
                    self.coordinador.agregar_proceso(size, burst, prio)
                    self.update_ui()
                    self.log(f"➕ Proceso agregado manualmente")
                    top.destroy()
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese valores numéricos válidos")

        btn_frame = ttk.Frame(main_frame, style='TFrame')
        btn_frame.pack(fill='x', pady=(30, 0))
        ttk.Button(btn_frame, text="✓ Confirmar y Agregar", command=confirmar_proceso, 
                  style='Action.TButton').pack(side=tk.LEFT, expand=True, padx=(0, 5), ipady=8)
        ttk.Button(btn_frame, text="✗ Cancelar", command=top.destroy).pack(side=tk.LEFT, expand=True, padx=(5, 0), ipady=8)

    def generar_test(self):
        """
        Abre una ventana para generar N procesos con atributos aleatorios
        """
        top = tk.Toplevel(self.root)
        top.title("🎲 Generador Aleatorio")
        top.geometry("350x220")
        top.configure(bg=COLOR_FONDO_SECUNDARIO)
        top.resizable(False, False)
        
        # Comportamiento modal (bloquea la ventana principal)
        top.transient(self.root)
        top.grab_set()
        
        main_frame = ttk.Frame(top, padding=20, style='TFrame')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(main_frame, text="Configuración de Generación", 
                 font=('Segoe UI', 11, 'bold'), foreground=COLOR_TEXTO_DORADO,
                 background=COLOR_FONDO_SECUNDARIO).pack(pady=(0, 20))
        
        # Campo para cantidad
        frame_cnt = ttk.Frame(main_frame, style='TFrame')
        frame_cnt.pack(fill='x', pady=10)
        
        ttk.Label(frame_cnt, text="Cantidad de procesos a generar:", font=('Segoe UI', 9),
                 foreground=COLOR_TEXTO_CLARO, background=COLOR_FONDO_SECUNDARIO).pack(anchor='w')
        
        e_cantidad = ttk.Entry(frame_cnt, font=('Segoe UI', 9), width=25)
        e_cantidad.pack(fill='x', pady=(5, 0))
        e_cantidad.insert(0, "5") # Valor por defecto
        e_cantidad.focus() # Poner el foco aquí

        def confirmar_generacion():
            try:
                cantidad = int(e_cantidad.get())
                if cantidad <= 0:
                    messagebox.showerror("Error", "La cantidad debe ser mayor a 0")
                    return
                
                # Generación de procesos aleatorios
                for _ in range(cantidad):
                    # Rangos aleatorios definidos:
                    # Tamaño: Entre 20KB y 200KB (para que quepan varios en 1024KB)
                    size = random.randint(20, 200)
                    # Burst Time: Entre 5 seg y 30 seg
                    burst = random.randint(5, 30)
                    # Prioridad: Entre 1 y 5
                    prio = random.randint(1, 5)
                    
                    self.coordinador.agregar_proceso(size, burst, prio)
                
                self.log(f"🎲 Se generaron {cantidad} procesos aleatorios.")
                self.update_ui()
                top.destroy()
                
            except ValueError:
                messagebox.showerror("Error", "Por favor ingrese un número entero válido.")

        # Botones
        btn_frame = ttk.Frame(main_frame, style='TFrame')
        btn_frame.pack(fill='x', pady=(20, 0))
        
        ttk.Button(btn_frame, text="✓ Confirmar y Agregar", command=confirmar_generacion, 
                  style='Action.TButton').pack(side=tk.LEFT, expand=True, padx=(0, 5), ipady=5)
        
        ttk.Button(btn_frame, text="✗ Cancelar", command=top.destroy).pack(side=tk.LEFT, expand=True, padx=(5, 0), ipady=5)

    def toggle(self):
        """Inicia/pausa la simulación"""
        self.simulando = not self.simulando
        if self.simulando:
            self.btn_run.config(text="⏸ PAUSAR SIMULACIÓN")
        else:
            self.btn_run.config(text="▶ INICIAR SIMULACIÓN")
        if self.simulando: 
            self.loop()

    def loop(self):
        """Bucle principal de simulación"""
        if not self.simulando: return
        msgs = self.coordinador.ejecutar_ciclo()
        for m in msgs: self.log(m)
        self.update_ui()
        self.draw_mem()
        self.draw_gantt()
        self.root.after(200, self.loop)

    def log(self, t):
        """Agrega un mensaje al log"""
        if int(self.txt_log.index('end-1c').split('.')[0]) > 200:
            self.txt_log.delete('1.0', '100.0')
        self.txt_log.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {t}\n")
        self.txt_log.see(tk.END)

    def update_ui(self):
        """Actualiza la interfaz de usuario"""
        for i in self.tree.get_children(): 
            self.tree.delete(i)
        
        gp = self.coordinador.gestor_procesos
        all_procs = gp.obtener_todos_procesos()
        all_procs.sort(key=lambda x: x.pid)
        
        estado_icons = {
            "NUEVO": "🆕",
            "LISTO": "✅",
            "EJECUCION": "⚡",
            "BLOQUEADO": "⏸️",
            "TERMINADO": "✔️"
        }
        
        for p in all_procs:
            estado_display = f"{estado_icons.get(p.estado, '')} {p.estado}"
            self.tree.insert("", tk.END, values=(
                f"P{p.pid}", 
                estado_display, 
                p.pc,  # Program Counter actualizado en tiempo real
                p.burst_time_restante, 
                f"{p.size} KB", 
                p.prioridad
            ))

    def draw_mem(self):
        """Dibuja la visualización de memoria"""
        self.canvas_mem.delete("all")
        h = self.canvas_mem.winfo_height()
        w = self.canvas_mem.winfo_width()
        if h < 50: return

        total_actual = self.coordinador.memoria.total_size
        scale = h / total_actual

        pid_ejecucion = (self.coordinador.gestor_procesos.proceso_ejecucion.pid 
                        if self.coordinador.gestor_procesos.proceso_ejecucion else None)

        y = 0
        for b in self.coordinador.memoria.mapa_memoria:
            bh = b["size"] * scale
            if b["estado"] == "OCUPADO":
                proceso = None
                all_procs = self.coordinador.gestor_procesos.obtener_todos_procesos()
                for p in all_procs:
                    if p.pid == b['pid']:
                        proceso = p
                        break
                
                if b['pid'] == pid_ejecucion:
                    color = COLOR_EJECUCION
                    outline_color = COLOR_EJECUCION_BRILLO
                    outline_width = 3
                    text_color = "#000000"
                else:
                    color = proceso.color if proceso else COLOR_OCUPADO
                    outline_color = "#2a3441"
                    outline_width = 1
                    text_color = COLOR_TEXTO_CLARO
            else:
                color = COLOR_LIBRE
                outline_color = "#1a2332"
                outline_width = 1
                text_color = "#7a8499"
            
            self.canvas_mem.create_rectangle(35, y, w - 15, y + bh, fill=color, 
                                             outline=outline_color, width=outline_width)
            
            if b["estado"] == "OCUPADO" and b['pid'] == pid_ejecucion:
                self.canvas_mem.create_rectangle(35, y, w - 15, y + min(bh * 0.3, 10), 
                                                 fill=COLOR_EJECUCION_BRILLO, 
                                                 outline="", stipple="gray25")
            
            if bh > 15:
                txt = f"P{b['pid']}" if b['pid'] else "LIBRE"
                if b['pid'] == pid_ejecucion:
                    txt = f"⚡ P{b['pid']}"
                self.canvas_mem.create_text((w + 20) / 2, y + bh / 2, text=txt, 
                                           font=("Segoe UI", 9, "bold"),
                                           fill=text_color)
            if bh > 20:
                size_text = f"{int(b['size'])} KB"
                self.canvas_mem.create_text((w + 20) / 2, y + bh / 2 + 12, text=size_text,
                                           font=("Segoe UI", 7),
                                           fill=text_color)
            self.canvas_mem.create_text(30, y + 2, text=f"{int(b['start'])}", 
                                       anchor="nw", font=("Segoe UI", 7),
                                       fill="#7a8499")
            y += bh

    def draw_gantt(self):
        """Dibuja el gráfico de Gantt"""
        self.canvas_gantt.delete("all")
        h = self.canvas_gantt.winfo_height()
        w = self.canvas_gantt.winfo_width()
        if not self.coordinador.planificador.historia_gantt: return
        visible = self.coordinador.planificador.historia_gantt[-60:]
        total = sum(item["duracion"] for item in visible)
        if total == 0: return
        scale_x = (w - 20) / max(total, 30)
        x = 10
        
        pid_ejecucion = (self.coordinador.gestor_procesos.proceso_ejecucion.pid 
                        if self.coordinador.gestor_procesos.proceso_ejecucion else None)
        
        for item in visible:
            ancho = item["duracion"] * scale_x
            if ancho < 1: ancho = 1
            
            if item['pid'] == pid_ejecucion:
                color_fill = COLOR_EJECUCION
                outline_color = COLOR_EJECUCION_BRILLO
                outline_width = 2
                text_color = "#000000"
            else:
                color_fill = item["color"]
                outline_color = "#2a3441"
                outline_width = 1
                text_color = COLOR_TEXTO_CLARO
            
            self.canvas_gantt.create_rectangle(x, 12, x + ancho, h - 12, 
                                               fill=color_fill, outline=outline_color, width=outline_width)
            if ancho > 25:
                self.canvas_gantt.create_text(x + ancho / 2, h / 2, 
                                             text=f"P{item['pid']}", 
                                             font=("Segoe UI", 9, "bold"),
                                             fill=text_color)
            elif ancho > 15:
                self.canvas_gantt.create_text(x + ancho / 2, h / 2, 
                                             text=f"P{item['pid']}", 
                                             font=("Segoe UI", 7),
                                             fill=text_color)
            x += ancho

    def limpiar_grafica_gantt(self):
        """Limpia el gráfico de Gantt"""
        self.coordinador.planificador.limpiar_gantt()
        self.canvas_gantt.delete("all")
        self.log("Gantt limpiado.")

    def on_hover_mem(self, e):
        """Maneja el hover sobre la memoria"""
        h = self.canvas_mem.winfo_height()
        if h == 0: return

        total_actual = self.coordinador.memoria.total_size
        my = int(e.y / (h / total_actual))

        found = None
        for b in self.coordinador.memoria.mapa_memoria:
            if b["start"] <= my < b["start"] + b["size"]: 
                found = b
                break
        
        pid_ejecucion = (self.coordinador.gestor_procesos.proceso_ejecucion.pid 
                        if self.coordinador.gestor_procesos.proceso_ejecucion else None)
        
        if found:
            if found["estado"] == "OCUPADO":
                if found['pid'] == pid_ejecucion:
                    estado_text = f"⚡ EJECUTANDO | PID: P{found['pid']} | Tamaño: {found['size']} KB | Inicio: {found['start']} KB"
                    self.lbl_hover.config(text=estado_text, foreground=COLOR_TEXTO_DORADO)
                else:
                    estado_text = f"🔵 OCUPADO | PID: P{found['pid']} | Tamaño: {found['size']} KB | Inicio: {found['start']} KB"
                    self.lbl_hover.config(text=estado_text, foreground=COLOR_TEXTO_CLARO)
            else:
                estado_text = f"⚪ LIBRE | Tamaño: {found['size']} KB | Inicio: {found['start']} KB"
                self.lbl_hover.config(text=estado_text, foreground="#7a8499")
        else:
            self.lbl_hover.config(text="Pasa el mouse sobre la memoria para ver detalles", 
                                 foreground=COLOR_TEXTO_DORADO)
