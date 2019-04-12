# -*- coding: utf-8 -*-

from ConsultaFipe import *
from TesteClasseSwitch import *

class Main(object):       
    def __init__(self):
        self.consulta = Consulta()

    def start(self):                

        self.consulta.escolheTipo()
        self.consulta.escolheMarca()
        self.consulta.escolheModelo()
        self.consulta.escolheModeloNaLista()
        self.consulta.escolheAno()
        
if __name__ == "__main__":
    main = Main()
    main.start()

## TODO: 

# separar classes para input
# Classe para montar url
# Melhorar workflow de chamadas de classes.