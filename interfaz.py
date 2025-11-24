import customtkinter as ctk
import json
import os


# =====================================================
# CONFIGURACIÓN TEMA ARCH LINUX (CORREGIDO)
# =====================================================

ctk.set_appearance_mode("dark")     # Modo oscuro
ctk.set_default_color_theme("blue") # Tema base, lo modificamos manualmente

# Colores del estilo Arch Linux
ARCH_BG = "#1a1a1a"
ARCH_PANEL = "#141414"
ARCH_BORDER = "#1793d1"
ARCH_TEXT = "#e6e6e6"
ARCH_BLUE = "#1793d1"
ARCH_BLUE_HOVER = "#0f80b8"



# =====================================================
# CLASE PRINCIPAL
# =====================================================
class SistemaOperativoUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Arch Linux System Monitor – Simulador SO")
        self.geometry("1250x750")
        self.configure(bg=ARCH_BG)

        self.crear_layout()
        self.after(1000, self.actualizar_estado)


    # =====================================================
    def crear_layout(self):

        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # --------------------------------------------------
        # PROCESOS
        # --------------------------------------------------
        self.panel_procesos = ctk.CTkFrame(self, fg_color=ARCH_PANEL)
        self.panel_procesos.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.label_proc = ctk.CTkLabel(
            self.panel_procesos,
            text="PROCESOS",
            text_color=ARCH_TEXT,
            font=("JetBrains Mono", 18, "bold")
        )
        self.label_proc.pack(pady=8)

        self.lista_procesos = ctk.CTkTextbox(
            self.panel_procesos,
            height=200,
            fg_color="#111111",
            text_color=ARCH_TEXT,
            border_color=ARCH_BLUE,
            border_width=1,
            corner_radius=6
        )
        self.lista_procesos.pack(fill="both", expand=True, padx=10, pady=10)


        # --------------------------------------------------
        # COLAS
        # --------------------------------------------------
        self.panel_colas = ctk.CTkFrame(self, fg_color=ARCH_PANEL)
        self.panel_colas.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.label_colas = ctk.CTkLabel(
            self.panel_colas,
            text="COLAS (Listos / Bloqueados / E/S)",
            text_color=ARCH_TEXT,
            font=("JetBrains Mono", 18, "bold")
        )
        self.label_colas.pack(pady=8)

        self.colas_box = ctk.CTkTextbox(
            self.panel_colas,
            height=200,
            fg_color="#111111",
            text_color=ARCH_TEXT,
            border_color=ARCH_BLUE,
            border_width=1,
            corner_radius=6
        )
        self.colas_box.pack(fill="both", expand=True, padx=10, pady=10)


        # --------------------------------------------------
        # PCB
        # --------------------------------------------------
        self.panel_pcb = ctk.CTkFrame(self, fg_color=ARCH_PANEL)
        self.panel_pcb.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)

        self.label_pcb = ctk.CTkLabel(
            self.panel_pcb,
            text="PCB – Proceso en Ejecución",
            text_color=ARCH_TEXT,
            font=("JetBrains Mono", 18, "bold")
        )
        self.label_pcb.pack(pady=8)

        self.pcb_box = ctk.CTkTextbox(
            self.panel_pcb,
            height=200,
            fg_color="#111111",
            text_color=ARCH_TEXT,
            border_color=ARCH_BLUE,
            border_width=1,
            corner_radius=6
        )
        self.pcb_box.pack(fill="both", expand=True, padx=10, pady=10)


        # --------------------------------------------------
        # MEMORIA
        # --------------------------------------------------
        self.panel_memoria = ctk.CTkFrame(self, fg_color=ARCH_PANEL)
        self.panel_memoria.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        self.label_mem = ctk.CTkLabel(
            self.panel_memoria,
            text="MEMORIA SEGMENTADA",
            text_color=ARCH_TEXT,
            font=("JetBrains Mono", 18, "bold")
        )
        self.label_mem.pack(pady=8)

        self.mem_box = ctk.CTkTextbox(
            self.panel_memoria,
            height=150,
            fg_color="#111111",
            text_color=ARCH_TEXT,
            border_color=ARCH_BLUE,
            border_width=1,
            corner_radius=6
        )
        self.mem_box.pack(fill="both", expand=True, padx=10, pady=10)


        # --------------------------------------------------
        # LOGS
        # --------------------------------------------------
        self.panel_logs = ctk.CTkFrame(self, fg_color=ARCH_PANEL)
        self.panel_logs.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)

        self.label_logs = ctk.CTkLabel(
            self.panel_logs,
            text="LOGS DEL SISTEMA",
            text_color=ARCH_TEXT,
            font=("JetBrains Mono", 18, "bold")
        )
        self.label_logs.pack(pady=8)

        self.logs_box = ctk.CTkTextbox(
            self.panel_logs,
            height=150,
            fg_color="#111111",
            text_color=ARCH_TEXT,
            border_color=ARCH_BLUE,
            border_width=1,
            corner_radius=6
        )
        self.logs_box.pack(fill="both", expand=True, padx=10, pady=10)


    # =====================================================
    def actualizar_estado(self):
        try:
            with open("estado.json", "r") as f:
                contenido = f.read()

            if not contenido.strip():
                print("[WARN] estado.json vacío, reintentando…")
                raise ValueError("Archivo vacío")

            data = json.loads(contenido)

            # Si llegó aquí, todo OK
            self.mostrar_datos(data)

        except Exception as e:
            print(f"[ERROR leyendo JSON]: {e}")

        finally:
            self.after(500, self.actualizar_estado)


    # =====================================================
    def mostrar_datos(self, data):

        # Procesos
        self.lista_procesos.delete("0.0", "end")
        for p in data.get("procesos", []):
            self.lista_procesos.insert(
                "end",
                f"PID: {p['pid']} | {p['estado']} | Burst={p['burst']} | Pri={p['prioridad']}\n"
            )

        
        # Colas
        self.colas_box.delete("0.0", "end")
        self.colas_box.insert("end", "Listos:\n")
        for pid in data.get("cola_listos", []):
            self.colas_box.insert("end", f"  → {pid}\n")

        self.colas_box.insert("end", "\nBloqueados:\n")
        for pid in data.get("cola_bloqueados", []):
            self.colas_box.insert("end", f"  → {pid}\n")

        self.colas_box.insert("end", "\nE/S:\n")
        for pid in data.get("cola_es", []):
            self.colas_box.insert("end", f"  → {pid}\n")

        # PCB
        self.pcb_box.delete("0.0", "end")
        if "pcb" in data:
            for k, v in data["pcb"].items():
                self.pcb_box.insert("end", f"{k}: {v}\n")

        # Memoria
        self.mem_box.delete("0.0", "end")
        for bloque in data.get("memoria", []):
            self.mem_box.insert(
                "end",
                f"[Bloque {bloque['id']}] Inicio={bloque['inicio']} | Tam={bloque['tam']} | Proceso={bloque['proceso']}\n"
            )

        # Logs
        for log in data.get("logs", []):
            self.logs_box.insert("end", f"{log}\n")



if __name__ == "__main__":
    app = SistemaOperativoUI()
    app.mainloop()
