class Horario:
    def __init__(self):
        self.cursos = []

    def agregar_curso(self, curso):
        self.cursos.append(curso)

    def obtener_cursos(self):
        return self.cursos

    def limpiar_horario(self):
        self.cursos.clear()

    def obtener_total_creditos(self):
        total = 0

        cursos_contados = []

        for curso in self.cursos:
            clave = (curso.nombre, curso.profesor, curso.creditos)

            if clave not in cursos_contados:
                total += curso.creditos
                cursos_contados.append(clave)

        return total