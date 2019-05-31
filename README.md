# BOT-DepreciacaoVeicular
Bot desenvolvido na disciplina de Interação Humano-Computador (IHC) da FATEC SJC.
O intuito do BOT é buscar o valor atual do seu veículo na tabela Fipe, e calcular a depreciação anual dele, de acordo com regras utilizadas por concessionárias e comerciantes de veículos brasileiros.

## Dependências
Instalar **requests** para requisições REST na aplicação e **python-telegram-bot** para comunicação com o telegram.

`python -m pip install requests python-telegram-bot`

## Utilização 
Digite **/oi** ou **/ola** para iniciar o BOT. 

Após o início, as instruções para visualização do valor do veículo e sua depreciação serão enviadas quando necessário.

### Tabela FIPE
Oferece a média de valores dos veículos vendidos no mercado nacional e serve apenas como parâmetro, uma vez que valores de revenda variam de acordo com conservação, cor oferta e demanda do veículo.

### Depreciação
O cálculo é realizado em veículos com mais de 5 anos de fabricação, cálculo médio realizado pela maioria das concessionárias brasileiras. 
Nele, após 5 anos de fabricação, o veículo pode depreciar até 10% de seu valor atual no ano seguinte.
Entretando, diversos fatores modificam esta conta e podem aumentar ou diminuir drasticamente o valor apresentado pelo BOT, portanto, assim como a tabela FIPE, este BOT funciona como um parâmetro.