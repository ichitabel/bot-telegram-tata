from Info_Mensaje import Info_Mensaje
class Registro():
    def init(self):
        self.grupos = []


    def add(self,info):
        gana = False
        id = info.id_chat
        grupo = filter(lambda n: n == id, self.grupos)
        if grupo == None:
            self.grupos.append(id)
            gana = True
        return gana



