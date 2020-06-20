import sqlite3
from Persona import Persona
class Servicios():
    @staticmethod
    def conexion():
        return sqlite3.connect('boteando.sqlite')

    @staticmethod
    def puntuacion(grupo):
        c = Servicios.conexion()
        query = "Select * from registro where id_grupo = ?"
        puntos = []
        for row in c.execute(query,grupo):
            persona = Persona(grupo= row[0],id=row[1],cant=row[2])
            puntos.append(persona)
        c.close()
        return puntos

    @staticmethod
    def persona_en_grupo(grupo,persona):
        existe = False
        c = Servicios.conexion()
        query = "Select cantid from registro where id_grupo =? AND id_persona = ?"
        if len(list(c.execute(query,grupo,persona)))>0:
            existe = True
        c.close()
        return existe

    @staticmethod
    def existe_grupo(grupo):
        existe = False
        c = Servicios.conexion()
        query = "Select cantid from registro where id_grupo =? "
        if len(list(c.execute(query, grupo))) > 0:
            existe = True
        c.close()
        return existe

    @staticmethod
    def annadir_persona(grupo, persona):
        c = Servicios.conexion()
        query = "INSERT INTO registro SET cantidad = cantidad +1 where id_grupo =? AND id_persona = ?"
        c.execute(query,grupo,persona)
        c.commit()
        c.close()

    @staticmethod
    def punto(grupo,persona):
        c = Servicios.conexion()
        query = "UPDATE registro ('id_grupo','id_persona','cantidad') VALUES (?,?'1')"
        c.execute(query, grupo, persona)
        c.commit()
        c.close()

    @staticmethod
    def add(grupo,persona):
        if Servicios.existe_grupo(grupo):
            if Servicios.persona_en_grupo(grupo,persona):
                Servicios.punto(grupo,persona)
            else:
                Servicios.annadir_persona(grupo,persona)
        else:
            Servicios.annadir_persona(grupo,persona)


