import random
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

def get_distance(unid1, unid2):
    margem = random.randint(80, 120) / 100
    return round(margem*TIMES[unid1][unid2],1)

unidades = """
RODOVIARIA
Rua Realeza 259
Rua Romeu Bach 80
Avenida Erasto Gaertner 797
Rua Pedro Bochino 750
Rua Des. Cid Campelo 8060
Rua Jaime Reis 331
Rua Conde dos Arcos 295
Rua Divina Providência 1445
Rua José Casagrande 220
R. Adriana Ceres Zago Bueno 1350
"""

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
class GeneticAlgo():
    
    def __init__(self,hash_map,start,steps=2,crossover_prob=0.15,mutation_prob=0.15,population_size=5,iterations=100):
        self.crossover_prob=crossover_prob
        self.mutation_prob=mutation_prob
        self.population_size=population_size
        self.hash_map = hash_map
        self.steps = steps
        self.iterations = iterations
        self.start = start
        self.cities = [k for k in self.hash_map.keys()] 
        self.cities.remove(start)
        self.genes = []
        self.epsilon = 1 - 1/self.iterations        
        self.generate_genes = vectorize(self.generate_genes)
        self.evaluate_fitness = vectorize(self.evaluate_fitness)
        self.evolve = vectorize(self.evolve)
        self.prune_genes = vectorize(self.prune_genes)
        self.converge = vectorize(self.converge)

        
        self.generate_genes()
        
    def generate_genes(self):
        for i in range(self.population_size):
            gene = [self.start]
            options = [k for k in self.cities]
            while len(gene) < len(self.cities)+1:
                city = random.choice(options)
                loc = options.index(city)
                gene.append(city)
                del options[loc]
            gene.append(self.start)
            self.genes.append(gene)
        return self.genes
    
    def evaluate_fitness(self):
        fitness_scores = []
        for gene in self.genes:
            total_distance = 0
            for idx in range(1,len(gene)):
                city_b = gene[idx]
                city_a = gene[idx-1]
                try:
                    dist = self.hash_map[city_a][city_b]
                except:
                    dist = self.hash_map[city_b][city_a]
                total_distance += dist
            fitness = 1/total_distance
            fitness_scores.append(fitness)
        return fitness_scores
    
    def evolve(self):
        index_map = {i:'' for i in range(1,len(self.cities)-1)}
        indices = [i for i in range(1,len(self.cities)-1)]
        to_visit = [c for c in self.cities]
        cross = (1 - self.epsilon) * self.crossover_prob
        mutate = self.epsilon * self.mutation_prob 
        crossed_count = int(cross * len(self.cities)-1)
        mutated_count = int((mutate * len(self.cities)-1)/2)
        for idx in range(len(self.genes)-1):
            gene = self.genes[idx]
            for i in range(crossed_count):
                try:
                    gene_index = random.choice(indices)
                    sample = gene[gene_index]
                    if sample in to_visit:
                        index_map[gene_index] = sample
                        loc = indices.index(gene_index)
                        del indices[loc]
                        loc = to_visit.index(sample)
                        del to_visit[loc]
                    else:
                        continue
                except:
                    pass
        last_gene = self.genes[-1]
        remaining_cities = [c for c in last_gene if c in to_visit]
        for k,v in index_map.items():
            if v != '':
                continue
            else:
                city = remaining_cities.pop(0)
                index_map[k] = city
        new_gene = [index_map[i] for i in range(1,len(self.cities)-1)]
        new_gene.insert(0,self.start)
        new_gene.append(self.start)
        for i in range(mutated_count):
            choices = [c for c in new_gene if c != self.start]
            city_a = random.choice(choices)
            city_b = random.choice(choices)
            index_a = new_gene.index(city_a)
            index_b = new_gene.index(city_b)
            new_gene[index_a] = city_b
            new_gene[index_b] = city_a
        self.genes.append(new_gene)
                
    def prune_genes(self):       
        for i in range(self.steps):
            self.evolve()
        fitness_scores = self.evaluate_fitness()
        for i in range(self.steps):
            worst_gene_index = fitness_scores.index(min(fitness_scores))
            del self.genes[worst_gene_index]
            del fitness_scores[worst_gene_index]
        return max(fitness_scores),self.genes[fitness_scores.index(max(fitness_scores))]
    
    def converge(self):
        for i in range(self.iterations):
            values = self.prune_genes()
            current_score = values[0]
            current_best_gene = values[1]
            self.epsilon -= 1/self.iterations
            if i % 100 == 0:
                print(f"{int(1/current_score)} minutos")
                
        return current_best_gene

g = GeneticAlgo(hash_map=dist_dict,start='RODOVIARIA',mutation_prob=0.25,crossover_prob=0.25,
                 population_size=30,steps=15,iterations=2000)
g.converge()