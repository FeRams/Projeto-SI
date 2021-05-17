import random
class Loader():
	def __init__ (self):
		#atributo que representa a velocidade em que o carregador faz o carregamento
		#em uma escala de 0 a 100
		self.speed = random.randint(0,100)