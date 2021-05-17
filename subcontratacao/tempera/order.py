import random
class Order():
    def __init__ (self):
		#atributo que representa o tamanho da carga da entrega
		#em uma escala de 0 a 100
        self.load = random.randint (0,100)
		#atributo que representa o tempo esperado para a entrega
		#minimo de 150, maximo de 300 minutos
        self.travel_time = random.randint (150,300)
		#atributo que representa a urgencia da entrega
		#em uma escala de 0 a 10
        self.urgency = random.randint (0,10)