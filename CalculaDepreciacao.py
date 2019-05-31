# encoding: utf-8

from datetime import datetime
import locale

locale.setlocale(locale.LC_ALL, '')

class CalculaDepreciacao(object):

    def __init__(self):
        self.ano = 0
        self.valorVeiculo = ''
        self.anoAtual = datetime.now().year
        self.idadeCarro = 0
        self.caracteres = 'R$ '

    def calcular(self, ano, valor):
        self.ano = ano
        self.valorVeiculo = valor
        
        if self.ano > self.anoAtual:
            self.idadeCarro = 0
            self.ano = self.anoAtual
        else:
            self.idadeCarro = self.anoAtual - self.ano

        self.valorVeiculo = self.valorVeiculo.replace(self.caracteres, '')
        self.valorVeiculo = locale.atof(self.valorVeiculo)
        
        if self.idadeCarro >= 5:
            self.valorVeiculo -= self.valorVeiculo * 0.1
            self.valorVeiculo = locale.currency(self.valorVeiculo, grouping=True,symbol=True)
            return u'\nSeu veículo valerá, aproximadamente,\n{}'.format(self.valorVeiculo)
                ## Como seu veículo tem mais de 5 anos, o cálculo de depreciação realizado é 
                # de -10% do valor atual anualmente
        else:
            self.valorVeiculo = locale.currency(self.valorVeiculo, grouping=True,symbol=True)
            return u'Seu veículo começará a depreciar efetivamente a partir de 5 anos de fabricação (em {})'.format(self.ano + 5)
        
        # return self.valorVeiculo