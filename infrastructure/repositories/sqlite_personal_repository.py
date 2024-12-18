import sqlite3
from domain.entities.personal import Personal
from icecream import ic

class SQLitePersonalRepository:
    def __init__(self):
        self.conn = sqlite3.connect('database.db', check_same_thread=False)

    def agregar(self, personal):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO personal (nombre, rol, horas_trabajadas) VALUES (?, ?, ?)",
            (personal.nombre, personal.rol, personal.horas_trabajadas)
        )
        personal.id = cursor.lastrowid
        self.conn.commit()

    def obtener_por_id(self, personal_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM personal WHERE personal_id = ?", (personal_id,))
        row = cursor.fetchone()
        if row:
            return Personal(
                id=row[0],
                nombre=row[1],
                rol=row[2],
                horas_trabajadas=row[3]
            )
        return None

    def listar_todos(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM personal")
        rows = cursor.fetchall()
        ic(rows)
        return [Personal(id=row[0], nombre=row[1], rol=row[2], horas_trabajadas=row[3]) for row in rows]

    def actualizar(self, personal):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE personal SET nombre = ?, rol = ?, horas_trabajadas = ? WHERE personal_id = ?",
            (personal.nombre, personal.rol, personal.horas_trabajadas, personal.id)
        )
        self.conn.commit()

    def eliminar(self, personal_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM personal WHERE personal_id = ?", (personal_id,))
        self.conn.commit()

    def asignar_a_proyecto(self, data):
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO proyecto_personal (personal_id, proyecto_id, horas_trabajadas) VALUES (?, ?, ?)",
            (data['personal_id'], data['proyecto_id'], data['horas_trabajadas'])
        )
        self.conn.commit()

    def obtener_proyectos_asignados(self, personal_id):
        """Devuelve los proyectos asignados a un personal."""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT p.id, p.nombre, p.fecha_inicio, p.fecha_estimacion_fin "
            "FROM proyectos p "
            "INNER JOIN personal_proyectos pp ON p.id = pp.proyecto_id "
            "WHERE pp.personal_id = ?",
            (personal_id,)
        )
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "nombre": row[1],
                "fecha_inicio": row[4],
                "fecha_estimacion_fin": row[5]
            }
            for row in rows
        ]
        
    def obtener_horas_trabajadas(self, personal_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT SUM(horas_trabajadas) FROM proyecto_personal WHERE personal_id = ?", (personal_id,))
        row = cursor.fetchone()
        return row[0] if row else 0
    
    