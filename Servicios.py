from Persona import Persona
import sys, psycopg2
import Singleton
import Conexion

@Singleton.SingletonDecorator
class Servicios():
    def puntuacion(self,grupo):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [grupo]
        miCursor.execute("SELECT * FROM pole JOIN persona ON persona.id_persona = pole.id_persona WHERE pole.id_grupo = %s ORDER BY pole.cantidad DESC",param_list)
        tabla = miCursor.fetchall() 
        puntos = []
        for row in tabla:
            persona = Persona(grupo=row[0], id=row[1], cant=row[2],nombre_persona=row[5])
            puntos.append(persona)
        miCursor.close()
        return puntos

    def persona_en_grupo(self,grupo,persona):
        existe = False
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [grupo,persona]
        miCursor.execute("SELECT * FROM pole WHERE pole.id_grupo = %s AND pole.id_persona = %s",param_list)
        tabla = miCursor.fetchall()
        for row in tabla:
            existe = True
            break
        miCursor.close()
        return existe

    def existe_grupo(self,grupo):
        existe = False
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [grupo]
        miCursor.execute("SELECT pole.cantidad FROM pole WHERE pole.id_grupo = %s",param_list)
        tabla = miCursor.fetchall() 
        for row in tabla:
            existe = True
        miCursor.close()
        return existe
        

    def annadir_persona_pole(self,grupo, persona):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [grupo,persona,1]
        miCursor.execute("INSERT INTO pole (id_grupo,id_persona,cantidad)VALUES(%s,%s,%s)",param_list)
        c.miConexion.commit()
        miCursor.close()

    def annadir_persona(self,id,nombre):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [id,nombre]
        miCursor.execute("INSERT INTO persona(id_persona,nombre_persona)VALUES(%s,%s)",param_list)
        c.miConexion.commit()
        miCursor.close()

    def actualizar_persona(self,id,nombre):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [nombre,id]
        miCursor.execute("UPDATE persona SET nombre_persona = %s WHERE persona.id_persona = %s",param_list)
        c.miConexion.commit()
        miCursor.close()

    def existe_persona(self,id):
        existe = False
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [id]
        miCursor.execute("SELECT * FROM persona WHERE persona.id_persona = %s",param_list)
        tabla = miCursor.fetchall() 
        for row in tabla:
            existe = True
        miCursor.close()
        return existe

    def punto(self,grupo,persona):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [grupo,persona]
        miCursor.execute("UPDATE pole SET cantidad = cantidad + 1 WHERE pole.id_grupo = %s AND pole.id_persona = %s",param_list)
        c.miConexion.commit()
        miCursor.close()

    def add(self,grupo, persona):
        if self.existe_grupo(grupo):
            if self.persona_en_grupo(grupo, persona):
                self.punto(grupo, persona)
            else:
                self.annadir_persona_pole(grupo, persona)
        else:
            self.annadir_persona_pole(grupo, persona)


