class Curso:
    def __init__(self, nombre, profesor, creditos, dia, hora_inicio, hora_fin):
        self.nombre = nombre
        self.profesor = profesor
        self.creditos = creditos
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin

        # Se llenan desde Horario.py
        self.inicio_minutos = 0
        self.fin_minutos = 0

    def obtener_texto(self):
        return (
            f"{self.nombre}\n"
            f"Prof: {self.profesor}\n"
            f"Créditos: {self.creditos}\n"
            f"{self.hora_inicio} - {self.hora_fin}"
        )