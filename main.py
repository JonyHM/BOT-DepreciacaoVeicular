# -*- coding: utf-8 -*-

from models.ConsultaFipe import ConsultaFipe

class Main(object):       
    def __init__(self):
        self.consulta = ConsultaFipe()

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

# Classe para montar url -> Terminar
# separar classes para input -> modelar
# Melhorar workflow de chamadas de classes. -> MVC
# Bot telegram api -> Continuar