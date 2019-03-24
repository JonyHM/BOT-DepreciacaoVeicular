# -*- coding: utf-8 -*-

from ConsultaFipe import *
from TesteClasseSwitch import *

class Principal(object):       
    def __init__(self):
        self.consulta = Consulta()
        self.url = self.consulta.url
        self.marcas = self.consulta.marcas

    def start(self):                
        tipos = self.consulta.escolheTipo(self.url)

        for tipo in tipos:
            print(tipo['name'])

        self.consulta.escolheMarca(self.marcas)
        




if __name__ == "__main__":
    main = Principal()
    main.start()