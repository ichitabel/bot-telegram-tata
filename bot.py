from Info_Mensaje import Info_Mensaje
from Registro import Registro
import json
from Servicios import Servicios
import datetime
import os
import requests
from flask import Flask, request
from datetime import datetime,time

class Bot():

    BOT_URL = f'https://api.telegram.org/bot{os.environ["BOT_KEY"]}/'  # <-- add your telegram token as environment variable

    app = Flask(__name__)
    def __init__(self):
        self.num_pole =0



    @app.route('/',methods=['Post'])
    def main(self):
        sms = request.json
        info = Info_Mensaje(self.info_mensaje(sms))
        if not info.is_bot and info.tipo_sms == "texto":
            if str(self.leer_mensaje(sms)).lower() == "!polerank":
                self.enviar_mensaje(info.id_chat,
                                           " No tenemos rango Equis De")
                #self.enviar_mensaje(Info_Mensaje(info).id_chat, self.puntuacion(Info_Mensaje(info).id_chat))
            elif str(self.leer_mensaje(sms)).lower() == "pole":
                date = self.unix_date(info.date)
                pole = self.is_pole(date)
                if pole != -1:
                    if pole != self.num_pole:
                        registro = Registro()
                        self.num_pole = pole
                    if (registro.add(info)):
                        self.enviar_mensaje(info.id_chat,
                                            info.persona + " ha ganado la pole XD")
                        #Servicios.add(Info_Mensaje(info).id_chat, Info_Mensaje(info).id_persona)
                    else :
                        self.enviar_mensaje(info.id_chat,
                                           " Te mamaste")
                else:
                    self.enviar_mensaje(info.id_chat,
                                           " No son horas de pole idiota ")





  #  def mostrar(self,idGrupo ):

   #     grupo = filter(lambda n: n.id == idGrupo,self.grupos)
    #    text = grupo.nombre +"\n..............\n"
  #      for persona in grupo.personas:
   #         text + persona.nombre + " " + str(persona.cant)+"\n"


    def actualizar(self ,offset):
        respuesta = requests.get(Conexion.URL + "getUpdates"+"?offset="+str(offset)+"&timeout="+str(100))
        mensajes_js = respuesta.cntent.decode("utf8")
        mensajes_diccionario = json.loads(mensajes_js)
        return mensajes_diccionario

    def leer_mensaje(self, mensaje):
        texto = mensaje["message"]["text"]
        return texto

    def enviar_mensaje(self,idChat, texto):
        json_data = {
        "chat_id": idChat,
        "text": texto,
    }
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=json_data)

    def info_mensaje(self, mensaje):

        if "text" in mensaje["message"]:
            tipo_sms ="texto"
        elif "sticker" in  mensaje["message"]:
            tipo_sms = "sticker"
        elif "animation" in mensaje["message"]:
            tipo_sms = "animacion"
        elif "photo" in mensaje["message"]:
            tipo_sms = "foto"
        else:
            tipo_sms = "otro"
        update_id = mensaje["update_id"]
        persona = mensaje["message"]["from"]["first_name"]
        id_persona = mensaje["message"]["from"]["id"]
        bot = mensaje["message"]["from"]["is_bot"]
        chat = mensaje["message"]["chat"]["first_name"]
        id_chat = mensaje["message"]["chat"]["id"]
        tipo_chat = mensaje["message"]["chat"]["type"]
        date = mensaje["message"]["date"]
        return Info_Mensaje( persona, id_persona , bot, chat, id_chat, tipo_chat, tipo_sms, date,update_id)

    def puntuacion(self,grupo):
        text = "WIIII\n..............\n"
        for persona in Servicios.puntuacion(grupo):
            text + "" + " " + str(persona.cantidad)+"\n"
        return text

    def is_pole(self,date):
        fecha = time(date)
        lista = [[time(3),time(4)],[time(9),time(10)],[time(15),time(16)],[time(21),time(22)]]
        pole = -1
        for i in range(0, lista.__len__()-1):
            if fecha >= lista[i][0] and fecha < lista[i][1]:
                pole = i
                break
        return pole

    def unix_date(self,fecha):
        return datetime.datetime.fromtimestamp(fecha).strftime("%H:%M:%S")

    if __name__ == '__main__':  
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
