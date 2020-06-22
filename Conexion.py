import psycopg2
import Singleton

@Singleton.SingletonDecorator
class Conexion:
    def __init__(self):
        try:
            self.miConexion = psycopg2.connect(os.environ["DATABASE_URL"])
        except:
            print("Error en la base de datos")

