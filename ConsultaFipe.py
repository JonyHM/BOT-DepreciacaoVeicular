# -*- coding: utf-8 -*-

import json, requests
from Escolhas import Escolhas
from MontaUrl import MontaUrl



### Vai apenas interagir com a API da tabela FIPE
class ConsultaFipe(object):    
    
    def __init__(self):
        self.escolha = Escolhas()           
        self.montaUrl = MontaUrl()
        self.nomeVeiculo = ''
        self.valorVeiculo = ''
        self.anoVeiculo = 0

        self.marcas = [] ### Separar coleções em outra classe?
        self.modelos = []
        self.modelo = []
        self.listaModelos = []
        self.dicio = {}
        self.ano = []
        
    def escolheTipo(self):  
        print('Escolha uma opção: ')
        print('\t 1 - Carro \n\t\
            2 - Moto \n\t\
            3 - Caminhão\n\t\
            0 - SAIR') ## Podem ser botões no telegram
        print('\n')

        opt = self.escolha.switchTipo(int(input()))

        if opt == 'invalido':
            print('Opção inválida!\nPor favor, tente novamente\n')
            self.escolheTipo()
        elif opt == 'SAIR':
            print('\nSaindo...\n')
            exit(0)
        else:
            tipo = opt

        # Fazendo a requisição GET na API da tabela FIPE e transformando em objeto python com a lib json
        url = self.montaUrl.montar(arg='/marcas', tipoVeiculo=tipo)

        self.marcas = self.pegaDados(url)

    def escolheMarca(self):
        print('Digite a marca do seu veículo (r para retornar): ')
        marca = input()
        print('\n')

        if marca.upper() == 'R':
            self.escolheTipo()

        for nome in self.marcas:
            if marca.upper() == nome['name'].upper():
                url = self.montaUrl.montar(arg='/veiculos/', idMarca=nome['id'])
                break

        try:
            self.modelos = self.pegaDados(url)
        except:
            print("Marca não reconhecida!\nPor favor, digite novamente\n\n")
            self.escolheMarca()

    def escolheModelo(self):
        if len(self.listaModelos) <= 0:
            print("Digite o modelo do seu veículo (r para retornar): ")
            opt = input()
            print('\n')

            if marca.upper() == 'R':
                self.escolheMarca()

            # Percorre a lista de modelos e verifica se o input do usuário é igual ao nome do modelo, ambos em upper case e o 
            #adiciona na lista de modelos para exibição futuramente
            for modelo in self.modelos:
                if opt.upper() in modelo['name'].upper():
                    self.listaModelos.append(modelo)

        
        # Imprime os modelos com o nome informado, cada um com índice. Depois atrela esse índice com a marca em um dicionario
        if self.listaModelos:
            i = 1
            for nome in self.listaModelos:
                print(str(i) + " - " + nome['name'])
                self.dicio[i] = nome['name']
                i+=1
        else:
            print("Modelo não reconhecido!\nPor favor, digite novamente\n\n")
            self.listaModelos = []
            self.escolheModelo()

    ## -- ARRUMAR TRATAMENTO DE REQUISIÇÕES -- ##
    def escolheModeloNaLista(self):
        print("Escolha o número correspondente ao seu veículo (0 para retornar): ") ## Dar um exemplo de uso para o usuário
        opt = int(input())
        print('\n')

        if opt == 0:
            self.escolheModelo()
        
        if opt in self.dicio.keys():
            modelo = self.dicio[opt]

            for nome in self.listaModelos:
                if modelo.upper() == nome['name'].upper():
                    self.nomeVeiculo = modelo
                    url = self.montaUrl.montar(arg="/veiculo/", idModelo=nome['id'])
        else:
            print("Opção inválida!\nPor favor, tente novamente\n\n")
            self.escolheModeloNaLista()

        self.modelo = self.pegaDados(url)

        self.dicio = {}
        i = 1
        for nome in self.modelo:
            print(str(i) + " - " + nome['name'])
            self.dicio[i] = nome
            i+=1

    def escolheAno(self):
        print("Escolha qual o Ano/Combustível de seu veículo (0 para retornar): ")
        opt = int(input())
        print('\n')

        if opt == 0:
            self.escolheModeloNaLista()

        if opt in self.dicio.keys():
            modelo = self.dicio[opt]
            url = self.montaUrl.montar(arg="/veiculo/", ano=modelo['key'])

            self.ano = self.pegaDados(url)

            self.valorVeiculo = self.ano['preco']
            self.anoVeiculo = int(self.ano['ano_modelo'])

            print('Valor atual do veículo (' + self.nomeVeiculo + '): ' + self.valorVeiculo)
        else:
            print("Opção inválida!\nPor favor, tente novamente\n\n")
            self.escolheAno()
        
    def pegaDados(self, link):
        response = requests.get(link)
        return json.loads(response.content)