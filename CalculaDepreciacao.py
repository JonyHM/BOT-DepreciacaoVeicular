# encoding: utf-8

from datetime import datetime

class CalculaDepreciacao(object):

    def __init__(self):
        self.ano = 0
        self.valorVeiculo = ''
        self.anoAtual = datetime.now().year
        self.idadeCarro = 0
        self.caracteres = ' R$.'

    def calcular(self, ano, valor):
        self.ano = ano
        self.valorVeiculo = valor
        self.idadeCarro = self.anoAtual - self.ano

        self.valorVeiculo = self.valorVeiculo.split(',')
        self.valorVeiculo = self.valorVeiculo[0]

        for i in range(0, len(self.caracteres)):
            self.valorVeiculo = self.valorVeiculo.replace(self.caracteres[i], '')

        self.valorVeiculo = int(self.valorVeiculo)

        if self.idadeCarro > 5:
            print('Veiculo "usado"\n')
            self.valorVeiculo -= self.valorVeiculo * 0.1
            print('\nSeu veículo valerá, aproximadamente R$' + str(self.valorVeiculo))
                ## Como seu veículo tem mais de 5 anos, o cálculo de depreciação realizado é 
                # de -10% do valor atual anualmente
        else:
            print('Seu veículo começará a depreciar efetivamente a partir de 5 anos de fabricação: ' + str(ano+5))
        
        return self.valorVeiculo