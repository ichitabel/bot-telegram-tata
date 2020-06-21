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
        miCursor.execute("SELECT * FROM datos WHERE datos.id_grupo = %s",param_list)
        tabla = miCursor.fetchall() 
        puntos = []
        for row in tabla:
            persona = Persona(grupo=row[0], id=row[1], cant=row[2])
            puntos.append(persona)
        miCursor.close()
        return puntos

    def persona_en_grupo(self,grupo,persona):
        existe = False
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [grupo,persona]
        miCursor.execute("SELECT * FROM datos WHERE datos.id_grupo = %s AND datos.id_persona = %s",param_list)
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
        miCursor.execute("SELECT datos.cantidad FROM datos WHERE datos.id_grupo = %s",param_list)
        tabla = miCursor.fetchall() 
        for row in tabla:
            existe = True
        miCursor.close()
        return existe
        

    def annadir_persona(self,grupo, persona):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [grupo,persona,1]
        miCursor.execute("INSERT INTO datos (id_grupo,id_persona,cantidad)VALUES(%s,%s,%s)",param_list)
        c.miConexion.commit()
        miCursor.close()

    def punto(self,grupo,persona):
        c = Conexion.Conexion()
        miCursor = c.miConexion.cursor()
        param_list = [grupo,persona]
        miCursor.execute("UPDATE datos SET cantidad = cantidad+1 WHERE datos.id_grupo = %s AND datos.id_persona = %s",param_list)
        c.miConexion.commit()
        miCursor.close()

    def add(self,grupo, persona):
        if self.existe_grupo(grupo):
            if self.persona_en_grupo(grupo, persona):
                self.punto(grupo, persona)
            else:
                self.annadir_persona(grupo, persona)
        else:
            self.annadir_persona(grupo, persona)


