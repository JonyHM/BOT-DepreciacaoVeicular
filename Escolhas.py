# encoding: utf-8

# Esta classe será destinada aos inputs do usuário
class Escolhas(object):   

    def switchTipo(self, option):
        switcher = {
            1: "carros",
            2: "motos",
            3: "caminhoes",
            0: "SAIR"
        }
        return switcher.get(option, "invalido")