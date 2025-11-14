# ver_estaciones.py
import sqlite3

def ver_estaciones():
    conn = sqlite3.connect('turnos.db')
    cursor = conn.cursor()
    
    print("📋 ESTACIONES EN LA BASE DE DATOS:")
    print("ID | Nombre")
    print("-" * 40)
    
    cursor.execute("SELECT id, nombre FROM estaciones ORDER BY id")
    estaciones = cursor.fetchall()
    
    for estacion in estaciones:
        print(f"{estacion[0]:2} | {estacion[1]}")
    
    conn.close()

if __name__ == '__main__':
    ver_estaciones()