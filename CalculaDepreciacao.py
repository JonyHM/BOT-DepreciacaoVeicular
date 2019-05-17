from datetime import datetime

ano = 2009
valorVeiculo = 'R$ 20.570,00'
anoAtual = datetime.now().year
idadeCarro = anoAtual - ano
caracteres = ' R$.'

valorVeiculo = valorVeiculo.split(',')
valorVeiculo = valorVeiculo[0]

for i in range(0, len(caracteres)):
    valorVeiculo = valorVeiculo.replace(caracteres[i], '')

valorVeiculo = int(valorVeiculo)

if idadeCarro > 5:
    print('Veiculo "usado"\n')
    valorVeiculo -= valorVeiculo * 0.1
    print('\nSeu veículo valerá, aproximadamente R$' + str(valorVeiculo))
        ## Como seu veículo tem mais de 5 anos, o cálculo de depreciação realizado é 
        # de -10% do valor atual anualmente
else:
    print('Seu veículo começará a depreciar efetivamente a partir de 5 anos de fabricação: ' + str(ano+5))