#!/usr/bin/env python3.7
# encoding: utf-8

import sys
sys.path.append('../')

import logging

import telegram
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler, CallbackQueryHandler, ConversationHandler, MessageHandler, Filters, RegexHandler)

from MontaUrl import MontaUrl
from Sinonimos import Sinonimos
from ConsultaFipe import ConsultaFipe
from CalculaDepreciacao import CalculaDepreciacao

TIPO, MARCA, MODELO, MODELO_LISTA, ANO, DEPRECIACAO, SAIR, PQ = range(8)

class App(object):

   def __init__(self):
      self.atualizador = Updater('721785961:AAEyD0MzGdj04HOJGC3FPJgdXObZD21-4Vg')
      self.despachante = self.atualizador.dispatcher
      self.logger = logging.getLogger(__name__)
      self.conv_handler = ''

      self.dicio = Sinonimos()
      self.uri = MontaUrl()
      self.fipe = ConsultaFipe()
      self.calc = CalculaDepreciacao()
      self.dic = {}
      self.ano = ''
      self.valor = ''
      
   logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
   
   def escolheTipo(self, bot, update):
      query = update.callback_query
      chat_id = query.message.chat.id
      
      self.fipe.escolheTipo(query.data)
      
      if query.data == 'SAIR':
         return SAIR
      elif query.data == 'moto':
         bot.sendMessage(chat_id=chat_id, text=u'Certo, agora informe a marca da sua {}: '.format(query.data))
      else: 
         bot.sendMessage(chat_id=chat_id, text=u'Certo, agora informe a marca do seu {}: '.format(query.data))
      
      return MARCA

   def escolheMarca(self, bot, update):
      marca = update.effective_message.text
      query = update.callback_query
      chat_id = query.message.chat.id
      
      resp = self.fipe.escolheMarca(marca)
      
      if resp == True:
         update.message.reply_text(u'Informe o modelo do seu veículo: ')
         return MODELO
      else:
         bot.sendMessage(chat_id=chat_id, text=resp)
         return MARCA
      

   def escolheModelo(self, bot, update):
      modelo = update.effective_message.text
      
      listaModelos = self.fipe.escolheModelo(modelo)
      if listaModelos:
         i = 1
         for nome in listaModelos:
            update.message.reply_text(str(i) + '-' + nome['name'])
            self.dic[i] = nome['name']
            i+=1
      else:
         print(u'Modelo não reconhecido!\n\
               Por favor, digite novamente\n\n')

      update.message.reply_text(u'\nEscolha o número correspondente ao seu veículo: ')

      return MODELO_LISTA

   def escolheModeloNaLista(self, bot, update):
      opt = update.effective_message.text

      modelo = self.fipe.escolheModeloNaLista(opt, self.dic)

      i = 1
      for nome in modelo:
         update.message.reply_text(str(i) + " - " + nome['name'])
         self.dic[i] = nome
         i += 1

      update.message.reply_text(u'\nEscolha qual o Ano/Combustível de seu veículo: ')
      
      return ANO

   def escolheAno(self, bot, update):
      opt = update.effective_message.text

      nomeValor = self.fipe.escolheAno(opt, self.dic)
      self.ano = nomeValor[1]
      self.valor = nomeValor[0]

      update.message.reply_text(u'\nValor atual do veículo ({}): {}'.format(nomeValor[2], nomeValor[0]))
      
      teclado = [
         [
            InlineKeyboardButton('Calcular depreciação contábil', callback_data='calcula'), 
            InlineKeyboardButton('SAIR', callback_data='sair')
         ]
      ]

      marcacao = InlineKeyboardMarkup(teclado)
      update.message.reply_text(u'\n\nEscolha o que fazer agora: ', reply_markup=marcacao)
      
      return DEPRECIACAO

   def calculaDepreciacao(self, bot, update):
      query = update.callback_query
      chat_id = query.message.chat.id
      opcao = query.data

      if opcao == 'sair':
         return SAIR
      elif opcao == 'calcula':
         print
         valorDepreciado = self.calc.calcular(self.ano, self.valor)
      else:
         print('Erro no input!')

      bot.sendMessage(chat_id=chat_id, text=valorDepreciado)
      
      return PQ
      
   def hello(self, bot, update):
      update.message.reply_text(u'Olá {}'.format(update.message.from_user.first_name))
      update.message.reply_text(u'Texto motivacional falando como isso funciona! Digite /sair para encerrar isso.\n\
      Depois de falar tudo, vamos começar?')

      teclado = [
         [
            InlineKeyboardButton('Carro', callback_data='carro'), 
            InlineKeyboardButton('Moto', callback_data='moto'), 
            InlineKeyboardButton('Caminhão', callback_data='caminhao'),
            InlineKeyboardButton('Sair', callback_data='SAIR')
         ]
      ]

      marcacao = InlineKeyboardMarkup(teclado)
      update.message.reply_text(u'Escolha um tipo de veículo:', reply_markup=marcacao)
      
      return TIPO
   
   def sair(self, bot, update):
      user = update.message.from_user
      
      self.logger.info(u'Usuário %s finalizou a pesquisa.', user.first_name)
      update.message.reply_text(u'Até mais! Volte sempre que precisar.')
      
      return ConversationHandler.END
   
   def porQue(self, bot, update):
      

   def error(self, update, context):
      self.logger.warning(u'A atualização "%s" Causou o erro "%s"', update, context.error)

   def main(self):
      self.conv_handler = ConversationHandler(
         entry_points=[CommandHandler(self.dicio.saudacao(), self.hello)],

         states={
            TIPO: [CallbackQueryHandler(self.escolheTipo)],

            MARCA: [RegexHandler('^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$', self.escolheMarca)],

            MODELO: [RegexHandler('^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$', self.escolheModelo)],

            MODELO_LISTA: [RegexHandler('^[\d]+$', self.escolheModeloNaLista)],

            ANO: [RegexHandler('^[\d]+$', self.escolheAno)],

            DEPRECIACAO: [CallbackQueryHandler(self.calculaDepreciacao)],

            SAIR: [CallbackQueryHandler(self.sair)],
            
            PQ: [CallbackQueryHandler(self.porQue)],
         },

         fallbacks=[CommandHandler('sair', self.sair)]
      )
      
      self.despachante.add_handler(self.conv_handler)
      self.despachante.add_error_handler(self.error)

      self.atualizador.start_polling()
      self.atualizador.idle()


# TODO: 
# - Botões "Por que este valor?" e "continuar" no fim do valor na FIPE e depreciação contábil
# - Tratamento de erro, chamando o próprio state de novo. (o consultaFipe vai retornar erro se 
#der errado e se o retorno das funções for uma string, chamamos de novo o state)