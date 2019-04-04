# -*- coding: utf-8 -*-

class Teste(object):    
    def __init__(self, option):
        self.option = option
        self.marcas = []
        self.modelos = []

    def switchTipo(self, option):
         switcher = {
             1: "carros",
             2: "motos",
             3: "caminhoes"
         }
         return switcher.get(option, "invalido")