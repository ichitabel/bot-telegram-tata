import psycopg2
import Singleton

@Singleton.SingletonDecorator
class Conexion:
    def __init__(self):
        try:
            self.miConexion = psycopg2.connect(dbname="d3e6itms38e4r5", user="sudvnykzdurqme", password="1d1ad100084a54a1192c4dcac82c88e2b93ebd42cd03849c6000776f81d989a5",host="ec2-3-216-129-140.compute-1.amazonaws.com")
        except:
            print("Error en la base de datos")

