from datetime import datetime


def guardar_record(monedas):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")# Obtiene la fecha y hora del momento exacto en que se guarda el record
    with open("Puntaje.txt", "a") as f:
        f.write(f" Fecha y hora : {fecha_hora} - Monedas Obtenidas: {monedas}/ 42  \n")
