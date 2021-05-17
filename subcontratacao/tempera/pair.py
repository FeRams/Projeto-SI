from loader import Loader
from motorista import Driver
class Pair():
	def __init__ (self):
		#uma dupla é formada por um motorista e um carregador
		self.loader = Loader()
		self.driver = Driver()
