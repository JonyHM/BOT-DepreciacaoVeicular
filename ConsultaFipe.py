# -*- coding: utf-8 -*-
#controller

import json, requests
from TesteClasseSwitch import Teste

class Consulta(object):
    url = 'http://fipeapi.appspot.com/api/1/'
    
    def __init__(self):
        self.tipo = ''
        self.marcas = []
        self.modelos = []
        self.dicio = {}
        self.modelo = []
        self.listaModelos = []
        self.id = 0
        self.ano = []
  
    def escolheTipo(self):        
        print("Escolha uma opção: ")
        print("\t 1 - Carro \n\t 2 - Moto \n\t 3 - Caminhão") ## Podem ser botões no telegram
        opt = int(input())
        print('\n')

        # Chamando Classe de Teste, fazendo switch case
        escolha = Teste(opt)            
        self.tipo = escolha.switchTipo(opt)

        # Fazendo a requisição GET na API da tabela FIPE e 
        #transformando em objeto python com a lib json
        self.url = self.url + self.tipo
        response = requests.get(self.url + "/marcas.json")

        self.marcas = json.loads(response.content)

    def escolheMarca(self):
        print("Digite a marca do seu veículo: ")
        marca = input()
        print('\n')
        
        for nome in self.marcas:
            if marca.upper() == nome['name']:
                id = nome['id']
                url = self.url + "/veiculos/" + str(id)
                self.id = str(id)
                break

        response = requests.get(url + ".json")

        try:
            self.modelos = json.loads(response.content)
        except:
            print("Marca não reconhecida!\nPor favor, digite novamente\n\n")
            self.escolheMarca()

    def escolheModelo(self):
        print("Digite o modelo do seu veículo: ")
        opt = input()
        print('\n')

        for modelo in self.modelos:
            if opt.upper() in modelo['name'].upper():
                self.listaModelos.append(modelo)

        # Imprime os modelos com o nome informado, cada um com índice.
        #Depois atrela esse índice com a marca em um dicionario
        i = 1
        for nome in self.listaModelos:
            print(str(i) + " - " + nome['name'])
            self.dicio[i] = nome['name']
            i+=1

    def ecolheModeloNaLista(self):
        print("Escolha o número correspondente ao seu veículo: ")
        opt = int(input())
        print('\n')
        
        if opt in self.dicio.keys():
            modelo = self.dicio[opt]

            for nome in self.listaModelos:
                if modelo.upper() == nome['name'].upper():
                    id = nome['id']
                    self.url = self.url + "/veiculo/" + self.id + "/" + str(id)

        response = requests.get(self.url + ".json") #Da pra criar classe pra isso
        self.modelo = json.loads(response.content) 

        self.dicio = {}
        i = 1
        for nome in self.modelo:
            print(str(i) + " - " + nome['name'])
            self.dicio[i] = nome
            i+=1

    def escolheAno(self):
        print("Escolha qual o Ano e Combustível de seu veículo: ")
        opt = int(input())
        print('\n')

        if opt in self.dicio.keys():
            modelo = self.dicio[opt]
            id = modelo['id']        
            self.url = self.url + "/" + str(id)
        
        response = requests.get(self.url + ".json")
        self.ano = json.loads(response.content)

        print('Valor atual do veículo: ' + self.ano['preco'])