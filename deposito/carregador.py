#import random

class Carregador:

    def __init__(self):
        self.n_caixas = 5    

    def fazer_pedido(self):
        #return randint(1,5)
        self.n_caixas = int(input())
        return self.n_caixas

    def receber_pedido(self, caixa):
        return