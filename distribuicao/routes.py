import random
import matplotlib.pyplot as plt
import numpy as np

plt_alg_gen = []

#tabela de tempos de deslocamento entre cada unidade. posição [0,3], por exemplo,
#representa o tempo para ir do depósito até o Bacacheri
TIMES = [
   [0,  25, 16, 10,  9, 24,  9, 14, 16, 15, 28],
   [25,  0, 16, 31, 24, 16, 27, 16, 22, 29, 13],
   [16, 16,  0, 22, 13, 25, 20, 13, 24, 25, 26],
   [10, 31, 22,  0, 15, 31, 12, 19, 22, 13, 33],
   [9,  24, 13, 15,  0, 26, 16, 14, 20, 21, 28],
   [24, 16, 25, 31, 26, 0,  20, 15,  9, 19, 16],
   [9,  27, 20, 12, 16, 20,  0, 16, 14,  7, 29],
   [14, 16, 13, 19, 14, 15, 16,  0, 12, 18, 18],
   [16, 22, 24, 22, 20, 9,  14, 12,  0, 15, 23],
   [15, 29, 25, 13, 21, 19,  7, 18, 15,  0, 29],
   [28, 13, 26, 33, 28, 16, 29, 18, 23, 29,  0]
]

#função que insere uma variação de até 20% no tempo de deslocamento
#simula atraso com trânsito, por exemplo
def get_distance(unid1, unid2):
    margem = random.randint(80, 120) / 100
    return round(margem*TIMES[unid1][unid2],1)

unidades = """
Depósito
Sao João Del Rey
Waldemar Monastier
Bacacheri
Cajuru
São Miguel
Mãe Curitiba
Fanny Lindóia
Santa Quitéria
Bom Pastor
Santa Rita
"""

#cria a tabela com as variações
unidades = [u for u in unidades.split('\n') if u != '']
edges = []
dist_dict = {u:{} for u in unidades}
for idx_1 in range(0,len(unidades)-1):
    for idx_2 in range(idx_1+1,len(unidades)):
        unid_a = unidades[idx_1]
        unid_b = unidades[idx_2]
        dist = get_distance(idx_1,idx_2)
        dist_dict[unid_a][unid_b] = dist
        edges.append((unid_a,unid_b,dist))

from numpy import vectorize

#classe que implementa o algoritmo genétic
class GeneticAlgo():
    
    #inicialização da classe
    def __init__(self,time_map,start,crossover_prob=10,mutation_prob=0.05,population_size=5,iterations=100):
        #representa o número de crossovers que serão realizados por geração
        self.number_of_crossovers = crossover_prob
        #somatório do fitness de todos os cromossomos. é utilizado na seleção
        self.total_fitness = 0
        #guarda o fitness dos cromossomos
        self.fitness_scores = []
        #probabilidade de mutação
        self.mutation_prob=mutation_prob
        #tamanho da população
        self.population_size=population_size
        #mapa dos tempos explicado acima
        self.time_map = time_map
        #totalde gerações que serão analisadas
        self.iterations = iterations
        #marca o local de inicío e fim do trajeto, que é fixo
        self.start = start
        #lista dos centros de saude
        self.centers = [k for k in self.time_map.keys()] 
        self.centers.remove(start)
        #lista de cromossomos pertencentes à geração atual
        self.crom = []      
        self.generate_crom = vectorize(self.generate_crom)
        self.evaluate_fitness = vectorize(self.evaluate_fitness)
        self.evolve = vectorize(self.evolve)
        self.prune_crom = vectorize(self.prune_crom)
        self.converge = vectorize(self.converge)

        
        self.generate_crom()

    #cria um cromossomo aleatório
    def generate_crom(self):
        for i in range(self.population_size):
            cromossom = [self.start]
            options = [k for k in self.centers]
            while len(cromossom) < len(self.centers)+1:
                center = random.choice(options)
                loc = options.index(center)
                cromossom.append(center)
                del options[loc]
            cromossom.append(self.start)
            self.crom.append(cromossom)
        return self.crom
    
    #função que avalia o tempo de deslocamento da combinação descrita por cada cromossomo
    def evaluate_fitness(self):
        self.total_fitness = 0
        fitness_scores = []
        for cromossom in self.crom:
            total_distance = 0
            for idx in range(1,len(cromossom)):
                center_b = cromossom[idx]
                center_a = cromossom[idx-1]
                try:
                    dist = self.time_map[center_a][center_b]
                except:
                    dist = self.time_map[center_b][center_a]
                total_distance += dist
            fitness = 1/total_distance
            self.total_fitness = self.total_fitness + fitness
            fitness_scores.append(fitness)
        return fitness_scores
    
    #função que realiza a seleção dos cromossomos para a reprodução
    def roleta(self, crom, fitness):
        sorteado = random.uniform(0, self.total_fitness)
        acumulado = 0
        #sorteia um cromossomo
        #a chance de ser escolhido é proporcional à seu fitness
        for i in range (0, len(crom)-1):
            acumulado = acumulado + fitness[i]
            if sorteado<acumulado:
                return i
        return -1          

    #operador de crossover
    def crossover_PMX (self, pai1, pai2, filho1, filho2):
        #sorteia um segmento para fazer a cópia
        inicio = random.randint (0, len(pai1)-1)
        fim = random.randint(inicio, len(pai1)-1)
        #faz a cópia (entre os pais alternados) do segmento sorteado 
        for i in range (0,len(pai1)):
            if (i<inicio or i>fim):
                filho1.append('')
                filho2.append('')
            else:
                filho1.append(pai2[i])
                filho2.append(pai1[i])
        #copia para os filhos os genes que podem ter sua posição mantida
        for i in range (0,len(pai1)):
            if (not(pai1[i]in filho1)and filho1[i] == ''):
                filho1[i] = pai1[i]
            if (not(pai2[i]in filho2) and filho2[i] == ''):
                filho2[i] = pai2[i]
        #para o restante dos genes, faz um mapeamento repetido até que possa inserir
        for i in range (0,len(pai1)):
            k = i
            while 1:
                if (not(pai1[i]in filho1)):
                    if (not (filho1[k] == '')):
                        k = pai1.index(filho1[k])
                    else:
                        filho1[k] = pai1[i]
                        break    
                else:
                    break                     
            k = i
            while 1:
                if (not(pai2[i]in filho2)):
                    if (not (filho2[k] == '')):
                        k = pai2.index(filho2[k])
                    else:
                        filho2[k] = pai2[i]
                        break           
                else:
                    break  

    #operador de mutação
    def mutacao (self, cromossom):
        sorteado = random.randint(0,100)
        #sorteia se vai ou não haver permutação no cromossomo analisado
        if sorteado < self.mutation_prob:
            #se houver mutação, sorteia dois genes e troca eles de lugar
            i = random.randint (0, len(cromossom)-1)
            j = random.randint(0, len(cromossom)-1)
            aux = cromossom[i]
            cromossom[i]= cromossom[j]
            cromossom[j] = aux            

    #função que engloba a criação da nova geração
    def evolve(self):
        aux = self.crom.copy()
        aux_fitness = self.fitness_scores.copy()
        parents = []
        #chama a seleção até que todos os pais tenham sido escolhidos
        for i in range(0,(self.number_of_crossovers*2)):
            new_parent = self.roleta(aux, aux_fitness)
            parents.append (aux[new_parent])
            self.total_fitness = self.total_fitness - aux_fitness[new_parent]
            del aux_fitness[new_parent]
            del aux[new_parent]
            self.total_fitness = self.total_fitness
        #vai gerar os novos cromossomos a partir dos pais escolhidos
        for i in range(0, self.number_of_crossovers):
            filho1 = []
            filho2 = []
            #retira a parte fixa dos trajeto dos cromossomos na parte de permutação e mutação
            del parents[i][0]
            del parents[i][10]
            del parents[i+1][0]
            del parents[i+1][10]
            #chama o crossover
            self.crossover_PMX(parents[i], parents[i+1], filho1, filho2)
            #chama a mutação
            self.mutacao(filho1)
            self.mutacao(filho2)
            #insere novamente a parte fixa
            parents[i].insert(0,self.start)
            parents[i].append(self.start)
            parents[i+1].insert(0,self.start)
            parents[i+1].append(self.start)
            filho1.insert(0,self.start)
            filho1.append(self.start)
            filho2.insert(0,self.start)
            filho2.append(self.start)
            #inssere os novos filhos na fila de cromossomos
            self.crom.append(filho1)
            self.crom.append(filho2)
        

    #elimina os individuos menos adaptados
    def prune_crom(self):       
        self.fitness_scores = self.evaluate_fitness()
        self.evolve()
        self.fitness_scores = self.evaluate_fitness()
        while(len(self.crom)>30):
            worst_cromossom_index = self.fitness_scores.index(min(self.fitness_scores))
            del self.crom[worst_cromossom_index]
            del self.fitness_scores[worst_cromossom_index]
        return max(self.fitness_scores),self.crom[self.fitness_scores.index(max(self.fitness_scores))]
    
    def converge(self):
        #executa o algoritmo no numero de iterações definidas
        for i in range(self.iterations):
            values = self.prune_crom()
            current_score = values[0]
            current_best_cromossom = values[1]
            plt_alg_gen.append(1/current_score)
            #imprime o resultado a cada 25 gerações
            if i % 25 == 0:
                print(f"{int(1/current_score)} minutos")
        print(*current_best_cromossom, sep = ", ")
        return current_best_cromossom


def greedy():
    current = unidades[0]
    total = 0
    result = [unidades[0]]
    for i in range (0,10):
        min = 50
        next = -1
        for j in unidades:
            dist = 50
            if (current != j):
                try:
                    dist = dist_dict[current][j]
                except:
                    dist = dist_dict[j][current]
            if (not(j in result) and dist<min):
                min = dist
                next = j
        if not (next in result):
            result.append(next)
            total += min
            current = next
    result.append(unidades[0])
    try:
        total += dist_dict[unidades[0]][current]
    except:
        total += dist_dict[current][unidades[0]]
    return total

        

def show_progression():
    plt.plot (plt_alg_gen, "-g", label = "genetico")
    greedy_result = greedy()
    greedy_plt = []
    for i in plt_alg_gen:
        greedy_plt.append(greedy_result)
    plt.plot(greedy_plt, "-b", label="greedy")
    plt.legend(loc="upper right")
    plt.show()

g = GeneticAlgo(time_map=dist_dict,start='Depósito',mutation_prob=0.05,crossover_prob=10,
                 population_size=30, iterations=500)
g.converge()

show_progression()

