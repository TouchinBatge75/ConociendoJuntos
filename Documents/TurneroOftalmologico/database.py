# database.py
import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('turnos.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    
    # Tabla de doctores
    conn.execute('''
        CREATE TABLE IF NOT EXISTS doctores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            especialidad TEXT,
            activo BOOLEAN DEFAULT 0,
            disponible BOOLEAN DEFAULT 1
        )
    ''')
    
    # Tabla de estaciones
    conn.execute('''
        CREATE TABLE IF NOT EXISTS estaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            descripcion TEXT
        )
    ''')
    
    # Tabla de turnos
    conn.execute('''
        CREATE TABLE IF NOT EXISTS turnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero TEXT NOT NULL,
            paciente_nombre TEXT NOT NULL,
            paciente_edad INTEGER,
            tipo TEXT DEFAULT 'CITA',  -- CITA o SIN_CITA
            estado TEXT DEFAULT 'PENDIENTE',  -- PENDIENTE, EN_ATENCION, COMPLETADO, FINALIZADO
            estacion_actual INTEGER,
            estacion_siguiente INTEGER,
            doctor_asignado INTEGER,
            prioridad INTEGER DEFAULT 1,
            timestamp_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            timestamp_atencion DATETIME,
            FOREIGN KEY (estacion_actual) REFERENCES estaciones (id),
            FOREIGN KEY (estacion_siguiente) REFERENCES estaciones (id),
            FOREIGN KEY (doctor_asignado) REFERENCES doctores (id)
        )
    ''')
    
    # Insertar estaciones básicas
    estaciones = [
        ('Recepción', 'Punto de entrada y salida del paciente'),
        ('Trabajo Social', 'Atención social para pacientes sin cita, asi como para agendar operaciones'),
        ('Toma de Calculos Correspondientes', 'Medición de agudeza visual, Presion Intraocular, Queratometria, Tonometria, Calculo de LIO, Refraccion'),
        ('Consulta Médica', 'Consulta con el medico asignado'),
        ('Farmacia', 'Entrega de medicamentos'),
        ('Asesoria Visual', 'Orientación sobre lentes'),
        ('Estudios Especiales', 'Exámenes especializados'),
        ('Salida', 'Final del proceso')
    ]
    
    conn.executemany(
        'INSERT OR IGNORE INTO estaciones (nombre, descripcion) VALUES (?, ?)',
        estaciones
    )
    
    # Insertar doctores
    doctores = [
        ('Dr. Ricardo', 'Consultorio 1', 1),
        ('Dra. Tania', 'Consultorio 2', 1),
        ('Dr. Julio', 'Consultorio 3', 1),
        ('Dr. Eduardo', 'Consultorio 4', 1),
        ('Dr. Eric', 'Especialista', 0),  # Inactivo por defecto
        ('Medico Internista', 'Consultorio', 0),  # Inactivo por defecto
        ('Dra. Carolina', 'Especialista', 0),  # Inactivo por defecto
    ]
    
    conn.executemany(
        'INSERT OR IGNORE INTO doctores (nombre, especialidad, activo) VALUES (?, ?, ?)',
        doctores
    )
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Base de datos inicializada correctamente!")