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
        self.consulta.ecolheModeloNaLista()
        self.consulta.escolheAno()
        
if __name__ == "__main__":
    main = Main()
    main.start()

## TODO: tratamento de erros de input de usuários
## 
# 