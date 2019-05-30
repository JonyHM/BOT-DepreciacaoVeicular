#!/usr/bin/env python3.7
# encoding: utf-8

import json, requests
from MontaUrl import MontaUrl

## Modelo de fluxo para ser implementaqdo no Bot

### Vai apenas interagir com a API da tabela FIPE
class ConsultaFipe(object):    
    
    def __init__(self):
        self.montaUrl = MontaUrl()
        self.nomeVeiculo = ''
        self.valorVeiculo = ''
        self.anoVeiculo = 0
        self.opt = ''

        self.marcas = [] 
        self.modelos = []
        self.modelo = []
        self.listaModelos = []
        self.dicio = {}
        self.ano = []
        
    def escolheTipo(self, opt):         
        self.opt = opt

        # Fazendo a requisição GET na API da tabela FIPE e transformando em objeto python com a lib json
        url = self.montaUrl.montar(arg='/marcas', tipoVeiculo=self.opt)

        if not self.marcas:
            self.marcas = self.pegaDados(url)

        return True

    def escolheMarca(self, marca):

        for nome in self.marcas:
            if marca.upper() == nome['name'].upper():
                url = self.montaUrl.montar(arg='/veiculos/', idMarca=nome['id'])
                break

        if marca.upper() not in self.modelos:
            self.modelos = []
            try:
                self.modelos = self.pegaDados(url)
            except: #retirar a mensagem e chamar o metodo denovo no bot
                return u'\nMarca não reconhecida!\n\
                    Por favor, digite novamente\n\n'

        return True

    def escolheModelo(self, mod):

        # if modelo.upper() == 'R':
        #     ok = self.escolheMarca()
        #     if ok:
        #         self.escolheModelo()

        # Percorre a lista de modelos e verifica se o input do usuário é igual ao nome do modelo, ambos em upper case e o 
        #adiciona na lista de modelos para exibição futuramente
        for modelo in self.modelos:
            if mod.upper() in modelo['name'].upper() and modelo not in self.listaModelos:
                self.listaModelos.append(modelo)

        return self.listaModelos

    def escolheModeloNaLista(self, opt, dicio):
        # ok = False

        # Imprime os modelos com o nome informado, cada um com índice. Depois atrela esse índice com a marca em um dicionario
        # if self.listaModelos:
        #     i = 1
        #     for nome in self.listaModelos:
        #         print(str(i) + " - " + nome['name'])
        #         self.dicio[i] = nome['name']
        #         i+=1
        # else:
        #     print(u'Modelo não reconhecido!\n\
        #         Por favor, digite novamente\n\n')
        #     self.listaModelos = []
        #     self.escolheModelo()

        # print(u'\nEscolha o número correspondente ao seu veículo (0 para retornar): ') ## Dar um exemplo de uso para o usuário
        # opt = int(input())
        # print('\n')

        # if opt == 0:
        #     ok = self.escolheModelo()
        #     if ok:
        #         self.escolheModeloNaLista() 
        self.dicio = dicio
        opt = int(opt)    
        if opt in self.dicio.keys():
            modelo = self.dicio[opt]

            for nome in self.listaModelos:
                if modelo.upper() == nome['name'].upper():
                    self.nomeVeiculo = modelo
                    url = self.montaUrl.montar(arg="/veiculo/", idModelo=nome['id'])
            self.modelo = self.pegaDados(url)
        else:
            return u'\nOpção inválida!\n\
                Por favor, tente novamente\n\n'

        return self.modelo

        # self.dicio = {}
        # i = 1
        # for nome in self.modelo:
        #     print(str(i) + " - " + nome['name'])
        #     self.dicio[i] = nome
        #     i+=1

        # return True

    def escolheAno(self, opt, dicio):
        # ok = False

        # print(u'\nEscolha qual o Ano/Combustível de seu veículo (0 para retornar): ')
        # opt = int(input())
        # print('\n')

        # if opt == 0:
        #     ok = self.escolheModelo()
        #     if ok:
        #         self.escolheModeloNaLista()

        self.dicio = dicio

        opt = int(opt)

        if opt in self.dicio.keys():
            veiculo = self.dicio[opt]
            url = self.montaUrl.montar(arg="/veiculo/", ano=veiculo['key'])

            self.ano = self.pegaDados(url)

            self.valorVeiculo = self.ano['preco']
            self.anoVeiculo = int(self.ano['ano_modelo'])

            print(u'Valor atual do veículo (' + self.nomeVeiculo + u'): ' + self.valorVeiculo)
            return [self.valorVeiculo, self.anoVeiculo, self.nomeVeiculo]
        else:
            return u'\nOpção inválida!\n\
                Por favor, tente novamente\n\n'
            # self.escolheAno()
        
    def pegaDados(self, link):
        response = requests.get(link)
        return json.loads(response.content)