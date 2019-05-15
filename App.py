import logging
import json, requests
import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

TOKEN = "892737322:AAGYB5X5cJnFyLbjsBSQ8lw4t1tYAPvR2t4"
BASE_URL = "http://fipeapi.appspot.com/api/1"

bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

global marca
global marcas
global modelo
global modelos
global modelos_dict
global ano_combustivel
global c

marca = None
marcas = None
modelo = None
modelos = None
modelos_dict = None
ano_combustivel = None
c = 0

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
    global modelos_dict
    global ano_combustivel
    global c

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
            modelo_id = args[0]

            print(modelos[:3])

            URL = ""
            found = False

            for m in modelos:
                if modelo_id == m['id']:
                    URL = "{}/carros/veiculo/{}/{}.json".format(BASE_URL, m['id'], modelo_id)
                    found = True
                    break
            
            response = requests.get(URL)

            modelo = json.loads(response.content)

            if not found:
                bot.sendMessage(chat_id=chat_id, text="Não achei este veículo :(")
            else:
                bot.sendMessage(chat_id=chat_id, text="{}".format(json.dumps(modelo)))
                bot.sendMessage(chat_id=chat_id, text="CABO MAN")
                

    ############################################
    
    #if not ano_combustivel:
    #    bot.sendMessage(chat_id=chat_id, text="Insira o ano/combustível de seu veículo")
    #else:
    #    ano_combustivel = args[0]
    #    print

def help(self, updater):
    pass

dispatcher.add_handler(CommandHandler('t', test, pass_args=True))
dispatcher.add_handler(CommandHandler('t2', t2, pass_args=True))

dispatcher.add_handler(CallbackQueryHandler(test))

updater.start_polling()
updater.idle()