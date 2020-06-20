from Persona import Persona
class Grupo():
    def __init__(self, nombre, id , persona):
        self.nombre = nombre
        self.id = id
        self.personas = [persona]


    def addPersona(self, persona):
        bien = False
        if len(list(filter(lambda n:Persona(n).id == Persona(persona).id)))==0:
            estaba = True
            self.personas.append(persona)
        return bien

    def aumentar(self,id_usuario):
          temp = filter(lambda n:n.id == id_usuario, self.personas)
          Persona(temp).cant += 1