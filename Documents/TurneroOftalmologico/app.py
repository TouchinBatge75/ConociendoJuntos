# app.py - REEMPLAZA TODO EL ARCHIVO
from flask import Flask, render_template, jsonify, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('turnos.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def recepcion():
    return render_template('recepcion.html')

# API SIMPLIFICADA - SOLO ESTACIÓN ACTUAL
@app.route('/api/turnos')
def get_turnos():
    conn = get_db_connection()
    turnos = conn.execute('''
        SELECT t.*, 
               e.nombre as estacion_actual_nombre,
               d.nombre as doctor_nombre
        FROM turnos t
        LEFT JOIN estaciones e ON t.estacion_actual = e.id
        LEFT JOIN doctores d ON t.doctor_asignado = d.id
        WHERE t.estado != "FINALIZADO" AND t.estado != "CANCELADO"
        ORDER BY t.timestamp_creacion DESC
    ''').fetchall()
    conn.close()
    
    # DEBUG: Ver datos
    for turno in turnos:
        print(f"DEBUG: Turno {dict(turno)['numero']} - Doctor: {dict(turno)['doctor_nombre']}")
    
    return jsonify([dict(turno) for turno in turnos])

@app.route('/api/doctores')
def get_doctores():
    conn = get_db_connection()
    doctores = conn.execute('SELECT * FROM doctores WHERE activo = 1').fetchall()
    conn.close()
    return jsonify([dict(d) for d in doctores])

@app.route('/api/estaciones')
def get_estaciones_disponibles():
    conn = get_db_connection()
    estaciones = conn.execute('SELECT * FROM estaciones WHERE id != 1 AND id != 8').fetchall()
    conn.close()
    return jsonify([dict(e) for e in estaciones])

@app.route('/api/turnos/nuevo', methods=['POST'])
def crear_turno():
    data = request.json
    
    conn = get_db_connection()
    ultimo_turno = conn.execute('SELECT numero FROM turnos ORDER BY id DESC LIMIT 1').fetchone()
    
    if ultimo_turno:
        ultimo_numero = int(ultimo_turno['numero'][1:])
        nuevo_numero = f"A{ultimo_numero + 1:03d}"
    else:
        nuevo_numero = "A001"
        
    # CORREGIDO: Usar 4 para Consulta Médica (como en tu HTML)
    estacion_inicial = data.get('estacion_inicial', 1)
    doctor_asignado = data.get('doctor_asignado') if estacion_inicial == 4 else None  # ← 4 no 6
    
    # INSERT SIMPLIFICADO - sin estacion_siguiente
    conn.execute('''
        INSERT INTO turnos (numero, paciente_nombre, paciente_edad, tipo, estacion_actual, doctor_asignado)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nuevo_numero, data['paciente_nombre'], data['paciente_edad'], data['tipo'], estacion_inicial, doctor_asignado))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'numero_turno': nuevo_numero})

@app.route('/api/turnos/<int:turno_id>/cancelar', methods=['PUT'])
def cancelar_turno(turno_id):
    conn = get_db_connection()
    conn.execute('UPDATE turnos SET estado = "CANCELADO" WHERE id = ?', (turno_id,))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

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