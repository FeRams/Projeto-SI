from agente import Agente 
from carregador import Carregador
from deposito import Deposito

deposito = Deposito()
carregador = Carregador()
agente = Agente (deposito, carregador)
agente.executar()
1