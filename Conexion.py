import psycopg2
import Singleton

@Singleton.SingletonDecorator
class Conexion:
    def __init__(self):
        try:
            self.miConexion = psycopg2.connect(dbname="dn43sr6l9fe8j", user="kmmfirqlfmuxce", password="8485bb0c2d4a98bf8993e3ad7ac24fc42e722ee5f20fa6d919b45e537b7e6034",host="ec2-34-230-231-71.compute-1.amazonaws.com")
        except:
            print("Error en la base de datos")

