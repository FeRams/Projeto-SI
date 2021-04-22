#classe que representa o atendente autônomo do deposito
class Agente:

    def __init__(self, dep, car):
        #vai iniciar no balcao e de maos vazias
        self.estado = "maos vazias" 
        self.entregue = 0
        self.objeto = 0
        self.posicao =[0,0]
        self.setor = "balcao"
        self.carregador = car
        self.deposito = dep
        self.n_ordem = 0

    #funcao que decide a proxima acao do agente
    def prox_acao(self):
        #se estiver ocioso, verifica se o carregador possui um pedido para fazer
        if self.n_ordem == 0:
            self.n_ordem = self.carregador.fazer_pedido()
            print("pedido recebido\n")
        #se estiver no balcao
        elif self.setor == "balcao":
            #fica nesse estado apos entregar caixa ou apos receber pedido
            if self.estado == "maos vazias":
                #vai para as os paletes para pegar uma caixa
                self.ir_para("paletes")
                self.posicao = [0,0]
            else :
                #se ja tiver pego a caixa, a entrega
                self.entregar()
        elif self.setor == "paletes":
            #se acabou de chegar nas paletes, procura a caixa
            if self.estado == "maos vazias":
                self.buscar_caixa()
            else:
                #se ja pegou uma caixa, vai por em uma caixa termica
                self.ir_para("caixas termicas")
        #se esta nas caixas termicas
        elif self.setor == "caixas termicas":
            #se não colocou, coloca
            if self.objeto>0:
                self.colocar_termica()
            else:
                #se ja colocou, vai entregar
                self.ir_para("balcao")
        
    #coloca vacinas na caixa termica
    def colocar_termica (self):
        self.objeto = -self.objeto

    #entrega caixa para o carregador
    def entregar (self):

        print("entregando caixa ", self.objeto, "\n")
        self.carregador.receber_pedido(self.objeto)
        self.objeto = 0
        self.estado = "maos vazias"
        self.n_ordem = self.n_ordem -1

    #vai para um setor diferente
    def ir_para (self, destino):
        print("indo para o setor ", destino, "\n")
        self.setor = destino

    #se descloca entre os paletes
    def andar(self, direcao):
        print("andando: ", direcao, "\n")
        return

    #função de pegar uma caixa na posição pos
    def pegar(self, pos, paletes): 
        self.objeto = paletes[pos[0]][pos[1]]
        paletes[pos[0]][pos[1]] = 0
        print("pegando caixa ", self.objeto, "\n")
        print(paletes, "\n")
        self.estado = "carregando"
        return

    #função de soltar a caixa que está segurando na posição pos
    def soltar(self, pos, paletes):
        paletes[pos[0]][pos[1]] = self.objeto
        print("soltando caixa ", self.objeto, "\n")
        print(paletes, "\n")
        self.objeto = 0
        self.estado = "maos vazias"
        return

    #função utilizada pelo agente para buscar uma caixa no deposito
    def buscar_caixa(self):
        paletes = self.deposito.paletes
        #procura onde está a caixa de menor validade
        aux = self.scan(paletes)
        pos = aux [1]
        #procura a rota a ser percorrida atraves de um algoritmo guloso
        caminho = self.busca_caminho(paletes, pos)
        i = 0
        prox_pos = [0,0]
        #loop para seguir os passos até chegada
        while (i<len(caminho)):
            #se ele não está tendo que retirar uma caixa do caminho, segue as instruções
            if self.estado == "maos vazias":
                if caminho[i] == 'd':
                    prox_pos = [self.posicao[0], self.posicao[1]+1]
                elif caminho[i] == 'u':
                    prox_pos = [self.posicao[0], self.posicao[1]-1]
                elif caminho[i] == 'r':
                    prox_pos = [self.posicao[0]+1, self.posicao[1]]
                elif caminho[i] == 'l':
                    prox_pos = [self.posicao[0]-1, self.posicao[1]]
                #verifica se o caminho está livre
                if paletes [prox_pos[0]] [prox_pos[1]] == 0:
                    #se estiver, anda
                    self.andar (caminho[i])
                    i = i+1
                    self.posicao = prox_pos
                else:
                    #se não estiver, pega a caixa 
                    self.pegar(prox_pos, paletes)
            else:
                #se está movendo uma caixa
                #tenta soltá-la em uma posição que não está no caminho
                if caminho[i] != 'd'and caminho[i-1] !=  'u' and paletes [self.posicao[0]] [self.posicao[1]+1] == 0:
                        self.soltar([self.posicao[0], self.posicao[1]+1], paletes)
                elif caminho[i] != 'u'and caminho[i-1] !=  'd' and paletes [self.posicao[0]] [self.posicao[1]-1] == 0 and self.posicao[1]>0:
                        self.soltar([self.posicao[0], self.posicao[1]-1], paletes)
                elif caminho[i] != 'r'and caminho[i-1] !=  'l' and paletes [self.posicao[0]+1] [self.posicao[1]] == 0:
                        self.soltar([self.posicao[0]+1, self.posicao[1]], paletes)
                elif caminho[i] != 'l'and caminho[i-1] !=  'r' and paletes [self.posicao[0]-1] [self.posicao[1]] == 0:
                        self.soltar([self.posicao[0]-1, self.posicao[1]], paletes)
                else: 
                    #se não houver opção, recua e tenta novamente
                    if self.posicao[0] == 0 and self.posicao[1] ==0:
                        return
                    if caminho[i-1] == 'u':
                        prox_pos = [self.posicao[0], self.posicao[1]+1]
                    elif caminho[i-1] == 'd':
                        prox_pos = [self.posicao[0], self.posicao[1]-1]
                    elif caminho[i-1] == 'l':
                        prox_pos = [self.posicao[0]+1, self.posicao[1]]
                    elif caminho[i-1] == 'r':
                        prox_pos = [self.posicao[0]-1, self.posicao[1]]            
                    i = i-1
                    self.posicao = prox_pos
                    self.andar ('-'+caminho[i])
        #agente chegou até a caixa
        self.pegar(pos, paletes)
        #como a etapa de ida garante que o caminho estará livre, volta seguindo o contrário das instruções
        while (i>1):
            if caminho[i-1] == 'u':
                prox_pos = [self.posicao[0], self.posicao[1]+1]
            elif caminho[i-1] == 'd':
                prox_pos = [self.posicao[0], self.posicao[1]-1]
            elif caminho[i-1] == 'l':
                prox_pos = [self.posicao[0]+1, self.posicao[1]]
            elif caminho[i-1] == 'r':
                prox_pos = [self.posicao[0]-1, self.posicao[1]]            
            i = i-1
            self.posicao = prox_pos
            self.andar ('-'+caminho[i])




    #algoritmo de busca gulosa
    def busca_caminho (self, paletes, pos_cx):
        operacoes = []
        direcao = 'n'
        pos_ag = self.posicao
        while (self.distancia(pos_ag, pos_cx)>1):
            #verifica qual das direções deixa o agente mais próximo do objetivo
            nxt_pos = pos_ag
            dist = 10000
            if pos_ag[1]< self.deposito.y-1:
                aux = [pos_ag[0], pos_ag[1]+1]
                if (paletes [aux[0]][aux[1]] != -1):
                    if self.distancia(aux, pos_cx) <dist:
                        nxt_pos = aux
                        direcao = 'd'
                        dist= self.distancia(aux, pos_cx)
            if pos_ag[1]>0:
                aux = [pos_ag[0], pos_ag[1]-1]
                if (paletes [aux[0]][aux[1]] != -1):
                    if self.distancia(aux, pos_cx) <dist:
                        nxt_pos = aux
                        direcao = 'u'
                        dist = self.distancia(aux, pos_cx)
            if pos_ag[0]<self.deposito.x-1:
                aux = [pos_ag[0]+1,pos_ag[1]]
                if (paletes [aux[0]][aux[1]] != -1):
                    if self.distancia(aux, pos_cx) <dist:
                        nxt_pos = aux
                        direcao = 'r'
                        dist = self.distancia(aux, pos_cx)
            if pos_ag[0]>0:
                aux = [pos_ag[0]-1, pos_ag[1]]
                if (paletes [aux[0]][aux[1]] != -1):
                    if self.distancia(aux, pos_cx) <dist:
                        nxt_pos = aux
                        direcao = 'l'
                        dist = self.distancia(aux, pos_cx)
            pos_ag = nxt_pos
            operacoes.append(direcao)
        return operacoes

    #retorna a distância em passos do robô até a caixa objetivo
    def distancia (self, pos1, pos2):
        return abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1])

        
    #scaneia a área dos paletes e retorna a posição e o valor da caixa com menor validade
    def scan(self, paletes):
        pos = [0,0]
        menor = 1000
        c1 = 0
        c2 = 0
        for i in paletes:
            c2 = 0
            for j in i:
                if j < menor and j >0:
                    pos = [c1,c2]
                    menor = j
                c2 = c2+1
            c1 = c1+1
        return [menor, pos]

    def executar(self):
        while 1:
            while self.n_ordem>0:
                self.prox_acao()
            self.n_ordem = self.carregador.fazer_pedido()
