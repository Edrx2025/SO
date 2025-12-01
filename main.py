"""
Archivo Principal del Simulador del Sistema Operativo
Integra todos los módulos y ejecuta la aplicación
"""

import tkinter as tk
from interfaz import SimuladorApp


if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorApp(root)
    root.mainloop()

