from Curso import Curso
from Horario import Horario
import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser


class InterfazHorario:
    def __init__(self, root):
        self.root = root
        self.root.title("Organizador de Horario")
        self.root.geometry("1100x700")

        self.horario = Horario()

        self.dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]
        self.dias_seleccionados = {}

        self.hora_inicio = 7
        self.hora_fin = 21

        self.ancho_hora = 80
        self.ancho_dia = 150
        self.alto_hora = 50

        self.color_curso = "#A7C7E7"

        self.crear_interfaz()

    def crear_interfaz(self):
        frame_principal = tk.Frame(self.root)
        frame_principal.pack(fill="both", expand=True)

        frame_formulario = tk.Frame(frame_principal, padx=10, pady=10)
        frame_formulario.pack(side="left", fill="y")

        frame_horario = tk.Frame(frame_principal)
        frame_horario.pack(side="right", fill="both", expand=True)
        
        self.boton_color = tk.Button(
            frame_formulario,
            text="Elegir color",
            command=self.elegir_color_curso,
            bg=self.color_curso,
            width=22
        )

        tk.Label(frame_formulario, text="Agregar curso", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Label(frame_formulario, text="Nombre del curso").pack(anchor="w")
        self.entry_nombre = tk.Entry(frame_formulario, width=30)
        self.entry_nombre.pack(pady=5)

        tk.Label(frame_formulario, text="Profesor").pack(anchor="w")
        self.entry_profesor = tk.Entry(frame_formulario, width=30)
        self.entry_profesor.pack(pady=5)

        tk.Label(frame_formulario, text="Créditos").pack(anchor="w")
        self.entry_creditos = tk.Entry(frame_formulario, width=30)
        self.entry_creditos.pack(pady=5)

        tk.Label(frame_formulario, text="Hora inicio").pack(anchor="w")
        self.entry_hora_inicio = tk.Entry(frame_formulario, width=30)
        self.entry_hora_inicio.insert(0, "7:00")
        self.entry_hora_inicio.pack(pady=5)

        tk.Label(frame_formulario, text="Hora final").pack(anchor="w")
        self.entry_hora_fin = tk.Entry(frame_formulario, width=30)
        self.entry_hora_fin.insert(0, "9:00")
        self.entry_hora_fin.pack(pady=5)

        tk.Label(frame_formulario, text="Días").pack(anchor="w", pady=(10, 0))
        tk.Label(frame_formulario, text="Color del curso").pack(anchor="w", pady=(10, 0))

        self.boton_color.pack(pady=5)
        for dia in self.dias:
            variable = tk.BooleanVar()
            tk.Checkbutton(frame_formulario, text=dia, variable=variable).pack(anchor="w")
            self.dias_seleccionados[dia] = variable

        tk.Button(
            frame_formulario,
            text="Agregar curso",
            command=self.agregar_curso_desde_interfaz,
            bg="#4CAF50",
            fg="white",
            width=22
        ).pack(pady=12)

        tk.Button(
            frame_formulario,
            text="Limpiar horario",
            command=self.limpiar_horario_interfaz,
            bg="#D9534F",
            fg="white",
            width=22
        ).pack(pady=5)
        tk.Button(
            frame_formulario,
            text="Guardar como imagen",
            command=self.guardar_horario_como_imagen,
            bg="#0275D8",
            fg="white",
            width=22
        ).pack(pady=5)

        self.label_creditos = tk.Label(
            frame_formulario,
            text="Total de créditos: 0",
            font=("Arial", 12, "bold")
        )
        self.label_creditos.pack(pady=20)

        self.canvas = tk.Canvas(frame_horario, bg="white")
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar_y = tk.Scrollbar(frame_horario, orient="vertical", command=self.canvas.yview)
        scrollbar_y.pack(side="right", fill="y")

        scrollbar_x = tk.Scrollbar(frame_principal, orient="horizontal", command=self.canvas.xview)
        scrollbar_x.pack(side="bottom", fill="x")

        self.canvas.configure(
            yscrollcommand=scrollbar_y.set,
            xscrollcommand=scrollbar_x.set
        )

        self.dibujar_horario()

    def convertir_hora_a_minutos(self, hora):
        try:
            partes = hora.split(":")
            if len(partes) != 2:
                raise ValueError

            horas = int(partes[0])
            minutos = int(partes[1])

        except ValueError:
            raise ValueError("La hora debe tener el formato HH:MM. Ejemplo: 7:30 o 13:00.")

        if horas < 0 or horas > 23:
            raise ValueError("La hora debe estar entre 0 y 23.")

        if minutos < 0 or minutos > 59:
            raise ValueError("Los minutos deben estar entre 00 y 59.")

        return horas * 60 + minutos

    def agregar_curso(self, nombre, profesor, creditos, dias, hora_inicio, hora_fin):
        if not nombre or not profesor or not creditos or not hora_inicio or not hora_fin:
            raise ValueError("Debe llenar todos los campos.")

        if not dias:
            raise ValueError("Debe seleccionar al menos un día.")

        try:
            creditos = int(creditos)
        except ValueError:
            raise ValueError("Los créditos deben ser un número.")

        if creditos <= 0:
            raise ValueError("Los créditos deben ser mayores a cero.")

        inicio_minutos = self.convertir_hora_a_minutos(hora_inicio)
        fin_minutos = self.convertir_hora_a_minutos(hora_fin)

        if inicio_minutos >= fin_minutos:
            raise ValueError("La hora de inicio debe ser menor que la hora final.")

        if inicio_minutos < 7 * 60 or fin_minutos > 21 * 60:
            raise ValueError("El horario permitido es de 7:00 a 21:00.")

        for dia in dias:
            if self.existe_choque(dia, inicio_minutos, fin_minutos):
                raise ValueError(f"Ya existe un curso en ese horario el día {dia}.")

        for dia in dias:
            curso = curso = Curso(nombre, profesor, creditos, dia, hora_inicio, hora_fin, self.color_curso)
            curso.inicio_minutos = inicio_minutos
            curso.fin_minutos = fin_minutos
            self.horario.agregar_curso(curso)

    def existe_choque(self, dia, inicio_minutos, fin_minutos):
        for curso in self.horario.obtener_cursos():
            if curso.dia == dia:
                if inicio_minutos < curso.fin_minutos and fin_minutos > curso.inicio_minutos:
                    return True
        return False
    def elegir_color_curso(self):
        color = colorchooser.askcolor(title="Elegir color del curso")

        if color[1]:
            self.color_curso = color[1]
            self.boton_color.config(bg=self.color_curso)
    def dibujar_horario(self):
        self.canvas.delete("all")

        x_inicio = self.ancho_hora
        y_inicio = 40

        ancho_total = self.ancho_hora + len(self.dias) * self.ancho_dia
        alto_total = y_inicio + (self.hora_fin - self.hora_inicio) * self.alto_hora

        self.canvas.config(scrollregion=(0, 0, ancho_total, alto_total))

        for i, dia in enumerate(self.dias):
            x = x_inicio + i * self.ancho_dia
            self.canvas.create_rectangle(x, 0, x + self.ancho_dia, y_inicio, fill="#E6E6E6", outline="black")
            self.canvas.create_text(x + self.ancho_dia / 2, y_inicio / 2, text=dia, font=("Arial", 10, "bold"))

        for hora in range(self.hora_inicio, self.hora_fin + 1):
            y = y_inicio + (hora - self.hora_inicio) * self.alto_hora
            self.canvas.create_text(self.ancho_hora / 2, y, text=f"{hora}:00", font=("Arial", 9))
            self.canvas.create_line(x_inicio, y, ancho_total, y, fill="#CCCCCC")

        for i in range(len(self.dias) + 1):
            x = x_inicio + i * self.ancho_dia
            self.canvas.create_line(x, y_inicio, x, alto_total, fill="#CCCCCC")

        self.dibujar_cursos()

    def dibujar_cursos(self):
        for i, curso in enumerate(self.horario.obtener_cursos()):
            indice_dia = self.dias.index(curso.dia)

            x1 = self.ancho_hora + indice_dia * self.ancho_dia
            x2 = x1 + self.ancho_dia

            minutos_desde_inicio = curso.inicio_minutos - self.hora_inicio * 60
            duracion = curso.fin_minutos - curso.inicio_minutos

            y1 = 40 + (minutos_desde_inicio / 60) * self.alto_hora
            y2 = y1 + (duracion / 60) * self.alto_hora

            color = curso.color

            self.canvas.create_rectangle(x1 + 3, y1 + 3, x2 - 3, y2 - 3, fill=color, outline="black")

            texto = f"{curso.nombre}\n{curso.profesor}\n{curso.creditos} créditos"

            self.canvas.create_text(
                (x1 + x2) / 2,
                (y1 + y2) / 2,
                text=texto,
                font=("Arial", 9),
                width=self.ancho_dia - 10
            )

    def agregar_curso_desde_interfaz(self):
        nombre = self.entry_nombre.get()
        profesor = self.entry_profesor.get()
        creditos = self.entry_creditos.get()
        hora_inicio = self.entry_hora_inicio.get()
        hora_fin = self.entry_hora_fin.get()

        dias = []

        for dia, variable in self.dias_seleccionados.items():
            if variable.get():
                dias.append(dia)

        try:
            self.agregar_curso(nombre, profesor, creditos, dias, hora_inicio, hora_fin)
            self.dibujar_horario()
            self.actualizar_total_creditos()
            self.limpiar_campos()
            messagebox.showinfo("Curso agregado", "El curso se agregó correctamente.")

        except ValueError as error:
            messagebox.showerror("Error", str(error))

    def limpiar_campos(self):
        self.entry_nombre.delete(0, tk.END)
        self.entry_profesor.delete(0, tk.END)
        self.entry_creditos.delete(0, tk.END)
        self.entry_hora_inicio.delete(0, tk.END)
        self.entry_hora_fin.delete(0, tk.END)

        self.entry_hora_inicio.insert(0, "7:00")
        self.entry_hora_fin.insert(0, "9:00")

        for variable in self.dias_seleccionados.values():
            variable.set(False)

    def actualizar_total_creditos(self):
        total = self.horario.obtener_total_creditos()
        self.label_creditos.config(text=f"Total de créditos: {total}")

    def limpiar_horario_interfaz(self):
        self.horario.limpiar_horario()
        self.dibujar_horario()
        self.actualizar_total_creditos()
        messagebox.showinfo("Horario limpio", "El horario se limpió correctamente.")

    def guardar_horario_como_imagen(self):
        archivo = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("Imagen PNG", "*.png")]
        )

        if not archivo:
            return

        try:
            from PIL import ImageGrab
        except ImportError:
            messagebox.showerror("Error", "Debe instalar Pillow con: pip install pillow")
            return

        self.root.update_idletasks()

        x = self.canvas.winfo_rootx()
        y = self.canvas.winfo_rooty()
        ancho = self.canvas.winfo_width()
        alto = self.canvas.winfo_height()

        imagen = ImageGrab.grab(bbox=(x, y, x + ancho, y + alto))
        imagen.save(archivo)

        messagebox.showinfo("Guardado", "El horario se guardó correctamente.")