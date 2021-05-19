from matplotlib import pyplot
from environment import Environment
from order import Order
from pair import Pair
import math
import random
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import mpl_toolkits.mplot3d.art3d as art3d
from matplotlib.patches import Rectangle, PathPatch

class Tempera:

    def __init__(self, env, ord):
        #cria uma dupla aleatoria, que sera o ponto de inicio da tempera
        self.pair = Pair()
        #inicializa variaveis de ambiente aleatórias
        self. environment = env
        #inicializa variaveis da ordem de entrega aleatórias
        self.order = ord
        self.tempo =0
        self.iteracoes = 100000
        #inicializa o grafico, com o plot da curva de risco
        self.create_plt()

    #funçao que define o risco dada uma configuração de dupla
    def calcular_risco(self, pair):
        #é formada por dois parabolóides elipricos, cada um define um mínimo local
        #a primeira define um minimo na posição (tempo_de_entrega/6+clima/0.006, tamanho_da_entrega)
        accident = ((pair.driver.speed-(self.order.travel_time)/6-self.environment.weather/0.06)**2 + (pair.loader.speed-self.order.load)**2 +self.environment.time*self.order.load/10)
        #a segunda define um minimo na posição (urgencia^2, tamanho_da_entrega*urgencia/10)
        delay = (((pair.driver.speed-(self.order.urgency**2))**2 + (pair.loader.speed-self.order.load*self.order.urgency/10)**2)+self.order.urgency*self.order.travel_time/300)
        return 1+(accident*delay)

    #TODO retorna um vizinho aleatorio
    def vizinho(self):
        neighbor = Pair()
        #sorteia uma direção possivel para se deslocar
        direction = random.randint(1,4)
        neighbor.driver.speed = self.pair.driver.speed
        neighbor.loader.speed = self.pair.loader.speed
        if (direction ==1 and self.pair.driver.speed<100):
            neighbor.driver.speed = self.pair.driver.speed+1
        elif (direction ==2 and self.pair.driver.speed>0):
            neighbor.driver.speed = self.pair.driver.speed-1
        elif (direction ==3 and self.pair.loader.speed<100):
            neighbor.loader.speed = self.pair.loader.speed+1
        elif (direction ==4 and self.pair.loader.speed>0):
            neighbor.loader.speed = self.pair.loader.speed-1
        return neighbor

    #retorna a temperatura em um determinado tempo
    def scheduler(self):
        return (self.iteracoes-self.tempo)/(self.iteracoes)


    #algoritmo da tempera em si
    def execucao (self):
        menor_risco = self.calcular_risco (self.pair)
        while (self.tempo<self.iteracoes):
            #incrementa o tempo
            self.tempo = self.tempo+1
            #atualiza a temperatura
            self.temperatura = self.scheduler()
            #olha para um vizinho aleatório
            viz = self.vizinho()
            #calcula o risco do vizinho
            risco = self.calcular_risco(viz).real
            diferenca = menor_risco -risco.real
            #se o vizinho for melhor, se desloca para a posição do vizinho
            if diferenca.real >0:
                self.pair = viz
                menor_risco = risco
            else :
                #se o viziho for pior, calcula a chance de se deslocar mesmo assim
                if(not (menor_risco == 0) and self.temperatura>0):
                    #foi utilizada a mesma formula explicada em aula
                    prob = 2.7182**((diferenca/(menor_risco*self.temperatura))) * 100
                    result  = random.randint(0,100)
                    if (result<prob):
                        self.pair = viz
                        menor_risco = risco
            if self.tempo%100==0:
                #a cada 100 iterações, mostra o progresso
                self.ax.scatter(self.pair.driver.speed, self.pair.loader.speed, 1000 + menor_risco, 'red')
        print ("resultado: ",self.pair.driver.speed,",",self.pair.loader.speed," de ", menor_risco, "\n")
        #self.show_results()
        return [self.pair.driver.speed,self.pair.loader.speed,menor_risco]

    def true_min(self):
        min = Pair()
        min.driver.speed = (self.order.travel_time)/6+self.environment.weather/0.06
        min.loader.speed = self.order.load
        zero = self.calcular_risco(min)
        print ("minimo em ",min.driver.speed,",",min.loader.speed," de ", zero, "\n")
        min.driver.speed = (self.order.urgency**2)
        min.loader.speed = self.order.load*self.order.urgency/10
        zero = self.calcular_risco(min)
        print ("minimo em ",min.driver.speed,",",min.loader.speed," de ", zero, "\n")
        return


    #cria o plot do grafico
    def create_plt(self):
        self.fig = plt.figure()
        self.ax = self.fig.gca(projection='3d')
        self.X = np.arange(0, 100, 1)
        self.Y = np.arange(0, 100, 1)
        self.X, self.Y = np.meshgrid(self.X, self.Y)
        self.Z = (((self.X-(self.order.travel_time)/6-self.environment.weather/0.06)**2 + (self.Y-self.order.load)**2 +self.environment.time*self.order.load)*(((self.X-(self.order.urgency**2))**2 + (self.Y-self.order.load*self.order.urgency/10)**2)+self.order.urgency*self.order.travel_time/300))
        surf = self.ax.plot_surface(self.X, self.Y, self.Z, rstride=1, cstride=1, linewidth=1, zorder=100)
        return

    #função que manda mostrar o grafico na tela
    def show_results(self):
        plt.show()
        return



    
