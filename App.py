import logging
import json, requests
import locale
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
locale.setlocale(locale.LC_ALL, '')

TOKEN = "892737322:AAGYB5X5cJnFyLbjsBSQ8lw4t1tYAPvR2t4"
BASE_URL = "http://fipeapi.appspot.com/api/1"

bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

global marca
global marcas
global modelo
global modelos
global modelo_id
global veiculo_id

marca = None
marcas = None
modelo = None
modelos = None
modelo_id = None
veiculo_id = None

def test(bot, update, args):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    user_name = update.message.chat.first_name
    message_id = update.message.message_id
    
    query = update.callback_query

    print("CALLBACK Q", query)
    print("MESSAGE:", update.message)

    print("ARGS TEST", args)

    if not query:
        bot.sendMessage(chat_id=chat_id, text="Olá, {}!".format(user_name))
        keyboard = [[
            InlineKeyboardButton('Carro', callback_data='car'),
            InlineKeyboardButton('Moto', callback_data='bike'),
            InlineKeyboardButton('Caminhão', callback_data='truck')
        ]]
        bot.sendMessage(chat_id=chat_id, text="Select option below", reply_markup=InlineKeyboardMarkup(keyboard))


def t2(bot, update, args):
    chat_id = update.message.chat.id
    user_id = update.message.from_user.id
    user_name = update.message.chat.first_name
    message_id = update.message.message_id

    query = update.callback_query
    print("QUERY [", query, "]")

    global marca
    global marcas
    global modelo
    global modelos
    global modelo_id
    global veiculo_id

    print("ARGS: ", args)

    ############################################
    if len(args) == 0:
        bot.sendMessage(chat_id=chat_id, text="Insira a marca de seu veículo")
    else:
        if not marca:
            bot.sendMessage(chat_id=chat_id, text="Recuperando dados de marcas de veículos, aguarde...")
            URL = "{}/carros/marcas.json".format(BASE_URL)

            response = requests.get(URL)

            marcas = json.loads(response.content)

            len_marcas = len(marcas)

            print("{} marcas".format(len_marcas))

            bot.sendMessage(chat_id=chat_id, text="Dados carregados! :D")

            marca = args[0]

            bot.sendMessage(chat_id=chat_id, text="Recuperando modelos de {}".format(marca))

            URL = ""
            for m in marcas:
                if marca.upper() == m['name']:
                    URL = "{}/carros/veiculos/{}.json".format(BASE_URL, m['id'])
                    break
        
            response = requests.get(URL)

            bot.sendMessage(chat_id=chat_id, text="Modelos recuperados! :D")

            modelos = json.loads(response.content)
            print(modelos[0])

            total_veiculos = len(modelos)

            bot.sendMessage(chat_id=chat_id, text="Encontrei {} {}. Aqui estão alguns deles: ".format(total_veiculos,
                            "modelos" if total_veiculos > 1 else "modelo"))
        
            for m in modelos[:11]:
                bot.sendMessage(chat_id=chat_id, text="ID: {} - {}".format(m['id'], m['name']))

            bot.sendMessage(chat_id=chat_id, text="Escolha o id de seu veículo")
        else:
            if not modelo:
                modelo_id = args[0]

                URL = ""
                found = False

                for m in modelos:
                    if modelo_id == m['id']:
                        URL = "{}/carros/veiculo/21/{}.json".format(BASE_URL, modelo_id)
                        found = True
                        break
                
                print("URL", URL)

                bot.sendMessage(chat_id=chat_id,text="Recuperando dados do modelo...")
                response = json.loads(requests.get(URL).content)

                if 'error' in response:
                    bot.sendMessage(chat_id=chat_id, text="Ocorreu um erro nesta operação")
                    bot.sendMessage(chat_id=chat_id, text="{}".format(json.dumps(response)))
                else:
                    modelo = response

                    if len(modelo) > 1 and type(modelo) == list:
                        bot.sendMessage(chat_id=chat_id, text="Encontrei mais de um modelo com esse nome")
                        
                        for m in response:
                            bot.sendMessage(chat_id=chat_id, text="ID: {} - {} {}".format(m['fipe_codigo'], m['veiculo'], m['name']))
                        
                        bot.sendMessage(chat_id=chat_id, text="Qual é o seu?")
            else:
                veiculo_id = args[0]

                URL = "{}/carros/veiculo/21/{}/{}.json".format(BASE_URL, modelo_id, veiculo_id)

                print(URL)

                modelo = json.loads(requests.get(URL).content)

                if 'error' in modelo:
                    bot.sendMessage(chat_id=chat_id, text="Não achei este veículo :(")
                else:
                    bot.sendMessage(chat_id=chat_id, text="{}".format(json.dumps(modelo)))
                    bot.sendMessage(chat_id=chat_id, text="CABO MAN")

                    print(int(modelo.get('preco')[2:]))
                    
def help(self, updater):
    pass

dispatcher.add_handler(CommandHandler('t', test, pass_args=True))
dispatcher.add_handler(CommandHandler('c', t2, pass_args=True))

dispatcher.add_handler(CallbackQueryHandler(test))

updater.start_polling()
updater.idle()