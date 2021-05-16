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

    def __init__(self):
        self.pair = Pair()
        self. environment = Environment()
        self.order = Order()
        self.tempo =0
        self.iteracoes = 1000
        self.create_plt()

    #TODO definir calculo da funcao
    def calcular_risco(self, pair):
        #accident = math.sqrt(abs(pair.driver.speed * self.order.travel_time*(self.environment.weather * self.environment.time)/600 + pair.loader.speed* self.order.load/100))
        #delay = -(pair.driver.speed**(self.order.travel_time/300))+ accident* self.order.travel_time/100 - pair.loader.speed* self.order.load/100
        #risk = accident + delay * (self.order.urgency**2)/100
        #return abs(risk)
        accident = ((pair.driver.speed-(self.order.travel_time)/150-self.environment.weather/0.6)**2 + (pair.loader.speed-self.order.load)**2 +self.environment.time*self.order.load)
        delay = (((pair.driver.speed-(self.order.urgency**2)/10)**2 + (pair.loader.speed-self.order.load*self.order.urgency/100)**2)+self.order.urgency*self.order.travel_time/300)
        return 1+ (accident*delay)

    #TODO retorna um vizinho aleatorio
    def vizinho(self):
        neighbor = Pair()
        direction = random.randint(1,4)
        neighbor.driver.speed = self.pair.driver.speed
        neighbor.loader.speed = self.pair.loader.speed
        if (direction ==1):
            neighbor.driver.speed = self.pair.driver.speed+1
        elif (direction ==2):
            neighbor.driver.speed = self.pair.driver.speed-1
        elif (direction ==3):
            neighbor.loader.speed = self.pair.loader.speed+1
        elif (direction ==4):
            neighbor.loader.speed = self.pair.loader.speed-1
        return neighbor

    #retorna a temperatura em um determinado tempo
    def scheduler(self):
        return (self.iteracoes-self.tempo)/(self.iteracoes)


    #algoritmo da tempera em si
    def execucao (self):
        menor_risco = self.calcular_risco (self.pair)
        while (self.tempo<self.iteracoes):
            self.tempo = self.tempo+1
            self.temperatura = self.scheduler()
            viz = self.vizinho()
            risco = self.calcular_risco(viz).real
            diferenca = menor_risco -risco.real
            if diferenca.real >0:
                self.pair = viz
                menor_risco = risco
            else :
                if(not (menor_risco == 0)):
                    prob = 2.7182**((diferenca/(menor_risco))-self.temperatura) * 100
                    result  = random.randint(0,100)
                    if (result<prob):
                        self.pair = viz
                        menor_risco = risco
            if self.tempo%10==0:
                self.ax.scatter(self.pair.driver.speed, self.pair.loader.speed, menor_risco, 'red')
        print (self.pair.driver.speed,"\n")
        print (self.pair.loader.speed,"\n")
        print (menor_risco,"\n")
        self.show_results()

    def create_plt(self):
        self.fig = plt.figure()
        self.ax = self.fig.gca(projection='3d')
        self.X = np.arange(0, 100, 1)
        self.Y = np.arange(0, 100, 1)
        self.X, self.Y = np.meshgrid(self.X, self.Y)
        self.Z = 1+ (((self.X-(self.order.travel_time)/150-self.environment.weather/0.6)**2 + (self.Y-self.order.load)**2 +self.environment.time*self.order.load)*((self.X-(self.order.urgency**2)/10)**2 + (self.Y-self.order.load*self.order.urgency/100)**2)+self.order.urgency*self.order.travel_time/300)
        surf = self.ax.plot_surface(self.X, self.Y, self.Z, rstride=1, cstride=1, linewidth=1, zorder=100)
        return

    def show_results(self):
        plt.show()
        return



    
