# -*- coding: utf-8 -*-

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
    
    def switchMarcas(self, option, marcas):
        ## Teste de tabela com as marcas (Ta meio cagado msm)
        print("Escolha uma marca: \n") 

        print()
        count = 1    
        print('{:<}{:-^121}{:<}'.format('|', '-', '|'))
        for marca in self.marcas:
            print('{:<}{:^11}'.format('|', marca['name']), end="")

            if(marca['name'] == self.marcas[len(marcas)-1]['name']):
                print("\n")
            
            if count == 10:
                print('{:>}'.format('|'), end="")
                print("\n")
                count = 0
            count += 1
        print('{:<}{:-^121}{:<}'.format('|', '-', '|'))

        switcher = {
            
        }