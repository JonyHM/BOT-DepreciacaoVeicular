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
      resp = self.fipe.escolheMarca(marca)
      
      if resp == True:
         update.message.reply_text(u'Informe o modelo do seu veículo: ')
         return MODELO
      else:
         update.message.reply_text(resp)
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
         txt = u'Modelo não reconhecido!\n\
               Por favor, digite novamente.\n\n'
         update.message.reply_text(txt)
         update.message.reply_text(u'Informe o modelo do seu veículo: ')
         return MODELO

      update.message.reply_text(u'\nEscolha o número correspondente ao seu veículo: ')

      return MODELO_LISTA

   def escolheModeloNaLista(self, bot, update):
      opt = update.effective_message.text
      modelo = self.fipe.escolheModeloNaLista(opt, self.dic)

      if isinstance(modelo, str):
         update.message.reply_text(modelo)
         update.message.reply_text(u'Informe o modelo do seu veículo: ')
         return MODELO 
      else:
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
      
      if isinstance(nomeValor, str):
         update.message.reply_text(nomeValor)
         update.message.reply_text(u'Informe o modelo do seu veículo: ')
         return MODELO
      else:
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
      else:
         valorDepreciado = self.calc.calcular(self.ano, self.valor)

      bot.sendMessage(chat_id=chat_id, text=valorDepreciado)
      
      return PQ
      
   def hello(self, bot, update):
      update.message.reply_text(u'Olá {}'.format(update.message.from_user.first_name))
      update.message.reply_text(u'Texto motivacional falando como isso funciona! Digite /sair para encerrar isso.\n\
      Depois de falar tudo, vamos começar?') ## Aprenentar o BOT, suas funções e motivações

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
      query = update.callback_query
      chat_id = query.message.chat.id
      opcao = query.data
      
      teclado = [
         [
            InlineKeyboardButton('Carro', callback_data='carro'), 
            InlineKeyboardButton('Moto', callback_data='moto'), 
            InlineKeyboardButton('Caminhão', callback_data='caminhao'),
            InlineKeyboardButton('Sair', callback_data='SAIR')
         ]
      ]
      marcacao = InlineKeyboardMarkup(teclado)
      
      textoAposDepreciacao = ''##Explicar o pq da depreciação - como funciona
      bot.sendMessage(chat_id=chat_id, text=textoAposDepreciacao)
      update.message.reply_text(u'Se deseja calcular outro veículo, escolha um tipo de veículo:', reply_markup=marcacao)
      
      return TIPO
         

   def error(self, update, context):
      self.logger.warning(u'A atualização "%s" Causou o erro "%s"', update, context.error)

   def main(self):
      self.conv_handler = ConversationHandler(
         entry_points=[CommandHandler(self.dicio.saudacao(), self.hello)],

         states={
            TIPO: [CallbackQueryHandler(self.escolheTipo)],

            MARCA: [RegexHandler('^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$', self.escolheMarca),
                          CommandHandler(self.dicio.saudacao(), self.hello)],

            MODELO: [RegexHandler('^[A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÍÏÓÔÕÖÚÇÑ ]+$', self.escolheModelo),
                          CommandHandler(self.dicio.saudacao(), self.hello)],

            MODELO_LISTA: [RegexHandler('^[\d]+$', self.escolheModeloNaLista),
                          CommandHandler(self.dicio.saudacao(), self.hello)],

            ANO: [RegexHandler('^[\d]+$', self.escolheAno),
                          CommandHandler(self.dicio.saudacao(), self.hello)],

            DEPRECIACAO: [CallbackQueryHandler(self.calculaDepreciacao),
                          CommandHandler(self.dicio.saudacao(), self.hello)],

            SAIR: [CallbackQueryHandler(self.sair)],
            
            PQ: [CallbackQueryHandler(self.porQue),
                          CommandHandler(self.dicio.saudacao(), self.hello)],
         },

         fallbacks=[CommandHandler('sair', self.sair)]
      )
      
      self.despachante.add_handler(self.conv_handler)
      self.despachante.add_error_handler(self.error)

      self.atualizador.start_polling()
      self.atualizador.idle()
      
# TODO: 
# - Melhorar a tratativa de erros