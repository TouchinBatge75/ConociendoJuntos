# ver_bd.py
import sqlite3
from datetime import datetime

def ver_base_datos():
    try:
        conn = sqlite3.connect('turnos.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        print("=" * 50)
        print("📊 VISOR DE BASE DE DATOS - TURNERO OFTALMOLÓGICO")
        print("=" * 50)
        
        # Ver todas las tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tablas = cursor.fetchall()
        
        for tabla in tablas:
            nombre_tabla = tabla['name']
            print(f"\n🎯 TABLA: {nombre_tabla.upper()}")
            print("-" * 30)
            
            # Ver contenido de cada tabla
            cursor.execute(f"SELECT * FROM {nombre_tabla}")
            filas = cursor.fetchall()
            
            if not filas:
                print("   (vacía)")
                continue
                
            # Mostrar columnas
            columnas = [desc[0] for desc in cursor.description]
            print(f"   Columnas: {', '.join(columnas)}")
            
            # Mostrar datos
            for i, fila in enumerate(filas, 1):
                print(f"   {i}. {dict(fila)}")
        
        conn.close()
        print("\n" + "=" * 50)
        print("✅ Base de datos leída correctamente")
        
    except sqlite3.OperationalError as e:
        print(f"❌ Error: {e}")
        print("💡 Sugerencia: ¿Tienes Flask ejecutándose? Detenlo con Ctrl+C")

if __name__ == '__main__':
    ver_base_datos()