# limpiar_turnos.py
import sqlite3

def limpiar_turnos():
    try:
        conn = sqlite3.connect('turnos.db')
        cursor = conn.cursor()
        
        print("=" * 50)
        print("🧹 LIMPIADOR DE TURNOS - TURNERO OFTALMOLÓGICO")
        print("=" * 50)
        
        # Contar turnos antes de limpiar
        cursor.execute("SELECT COUNT(*) FROM turnos")
        total_turnos = cursor.fetchone()[0]
        
        print(f"📊 Turnos existentes: {total_turnos}")
        
        if total_turnos == 0:
            print("✅ No hay turnos para limpiar")
            conn.close()
            return
        
        # Mostrar turnos que se van a eliminar
        print("\n🎯 TURNOS QUE SE ELIMINARÁN:")
        print("-" * 40)
        cursor.execute("SELECT id, numero, paciente_nombre FROM turnos")
        turnos = cursor.fetchall()
        
        for turno in turnos:
            print(f"   #{turno[0]} - {turno[1]} - {turno[2]}")
        
        # Confirmar eliminación
        print(f"\n⚠️  ¿Estás seguro de que quieres eliminar {total_turnos} turnos?")
        confirmacion = input("   Escribe 'SI' para confirmar: ")
        
        if confirmacion.upper() == 'SI':
            # Eliminar todos los turnos
            cursor.execute("DELETE FROM turnos")
            
            # Reiniciar el contador de IDs (opcional pero recomendado)
            cursor.execute("DELETE FROM sqlite_sequence WHERE name='turnos'")
            
            conn.commit()
            conn.close()
            
            print("✅ ¡TODOS LOS TURNOS HAN SIDO ELIMINADOS!")
            print("💡 La base de datos está lista para nuevos turnos")
            
        else:
            conn.close()
            print("❌ Operación cancelada - Los turnos se mantienen")
            
    except sqlite3.OperationalError as e:
        print(f"❌ Error: {e}")
        print("💡 Sugerencia: ¿Tienes Flask ejecutándose? Detenlo con Ctrl+C")

def ver_turnos_actuales():
    """Función para ver los turnos actuales"""
    try:
        conn = sqlite3.connect('turnos.db')
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM turnos")
        total = cursor.fetchone()[0]
        
        print(f"\n📈 ESTADO ACTUAL: {total} turnos en la base de datos")
        
        if total > 0:
            cursor.execute("SELECT id, numero, paciente_nombre, estado FROM turnos")
            turnos = cursor.fetchall()
            
            print("🎫 TURNOS ACTUALES:")
            for turno in turnos:
                print(f"   #{turno[0]} - {turno[1]} - {turno[2]} - Estado: {turno[3]}")
        
        conn.close()
        
    except sqlite3.OperationalError:
        print("   (No se pudo verificar el estado actual)")

if __name__ == '__main__':
    # Mostrar estado actual primero
    ver_turnos_actuales()
    
    # Preguntar si quieres limpiar
    print("\n" + "=" * 50)
    opcion = input("¿Quieres limpiar todos los turnos? (s/n): ")
    
    if opcion.lower() in ['s', 'si', 'y', 'yes']:
        limpiar_turnos()
    else:
        print("❌ Operación cancelada")
    
    # Mostrar estado final
    print("\n" + "=" * 50)
    ver_turnos_actuales()