# app.py
from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Función para conexión a BD
def get_db_connection():
    conn = sqlite3.connect('turnos.db')
    conn.row_factory = sqlite3.Row
    return conn

# Ruta principal - Recepción
@app.route('/')
def recepcion():
    return render_template('recepcion.html')

# API: Obtener todos los turnos activos
@app.route('/api/turnos')
def get_turnos():
    conn = get_db_connection()
    turnos = conn.execute('''
        SELECT t.*, 
               e_actual.nombre as estacion_actual_nombre, 
               e_siguiente.nombre as estacion_siguiente_nombre,
               d.nombre as doctor_nombre
        FROM turnos t
        LEFT JOIN estaciones e_actual ON t.estacion_actual = e_actual.id
        LEFT JOIN estaciones e_siguiente ON t.estacion_siguiente = e_siguiente.id
        LEFT JOIN doctores d ON t.doctor_asignado = d.id
        WHERE t.estado != "FINALIZADO" AND t.estado != "CANCELADO"
        ORDER BY t.timestamp_creacion DESC
    ''').fetchall()
    conn.close()
    
    turnos_list = []
    for turno in turnos:
        turnos_list.append(dict(turno))
    
    return jsonify(turnos_list)

# API: Obtener doctores activos
@app.route('/api/doctores')
def get_doctores():
    conn = get_db_connection()
    doctores = conn.execute('''
        SELECT * FROM doctores WHERE activo = 1
    ''').fetchall()
    conn.close()
    return jsonify([dict(d) for d in doctores])

# API: Obtener estaciones (¡MOVIDO ARRIBA!)
@app.route('/api/estaciones')
def get_estaciones_disponibles():
    conn = get_db_connection()
    estaciones = conn.execute('''
        SELECT * FROM estaciones WHERE id != 1 AND id != 9  # Excluir Recepción y Salida
    ''').fetchall()
    conn.close()
    return jsonify([dict(e) for e in estaciones])

# API: Crear nuevo turno
@app.route('/api/turnos/nuevo', methods=['POST'])
def crear_turno():
    data = request.json
    
    # Generar número de turno (A001, A002, ...)
    conn = get_db_connection()
    ultimo_turno = conn.execute('SELECT numero FROM turnos ORDER BY id DESC LIMIT 1').fetchone()
    
    if ultimo_turno:
        ultimo_numero = int(ultimo_turno['numero'][1:])
        nuevo_numero = f"A{ultimo_numero + 1:03d}"
    else:
        nuevo_numero = "A001"
        
    # Determinar estación inicial basado en la selección
    estacion_inicial = data.get('estacion_inicial', 1)
    doctor_asignado = data.get('doctor_asignado') if estacion_inicial == 6 else None
    
    # Insertar nuevo turno
    conn.execute('''
        INSERT INTO turnos (numero, paciente_nombre, paciente_edad, tipo, estacion_actual, estacion_siguiente, doctor_asignado)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nuevo_numero, data['paciente_nombre'], data['paciente_edad'], data['tipo'], estacion_inicial, estacion_inicial, doctor_asignado))  
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'numero_turno': nuevo_numero})

# API: Buscar turnos
@app.route('/api/turnos/buscar/<query>')
def buscar_turnos(query):
    conn = get_db_connection()
    turnos = conn.execute('''
        SELECT t.*, e.nombre as estacion_actual_nombre, d.nombre as doctor_nombre
        FROM turnos t
        LEFT JOIN estaciones e ON t.estacion_actual = e.id
        LEFT JOIN doctores d ON t.doctor_asignado = d.id
        WHERE t.numero LIKE ? OR t.paciente_nombre LIKE ?
        ORDER BY t.timestamp_creacion DESC
    ''', (f'%{query}%', f'%{query}%')).fetchall()
    conn.close()
    return jsonify([dict(t) for t in turnos])

# API: Cancelar turno
@app.route('/api/turnos/<int:turno_id>/cancelar', methods=['PUT'])
def cancelar_turno(turno_id):
    conn = get_db_connection()
    conn.execute('UPDATE turnos SET estado = "CANCELADO" WHERE id = ?', (turno_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# API: Editar turno (REEMPLAZA "mover_turno")
@app.route('/api/turnos/<int:turno_id>/editar', methods=['PUT'])
def editar_turno(turno_id):
    data = request.json
    conn = get_db_connection()
    
    conn.execute('''
        UPDATE turnos 
        SET paciente_nombre = ?, paciente_edad = ?, tipo = ?, estacion_actual = ?, doctor_asignado = ?
        WHERE id = ?
    ''', (data['paciente_nombre'], data['paciente_edad'], data['tipo'], data['estacion_actual'], data.get('doctor_asignado'), turno_id))
    
    conn.commit()
    conn.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)