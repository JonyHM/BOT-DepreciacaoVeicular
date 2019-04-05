# -*- coding: utf-8 -*-

# Esta classe será destinada aos inputs do usuário
class Teste(object):    
    def __init__(self, option):
        self.option = option

    def switchTipo(self, option):
         switcher = {
             1: "carros",
             2: "motos",
             3: "caminhoes"
         }
         return switcher.get(option, "invalido")