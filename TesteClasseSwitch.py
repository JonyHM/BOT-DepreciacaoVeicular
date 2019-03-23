# -*- coding: utf-8 -*-

class Teste(object):    
    def __init__(self):
        pass

    def switch_teste(self, option):
         switcher = {
             1: "carros",
             2: "motos",
             3: "caminhoes"
         }
         return switcher.get(option, "invalido")