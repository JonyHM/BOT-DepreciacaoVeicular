# -*- coding: utf-8 -*-

## BOT Exemplo no telepot - Será extinto

# importando a biblioteca do bot
import telepot

# identificação do bot (token)
api = "846565667:AAEfYJPkNVRSgYY8IRggBlmGSjtMXteQEWc" 

# função para receber mensagem do usuário, retornar seu ID e nome
# cadastrado no python
def receber(msg): 
    text = msg['text']
    user_id = msg['from']['id']
    nome = msg['from']['first_name']
    print("ID: ", user_id)
    print("Nome: ", nome)
    print(text)
    if 'Oi' in text:
        tele.sendMessage(user_id, "Oi " + str(nome))
    else:
        tele.sendMessage(user_id, "Oi " + str(nome))
    tele.sendMessage(user_id, "Sou o DepreciaçãoBot, bot que calcula a depreciação do seu veículo, falando nisso, qual a marca do seu carro?")    	
        

tele = telepot.Bot(api)
tele.message_loop(receber)


while True:
    pass
