from Info_Mensaje import Info_Mensaje
from Registro import Registro
import json
import Servicios
import datetime
import os
import requests
from flask import Flask, request
from datetime import datetime,time
import Persona


BOT_URL = f'https://api.telegram.org/bot{os.environ["BOT_KEY"]}/'  # <-- add your telegram token as environment variable

app = Flask(__name__)

servicio = Servicios.Servicios()

@app.route('/',methods=['Post'])
def main():
        sms = request.json
        info = info_mensaje(sms)
        if not info.is_bot and info.tipo_sms == "texto":
            #El mensaje es '!polerank'
            if str(leer_mensaje(sms)).lower() == "!polerank":
                if not info.tipo_chat.lower() == "private":
                    puntos = servicio.puntuacion(info.id_chat)
                    ranking = str_puntuacion(puntos)
                    enviar_mensaje(info.id_chat,ranking)
                else:
                    enviar_mensaje(info.id_chat,
                                           "La pole solo está habilitada en grupos o supergrupos")    
            #El mensaje es 'pole'
            elif str(leer_mensaje(sms)).lower() == "pole":
                if not info.tipo_chat.lower() == "private":
                    date = unix_date(info.date)
                    pole = is_pole(date)
                    if pole != -1:
                        if pole != temp.num_pole:
                            temp.registro = Registro()
                            temp.num_pole = pole
                        if (temp.registro.add(info)):
                            enviar_mensaje(info.id_chat,
                                            info.persona + " ha ganado la pole XD")
                            servicio.add(info.id_chat,info.id_persona)
                        else :
                            enviar_mensaje(info.id_chat,
                                           " Te mamaste")
                    else:
                        enviar_mensaje(info.id_chat,
                                           " No son horas de pole idiota ")
                else:
                    enviar_mensaje(info.id_chat,
                                           "La pole solo está habilitada en grupos o supergrupos")
        return ''

def leer_mensaje(mensaje):
    texto = mensaje['message']['text']
    return texto

def str_puntuacion(lista):
    result = ""
    for i in lista:
        id = i.id_persona
        """json_data = {
        "id": id,
        }
        message_url = BOT_URL + 'getFullUser'
        persona = requests.post(message_url, json=json_data)"""
        persona = requests.get("https://api.telegram.org/"+"getFullUser?id="+str(id))
        wi = persona.json()
        print(wi)
        nombre = wi['user']['first_name']
        result = result + nombre + "--"
        result = result + i.cantidad + "\n"
    return result

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
        
        tipo_chat = mensaje['message']['chat']['type']

        chat = ""
        if not tipo_chat.lower() == "private":
            chat = mensaje['message']['chat']['title']
        else:
            chat = tipo_chat

        update_id = mensaje['update_id']
        persona = mensaje['message']['from']['first_name']
        id_persona = mensaje['message']['from']['id']
        bot = mensaje['message']['from']['is_bot']
        id_chat = mensaje['message']['chat']['id']
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
    num_pole = -1
    registro = Registro()
    def __init__(self):
        pass

if __name__ == '__main__':  
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
