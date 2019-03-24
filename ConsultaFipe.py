# -*- coding: utf-8 -*-

import json, requests
from TesteClasseSwitch import Teste

class Consulta(object):
    url = 'http://fipeapi.appspot.com/api/1/'
    
    def __init__(self):
        self.tipo = ''
        self.marcas = []
        self.modelos = []
  
    def escolheTipo(self, url):        
        print("Escolha uma opção: ")
        print("\t 1 - Carro \n\t 2 - Moto \n\t 3 - Caminhão") ## Podem ser botões no telegram
        opt = int(input())

        # Chamando Classe de Teste, fazendo switch case
        choice = Teste(opt)            
        self.tipo = choice.switchTipo(opt)

        # Fazendo a requisição GET na API da tabela FIPE e 
        #transformando em objeto python com a lib json
        self.url = self.url + self.tipo
        response = requests.get(self.url + "/marcas.json")

        self.marcas = json.loads(response.content)

    def escolheMarca(self, marcas):
        print("Digite a marca do seu veículo: ")
        marca = input()

        for nome in self.marcas:
            if marca.upper() == nome['name']:
                id = nome['id']
                self.url = self.url + "/veiculos/" + str(id)
                break

        response = requests.get(self.url + ".json")

        try:
            self.modelos = json.loads(response.content)
        except:
            print("Marca não reconhecida!\nPor favor, digite novamente\n\n")
            self.escolheMarca(self.marcas)

        #Print pra ver modelos
        # for modelo in self.modelos:
        #     print(modelo['name'])

    ##def escolheModelo(self):


    #COMO DEFINIR QUAL O EXATO MODELO DO CARRO?
        #USUÁRIO VAI DIGITAR?
        #COMO GARANTIR QUE VAI DIGITAR CERTO? (TEM UM PADRÃO BEM ESPECÍFICO)
            #- Poderia pegar uma palavra digitada (EX: modelo = 'palio') e fazer 
            #um if modelo in self.modelos['nome'] - continua.... (Mas o foda é pegar o exato modelo)