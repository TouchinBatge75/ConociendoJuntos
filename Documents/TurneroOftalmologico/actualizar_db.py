# actualizar_db.py
import sqlite3

def actualizar_base_datos():
    conn = sqlite3.connect('turnos.db')
    
    try:
        # Crear tabla historial_turnos si no existe
        conn.execute('''
            CREATE TABLE IF NOT EXISTS historial_turnos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                turno_id INTEGER NOT NULL,
                accion TEXT NOT NULL,
                detalles TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                usuario TEXT DEFAULT 'sistema',
                FOREIGN KEY (turno_id) REFERENCES turnos (id)
            )
        ''')
        
        # Agregar campos para estadísticas si no existen
        try:
            conn.execute('ALTER TABLE turnos ADD COLUMN timestamp_cancelado DATETIME')
            print("✅ timestamp_cancelado agregado")
        except sqlite3.OperationalError:
            print("ℹ️ timestamp_cancelado ya existe")
            
        try:
            conn.execute('ALTER TABLE turnos ADD COLUMN razon_cancelacion TEXT')
            print("✅ razon_cancelacion agregado")
        except sqlite3.OperationalError:
            print("ℹ️ razon_cancelacion ya existe")
            
        try:
            conn.execute('ALTER TABLE turnos ADD COLUMN tiempo_total INTEGER')
            print("✅ tiempo_total agregado")
        except sqlite3.OperationalError:
            print("ℹ️ tiempo_total ya existe")
        
        conn.commit()
        print("✅ Base de datos actualizada correctamente")
        
        # Verificar estructura de la tabla turnos
        print("\n📋 Estructura de la tabla 'turnos':")
        cursor = conn.execute("PRAGMA table_info(turnos)")
        for col in cursor.fetchall():
            print(f"  - {col[1]} ({col[2]})")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
        
    finally:
        conn.close()

if __name__ == '__main__':
    actualizar_base_datos()