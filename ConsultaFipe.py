# -*- coding: utf-8 -*-

import json, requests
from .TesteClasseSwitch import Teste

class Consulta(object):

    def __init__(self, option):
        self.option = option

    url = 'http://fipeapi.appspot.com/api/1/'

    print("Escolha uma opção: C Ta Ligado")
    opt = int(input())

    
    tipo = Teste(opt)
        
    print(tipo.switch_teste())

    """ response = requests.get(url+tipo)

    marcas = json.loads(response.content)

    for i in range(len(marcas)):
        print(marcas[i]['name']) """

    
if __name__ == "__main__":

    
