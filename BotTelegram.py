# encoding: utf-8

import sys
sys.path.append('../')

import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

from models.MontaUrl import MontaUrl


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

def botao(bot, update):
   teste = MontaUrl()
   query = update.callback_query

   query.edit_message_text(text="Opção selecionada: {}".format(query.data))

   print(teste.montar(query.data))


def hello(bot, update):
   update.message.reply_text(
      'Falae {}'.format(update.message.from_user.first_name))

   teclado = [[InlineKeyboardButton('Carro', callback_data='carro'), 
      InlineKeyboardButton('Moto', callback_data='moto'), 
      InlineKeyboardButton('Caminhão', callback_data='caminhao')]]

   marcacao = InlineKeyboardMarkup(teclado)
   update.message.reply_text('Escolha um tipo de veículo:', reply_markup=marcacao)

def error(update, context):
   logger.warning('A atualização "%s" Causou o erro "%s"', update, context.error)

def main():
   updater = Updater(
      '721785961:AAEyD0MzGdj04HOJGC3FPJgdXObZD21-4Vg')

   despachante = updater.dispatcher

   despachante.add_handler(CommandHandler('oi', hello))
   despachante.add_handler(CallbackQueryHandler(botao))
   despachante.add_error_handler(error)

   updater.start_polling()
   updater.idle()

if __name__ == '__main__':
    main()