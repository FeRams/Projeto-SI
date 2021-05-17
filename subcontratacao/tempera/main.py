# -*- main generico -*-
from order import Order
from environment import Environment
from tempera import Tempera
from pair import Pair
import math

environment = Environment()
order = Order()
tempera  = Tempera(environment, order)

#gera duplas aleatorias
duplas = []
for i in range (0,20):
    duplas.append(Pair())
    print ("dupla ",i ,", motorista: ",duplas[i].driver.speed, ", carregador: ",duplas[i].loader.speed, "\n" )


#acha uma estimativa do ótimo atravez do algoritmo de tempera simulada
tempera.true_min()
otimo = tempera.execucao()

#procura qual a dupla que mais se aproxima do ótimo
for i in range (0,20):
    proximidade = math.sqrt((duplas[i].driver.speed-otimo[0])**2 + (duplas[i].loader.speed-otimo[1])**2)
    if i ==0:
        melhor = [i,proximidade]
    elif proximidade < melhor[1]:
        melhor = [i,proximidade]
#decide o quanto vai pagar para a dupla contratada de acordo com o quanto se aproximou do ótimo estimado
#o valor maximo a ser pago é 100
custo = 100*(1- melhor[1]/(100*math.sqrt(2)))
print ("dupla escolhida: ",melhor[0] ,"(motorista: ",duplas[melhor[0]].driver.speed, ", carregador: ",duplas[melhor[0]].loader.speed, ")\n" )
print ("foi pago: ", custo, "\n" )
#plota o grafico com os pontos que mostram o avanço da têmpera
tempera.show_results()