import tkinter as tk
from tkinter import messagebox
from PIL import ImageGrab

from Horario import Horario


class InterfazHorario:
    def __init__(self, root):
        self.root = root
        self.root.title("Organizador de Horario")
        self.root.geometry("1100x700")

        self.horario = Horario()

        self.dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
        self.dia_seleccionado = "Lunes"

        self.hora_inicio = 7
        self.hora_fin = 21

        self.ancho_hora = 80
        self.ancho_dia = 150
        self.alto_hora = 50

        self.crear_interfaz()

    def crear_interfaz(self):
        frame_principal = tk.Frame(self.root)
        frame_principal.pack(fill="both", expand=True)

        panel_izquierdo = tk.Frame(frame_principal, width=220, bg="#eeeeee")
        panel_izquierdo.pack(side="left", fill="y")

        tk.Label(
            panel_izquierdo,
            text="Día de la semana",
            font=("Arial", 12, "bold"),
            bg="#eeeeee"
        ).pack(pady=10)

        for dia in self.dias:
            tk.Button(
                panel_izquierdo,
                text=dia,
                width=18,
                command=lambda d=dia: self.seleccionar_dia(d)
            ).pack(pady=4)

        tk.Label(
            panel_izquierdo,
            text="Datos del curso",
            font=("Arial", 12, "bold"),
            bg="#eeeeee"
        ).pack(pady=15)

        self.entrada_curso = self.crear_entrada(panel_izquierdo, "Nombre del curso")
        self.entrada_profesor = self.crear_entrada(panel_izquierdo, "Profesor")
        self.entrada_creditos = self.crear_entrada(panel_izquierdo, "Créditos")
        self.entrada_inicio = self.crear_entrada(panel_izquierdo, "Hora inicio")
        self.entrada_fin = self.crear_entrada(panel_izquierdo, "Hora fin")

        tk.Label(
            panel_izquierdo,
            text="Ejemplo: 7:30, 9:00, 13:00",
            bg="#eeeeee",
            font=("Arial", 9)
        ).pack(pady=5)

        tk.Button(
            panel_izquierdo,
            text="Agregar curso",
            width=18,
            bg="#90ee90",
            command=self.agregar_curso
        ).pack(pady=10)

        tk.Button(
            panel_izquierdo,
            text="Limpiar horario",
            width=18,
            bg="#ff9999",
            command=self.limpiar_horario
        ).pack(pady=10)

        tk.Button(
            panel_izquierdo,
            text="Descargar como imagen",
            width=18,
            bg="#add8e6",
            command=self.guardar_imagen
        ).pack(pady=10)

        self.label_dia = tk.Label(
            panel_izquierdo,
            text=f"Día seleccionado:\n{self.dia_seleccionado}",
            bg="#eeeeee",
            font=("Arial", 11, "bold")
        )
        self.label_dia.pack(pady=20)

        self.label_creditos = tk.Label(
            panel_izquierdo,
            text="Total de créditos: 0",
            bg="#eeeeee",
            font=("Arial", 11, "bold")
        )
        self.label_creditos.pack(pady=10)

        self.canvas = tk.Canvas(frame_principal, bg="white")
        self.canvas.pack(side="right", fill="both", expand=True)

        self.dibujar_horario()

    def crear_entrada(self, padre, texto):
        tk.Label(padre, text=texto, bg="#eeeeee").pack()
        entrada = tk.Entry(padre, width=22)
        entrada.pack(pady=4)
        return entrada

    def seleccionar_dia(self, dia):
        self.dia_seleccionado = dia
        self.label_dia.config(text=f"Día seleccionado:\n{dia}")

    def dibujar_horario(self):
        self.canvas.delete("all")

        # Encabezados de días
        for i, dia in enumerate(self.dias):
            x = self.ancho_hora + i * self.ancho_dia

            self.canvas.create_rectangle(
                x,
                0,
                x + self.ancho_dia,
                self.alto_hora,
                fill="#d9eaff",
                outline="black"
            )

            self.canvas.create_text(
                x + self.ancho_dia / 2,
                self.alto_hora / 2,
                text=dia,
                font=("Arial", 10, "bold")
            )

        # Filas de horas
        for hora in range(self.hora_inicio, self.hora_fin + 1):
            y = self.alto_hora + (hora - self.hora_inicio) * self.alto_hora

            self.canvas.create_rectangle(
                0,
                y,
                self.ancho_hora,
                y + self.alto_hora,
                fill="#f0f0f0",
                outline="black"
            )

            self.canvas.create_text(
                self.ancho_hora / 2,
                y + self.alto_hora / 2,
                text=f"{hora}:00",
                font=("Arial", 9)
            )

            self.canvas.create_line(
                self.ancho_hora,
                y,
                self.ancho_hora + len(self.dias) * self.ancho_dia,
                y,
                fill="gray"
            )

        # Líneas verticales
        for i in range(len(self.dias) + 1):
            x = self.ancho_hora + i * self.ancho_dia

            self.canvas.create_line(
                x,
                0,
                x,
                self.alto_hora + (self.hora_fin - self.hora_inicio + 1) * self.alto_hora,
                fill="gray"
            )

        self.dibujar_cursos()

    def dibujar_cursos(self):
        for curso in self.horario.obtener_cursos():
            indice_dia = self.dias.index(curso.dia)

            x1 = self.ancho_hora + indice_dia * self.ancho_dia + 5
            x2 = x1 + self.ancho_dia - 10

            minutos_inicio_dia = self.hora_inicio * 60

            y1 = (
                self.alto_hora
                + ((curso.inicio_minutos - minutos_inicio_dia) / 60) * self.alto_hora
                + 5
            )

            y2 = (
                self.alto_hora
                + ((curso.fin_minutos - minutos_inicio_dia) / 60) * self.alto_hora
                - 5
            )

            self.canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill="#b6f2c2",
                outline="black",
                width=2
            )

            self.canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                text=curso.obtener_texto(),
                font=("Arial", 9),
                width=self.ancho_dia - 15
            )

    def agregar_curso(self):
        nombre = self.entrada_curso.get()
        profesor = self.entrada_profesor.get()
        creditos = self.entrada_creditos.get()
        inicio = self.entrada_inicio.get()
        fin = self.entrada_fin.get()

        try:
            self.horario.agregar_curso(
                nombre,
                profesor,
                creditos,
                self.dia_seleccionado,
                inicio,
                fin
            )

            self.dibujar_horario()
            self.actualizar_total_creditos()
            self.limpiar_campos()

        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def actualizar_total_creditos(self):
        total = self.horario.obtener_total_creditos()
        self.label_creditos.config(text=f"Total de créditos: {total}")

    def limpiar_campos(self):
        self.entrada_curso.delete(0, tk.END)
        self.entrada_profesor.delete(0, tk.END)
        self.entrada_creditos.delete(0, tk.END)
        self.entrada_inicio.delete(0, tk.END)
        self.entrada_fin.delete(0, tk.END)

    def limpiar_horario(self):
        respuesta = messagebox.askyesno(
            "Limpiar horario",
            "¿Está seguro de que desea limpiar todo el horario?"
        )

        if respuesta:
            self.horario.limpiar_horario()
            self.dibujar_horario()
            self.actualizar_total_creditos()

    def guardar_imagen(self):
        try:
            x = self.root.winfo_rootx() + self.canvas.winfo_x()
            y = self.root.winfo_rooty() + self.canvas.winfo_y()
            x2 = x + self.canvas.winfo_width()
            y2 = y + self.canvas.winfo_height()

            imagen = ImageGrab.grab(bbox=(x, y, x2, y2))
            imagen.save("horario.png")

            messagebox.showinfo(
                "Imagen guardada",
                "El horario fue guardado como horario.png"
            )

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"No se pudo guardar la imagen.\n{error}"
            )