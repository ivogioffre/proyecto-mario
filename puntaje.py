from datetime import datetime
from entities import Player

def guardar_record(monedas=0, tiempo_total=0, puntaje_total=0):
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
   
    # Formatear tiempo
    minutos = int(tiempo_total // 60)
    segundos = int(tiempo_total % 60)
    tiempo_formateado = f"{minutos}:{segundos:02d}"
   
    with open("Puntaje.txt", "a") as f:
        f.write(f"Fecha y hora: {fecha_hora} - Monedas: {monedas}/84 - Tiempo Total: {tiempo_formateado} - Puntaje Total: {puntaje_total}\n")

