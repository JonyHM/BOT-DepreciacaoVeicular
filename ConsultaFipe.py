# -*- coding: utf-8 -*-

import json, requests
from TesteClasseSwitch import Teste

class Consulta(object):
    url = 'http://fipeapi.appspot.com/api/1/'
    
    def __init__(self):
        self.tipo = ''
        self.marcas = []
  
    def escolheTipo(self, url):        
        print("Escolha uma opção: ")
        print("\t 1 - Carro \n\t 2 - Moto \n\t 3 - Caminhão")
        opt = int(input())

        # Chamando Classe de Teste, fazendo switch case
        choice = Teste(opt)            
        self.tipo = choice.switchTipo(opt)

        # Fazendo a requisição GET na API da tabela FIPE e 
        #transformando em objeto python com a lib json
        self.url = self.url + self.tipo
        response = requests.get(self.url + "/marcas.json")

        self.marcas = json.loads(response.content)

        return self.marcas

    def escolheMarca(self, marcas):
        print("Escolha uma marca: \n") 

        count = 1
    
        print('{:-^127}'.format("-"))
        for marca in self.marcas:
            print('{:<}{:^11}'.format('|', marca['name']), end="")
            
            if count == 10:
                print("\n")
                count = 0
            count += 1


