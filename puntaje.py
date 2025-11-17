from datetime import datetime
from puntaje_nivel import puntajes_acumulados

def guardar_record(monedas):
    """
    Guarda el récord del juego completo con todos los detalles de puntaje.
    """
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Calcular totales desde puntajes_acumulados
    total_puntos = sum(v.get("puntos_nivel", 0) + v.get("bonus_tiempo", 0) 
                       for v in puntajes_acumulados.values())
    total_monedas = sum(v.get("monedas", 0) for v in puntajes_acumulados.values())
    total_tiempo = sum(v.get("tiempo_total", 0) for v in puntajes_acumulados.values())
    total_enemigos = sum(v.get("puntos_por_enemigos", 0) for v in puntajes_acumulados.values())
    
    # Calcular minutos y segundos
    minutos = int(total_tiempo // 60)
    segundos = int(total_tiempo % 60)
    
    # Guardar con formato detallado
    with open("Puntaje.txt", "a", encoding="utf-8") as f:
        f.write(f"Fecha y hora: {fecha_hora} - ")
        f.write(f"Monedas Obtenidas: {total_monedas}/84 - ")
        f.write(f"Puntos Totales: {total_puntos} - ")
        f.write(f"Tiempo: {minutos}:{segundos:02d} - ")
        f.write(f"Puntos por Enemigos: {total_enemigos}\n")