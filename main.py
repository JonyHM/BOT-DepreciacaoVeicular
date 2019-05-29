#!/usr/bin/env python3.7
# encoding: utf-8

from ConsultaFipe import ConsultaFipe
from BotTelegram import App

class Main(object):       
    def __init__(self):
        # self.consulta = ConsultaFipe()
        self.bot = App()

    def start(self):                
        self.bot.main()
        # self.consulta.escolheTipo()
        # self.consulta.escolheMarca()
        # self.consulta.escolheModelo()
        # self.consulta.escolheModeloNaLista()
        # self.consulta.escolheAno()
        
if __name__ == "__main__":
    main = Main()
    main.start()

## TODO: 

# separar classes para input -> modelar
# Melhorar workflow de chamadas de classes. -> MVC
# Bot telegram api -> Continuar