import sqlite3
from domain.entities.proyecto import Proyecto
from icecream import ic

class SQLiteProyectoRepository:
    def agregar(self, proyecto):
        ic(proyecto)
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO proyectos (nombre, presupuesto_inicial, fecha_inicio, fecha_estimacion_fin, porcentaje_avance) VALUES (?, ?, ?, ?, ?)",
            (proyecto.nombre, proyecto.presupuesto_inicial, proyecto.fecha_inicio, proyecto.fecha_estimacion_fin, proyecto.porcentaje_avance)
        )
        proyecto.id = cursor.lastrowid
        conn.commit()
         # Verificar lo que se guardó
        cursor.execute("SELECT * FROM proyectos WHERE id = ?", (cursor.lastrowid,))
        row = cursor.fetchone()
        ic(row)
        conn.close()

    def obtener_por_id(self, proyecto_id):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, presupuesto_inicial, fecha_inicio, fecha_estimacion_fin, porcentaje_avance FROM proyectos WHERE id = ?", (proyecto_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            proyecto = Proyecto(nombre=row[1], presupuesto_inicial=row[2], fecha_inicio=row[3], fecha_estimacion_fin=row[4], porcentaje_avance=row[5])
            proyecto.id = row[0]
            return proyecto
        return None

    def listar_todos(self):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre, presupuesto_inicial, fecha_inicio, fecha_estimacion_fin, porcentaje_avance FROM proyectos")
        rows = cursor.fetchall()
        conn.close()
        proyectos = []
        for row in rows:
            proyecto = Proyecto(nombre=row[1], presupuesto_inicial=row[2], fecha_inicio=row[3], fecha_estimacion_fin=row[4], porcentaje_avance=row[5])
            proyecto.id = row[0]
            proyectos.append(proyecto)
        return proyectos
    
    def actualizar(self, proyecto):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE proyecto SET nombre = ?, presupuesto_inicial = ?, fecha_inicio = ?, fecha_estimacion_fin = ?, porcentaje_avance = ? WHERE id = ?",
            (proyecto.nombre, proyecto.presupuesto_inicial, proyecto.fecha_inicio, proyecto.fecha_estimacion_fin, proyecto.porcentaje_avance, proyecto.id)
        )
        conn.commit()
        conn.close()
        
    def eliminar(self, proyecto_id):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM proyectos WHERE id = ?", (proyecto_id,))
        conn.commit()
        conn.close()