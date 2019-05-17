# -*- coding: utf-8 -*-

class MontaUrl(object):

    def __init__(self):
        self.url = 'http://fipeapi.appspot.com/api/1/'
        self.tipoVeiculo = ''
        self.idMarca = 0
        self.idModelo = 0
        self.ano = 0

    """
    Este método recebe apenas 'arg' por padrão, os demais argumentos são opcionais.
    Caso os valores dos argumentos estejam diferentes do padrão, serão armazenados
    """
    def montar(self, arg, tipoVeiculo='', idMarca=0, idModelo=0, ano=0):
        if tipoVeiculo != '':
            self.tipoVeiculo = tipoVeiculo
        
        if idMarca != 0:
            self.idMarca = idMarca
            arg += str(self.idMarca)

        if idModelo != 0:
            self.idModelo = idModelo
            arg += str(self.idMarca) + '/' + str(self.idModelo)

        if ano != 0:
            self.ano = ano
            arg += str(self.idMarca) + '/' + str(self.idModelo) + '/' + str(self.ano)
            
        return self.url + self.tipoVeiculo + arg + '.json'
    
    def getUrl(self):
        return self.url