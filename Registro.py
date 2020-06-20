from Grupo import Grupo
from Persona import Persona
from Info_Mensaje import Info_Mensaje
class Registro():
    def init(self):
        self.grupos = []


    def add(self,info):
        gana = False
        self.grupos
        grupo = None
        grupo = filter(lambda n: Grupo(n).id == (Info_Mensaje).id_chat, self.grupos)
        if grupo == None:
            persona = Info_Mensaje(info).persona
            id_persoma = Info_Mensaje(info).id_persona
            chat = Info_Mensaje(info).chat
            id_chat = Info_Mensaje(info).id_chat
            grupo = Grupo(chat, id_chat, Persona(persona,id_persoma))
            self.grupos.append(grupo)
            gana = True
        return gana



