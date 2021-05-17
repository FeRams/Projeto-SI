import random
class Environment():
	def __init__ (self):
		#representa as condições climaticas no momento da entrega
		#1-> ceu limpo, 2-> chuvoso, 3-> neblina
		self.weather = random.randint (1,3)
		#representa o horario do dia
		#1-> dia, 2-> noite
		self.time = random.randint (1,2)
