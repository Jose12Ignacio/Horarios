import tkinter as tk
from interfaz import InterfazHorario


def main():
    ventana = tk.Tk()
    app = InterfazHorario(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    main()