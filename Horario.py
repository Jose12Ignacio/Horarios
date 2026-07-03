from Curso import Curso


class Horario:
    def __init__(self):
        self.cursos = []

    def convertir_hora_a_minutos(self, hora):
        try:
            partes = hora.split(":")

            if len(partes) != 2:
                raise ValueError

            horas = int(partes[0])
            minutos = int(partes[1])

        except ValueError:
            raise ValueError(
                "La hora debe tener el formato HH:MM. Ejemplo: 7:30 o 13:00."
            )

        if horas < 0 or horas > 23:
            raise ValueError("La hora debe estar entre 0 y 23.")

        if minutos < 0 or minutos > 59:
            raise ValueError("Los minutos deben estar entre 00 y 59.")

        return horas * 60 + minutos

    def agregar_curso(self, nombre, profesor, creditos, dia, hora_inicio, hora_fin):
        if not nombre or not profesor or not creditos or not hora_inicio or not hora_fin:
            raise ValueError("Debe llenar todos los campos.")

        try:
            creditos = int(creditos)
        except ValueError:
            raise ValueError("Los créditos deben ser un número.")

        if creditos <= 0:
            raise ValueError("Los créditos deben ser mayores a cero.")

        inicio_minutos = self.convertir_hora_a_minutos(hora_inicio)
        fin_minutos = self.convertir_hora_a_minutos(hora_fin)

        limite_inicio = 7 * 60
        limite_fin = 21 * 60

        if inicio_minutos >= fin_minutos:
            raise ValueError("La hora de inicio debe ser menor que la hora final.")

        if inicio_minutos < limite_inicio or fin_minutos > limite_fin:
            raise ValueError("El horario permitido es de 7:00 a 21:00.")

        if self.existe_choque(dia, inicio_minutos, fin_minutos):
            raise ValueError("Ya existe un curso en ese horario.")

        curso = Curso(nombre, profesor, creditos, dia, hora_inicio, hora_fin)
        curso.inicio_minutos = inicio_minutos
        curso.fin_minutos = fin_minutos

        self.cursos.append(curso)

    def existe_choque(self, dia, inicio_minutos, fin_minutos):
        for curso in self.cursos:
            if curso.dia == dia:
                if inicio_minutos < curso.fin_minutos and fin_minutos > curso.inicio_minutos:
                    return True

        return False

    def obtener_cursos(self):
        return self.cursos

    def obtener_total_creditos(self):
        total = 0

        for curso in self.cursos:
            total += curso.creditos

        return total

    def limpiar_horario(self):
        self.cursos.clear()