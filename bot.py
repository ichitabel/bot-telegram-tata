from Info_Mensaje import Info_Mensaje
from Registro import Registro
import json
from Servicios import Servicios
import datetime
import os
import requests
from flask import Flask, request
from datetime import datetime,time


BOT_URL = f'https://api.telegram.org/bot{os.environ["BOT_KEY"]}/'  # <-- add your telegram token as environment variable

app = Flask(__name__)



@app.route('/',methods=['Post'])
def main():
        sms = request.json
        info = info_mensaje(sms)
        if not info.is_bot and info.tipo_sms == "texto":
            if str(leer_mensaje(sms)).lower() == "!polerank":
                enviar_mensaje(info.id_chat,
                                           " No tenemos rango Equis De")
                #self.enviar_mensaje(Info_Mensaje(info).id_chat, self.puntuacion(Info_Mensaje(info).id_chat))
            elif str(leer_mensaje(sms)).lower() == "pole":
                date = unix_date(info.date)
                pole = is_pole(date)
                if pole != -1:
                    if pole != temp.num_pole:
                        registro = Registro()
                        temp.num_pole = pole
                    if (registro.add(info)):
                        enviar_mensaje(info.id_chat,
                                            info.persona + " ha ganado la pole XD")
                        #Servicios.add(Info_Mensaje(info).id_chat, Info_Mensaje(info).id_persona)
                    else :
                        enviar_mensaje(info.id_chat,
                                           " Te mamaste")
                else:
                    enviar_mensaje(info.id_chat,
                                           " No son horas de pole idiota ")
        return ''





  #  def mostrar(self,idGrupo ):

   #     grupo = filter(lambda n: n.id == idGrupo,self.grupos)
    #    text = grupo.nombre +"\n..............\n"
  #      for persona in grupo.personas:
   #         text + persona.nombre + " " + str(persona.cant)+"\n"

def leer_mensaje(mensaje):
        texto = mensaje['message']['text']
        return texto

def enviar_mensaje(idChat, texto):
    json_data = {
        "chat_id": idChat,
        "text": texto,
    }
    message_url = BOT_URL + 'sendMessage'
    requests.post(message_url, json=json_data)
    return ''

def info_mensaje(mensaje):
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
        update_id = mensaje['update_id']
        persona = mensaje['message']['from']['first_name']
        id_persona = mensaje['message']['from']['id']
        bot = mensaje['message']['from']['is_bot']
        #chat = mensaje['message']['chat']['first_name']
        chat = "el pingas"
        id_chat = mensaje['message']['chat']['id']
        tipo_chat = mensaje['message']['chat']['type']
        date = mensaje['message']['date']
        return Info_Mensaje( persona, id_persona , bot, chat, id_chat, tipo_chat, tipo_sms, date,update_id)

def is_pole(date):
        lista = [[time(3),time(8,59)],[time(9),time(14,59)],[time(15),time(20,59)],[time(21),time(23,59)]]
        pole = -1
        for i in range(0, lista.__len__()-1):
            if date >= lista[i][0] and date < lista[i][1]:
                pole = i
                break
        return pole

def unix_date(fecha):
        return datetime.fromtimestamp(fecha).time()

class temp():
    num_pole = 0

if __name__ == '__main__':  
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
