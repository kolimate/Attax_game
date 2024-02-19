from copy import deepcopy
import pygame
import numpy as np
import math
import time
WIDTH,HEIGHT=760,760
win = pygame.display.set_mode((WIDTH, HEIGHT))#inica a parte grafica

Black=(0,0,0)
Yellow =(204,204,0)
Red =(255,0,0)
Blue=(0,0,255)
Ciano =(0,255,255)
Cianoc =(0,200,255)
Gray =(64,64,64)
White =(255,255,255)
Lightgray=(77,77,77)
poss = []

def createboard(tab):#cria o tabuleiro
    a = -1
    b =0
    fich = 'tabuleiro' + str(tab) + ".txt"
    with open(fich) as line:
        for i in line:
            if a ==-1:
                NQ = int(i)
                board =np.array([[0]*NQ]*NQ)
            for x in i:
                if x == '0' or x=='1' or x== '2' or x =='8':
                    board[a][b] = int(x)
                    b += 1
                elif x== '\n':
                    a =a+1
                    b=0
    return NQ,board

def draw_board(NB,tamqua,board,extra):#desenha o tabuleiro
    win.fill(White)
    for l in range(NB):
        for c in range(NB):
            if board[l][c] == 1:
                 pygame.draw.circle(win, Cianoc,(int(tamqua/2) + c*tamqua,int(tamqua/2) + l*tamqua),int(tamqua/2)-8)
            elif board[l][c] == 2:
                 pygame.draw.circle(win, Yellow,(int(tamqua/2) + c*tamqua,int(tamqua/2) + l*tamqua),int(tamqua/2)-8)
            elif board[l][c] == 8:
                pygame.draw.rect(win, Black, (c*tamqua, l*tamqua , tamqua, tamqua))
    for i in range(NB):
        pygame.draw.line(win,Black,(0,i*tamqua),(WIDTH,i*tamqua ))
        pygame.draw.line(win,Black,(i*tamqua,0),(i*tamqua,HEIGHT ))
    if extra ==1:
        myfont = pygame.font.SysFont(None,80)
        textsurface = myfont.render('Escolhe o tabuleiro', True, Yellow)
        tex = textsurface.get_rect(center=(WIDTH/2,HEIGHT/2))
        win.blit(textsurface,tex)
        myfont = pygame.font.SysFont(None,30)
        textsurface = myfont.render('(<-/-> para escolher, Rato para selecionar)', True, Yellow)
        tex = textsurface.get_rect(center=(WIDTH/2,(HEIGHT/2)+200))
        win.blit(textsurface,tex)
    pygame.display.update()

def draw_piece(c,l,tamqua,jog):#desanha as pecas
    if jog ==1:
        pygame.draw.circle(win, Cianoc,(int(tamqua/2) + c*tamqua,int(tamqua/2) + l*tamqua),int(tamqua/2)-8)
    else:
        pygame.draw.circle(win, Yellow,(int(tamqua/2) + c*tamqua,int(tamqua/2) + l*tamqua),int(tamqua/2)-8)
    pygame.display.update()

def tuapeca(col,lin,jog,board):#verifica se a peca Ã© do jogador
    if board[lin,col] == jog:
        return True
    else:
        return False

def dist(valor1,valor2):#calcula a distancia entre dois pontos
    return(int(math.sqrt((valor1[0]-valor2[0])**2 + (valor1[1]-valor2[1])**2)))

def todapecas(jog,board):#faz uma lista com as posicoes de todas as pecas de um jogador
    todapecas = []
    for l in range(li):
        for c in range(co):
            if board[l][c] == jog:
                todapecas.append([l,c])
    return todapecas

def possimoves(col,lin,board):#movementos possiveis de uma peca
    poss =[]
    for l in range(li):
        for c in range(co):
            if board[l][c]== 0 and (dist((lin,col),(l,c))>0 and dist((lin,col),(l,c)) <3):
                poss.append([l,c])
    return poss

def draw_posi(poss):#desenhas os lugares possiveis de mover uma peca
    for i in poss:
        pygame.draw.circle(win, Blue,(int(tamqua/2) + i[1]*tamqua,int(tamqua/2) + i[0]*tamqua),int(tamqua/2)-int((tamqua/5)*2))
    pygame.display.update()

def move(ini,fin,jog,board):#move uma peca no tabuleiro tanto na matriz como no tabuleiro
    if dist(ini,fin) ==1:
        draw_piece(fin[1],fin[0],tamqua,jog)
        board[fin[0]][fin[1]] = board[ini[0]][ini[1]]
    else:
        draw_piece(fin[1],fin[0],tamqua,jog)
        board[fin[0]][fin[1]] = board[ini[0]][ini[1]]
        board[ini[0]][ini[1]] = 0
        apagar(ini,board)
    adja(fin,jog,board)

def movebot(ini,fin,jog,board):#move uma peca no tabuleiro na matriz
    if dist(ini,fin) ==1:
        board[fin[0]][fin[1]] = board[ini[0]][ini[1]]
    else:
        board[fin[0]][fin[1]] = board[ini[0]][ini[1]]
        board[ini[0]][ini[1]] = 0
    adjabot(fin,jog,board)

def apagar(pos,board):#apaga uma peca do tabuleiro
    pygame.draw.rect(win, White, (pos[1]*tamqua +5, pos[0]*tamqua+5 , tamqua -5, tamqua-5))
    board[pos[0]][pos[1]] = 0
    pygame.display.update()

def apagar_poss(poss):#apaga o desenho de todos os movimentos posiveis de uma jogador
    for pos in poss:
        pygame.draw.rect(win, White, (pos[1]*tamqua +5, pos[0]*tamqua+5 , tamqua -5, tamqua-5))

def adja(valor1,jog,board):#transforma tanto na matriz como no tabuleiro as pecas de um jogador adversario na do outro jogador que estajam adjacentes
    adja=[]
    if jog ==1:
        for l in range(li):
            for c in range(co):
                if board[l][c] ==2 and (dist(valor1,[l,c]) <2):
                    adja.append([l,c])
    else:
        for l in range(li):
            for c in range(co):
                if board[l][c] ==1 and (dist(valor1,[l,c])<2):
                    adja.append([l,c])
    for pos in adja:
        draw_piece(pos[1],pos[0],tamqua,jog)
        board[pos[0]][pos[1]] = jog

def adjabot(valor1,jog,board):#transforma na matriz as pecas de um jogador adversario na do outro jogador que estajam adjacentes
    adja=[]
    if jog ==1:
        for l in range(li):
            for c in range(co):
                if board[l][c] ==2 and (dist(valor1,[l,c]) <2):
                    adja.append([l,c])

    else:
        for l in range(li):
            for c in range(co):
                if board[l][c] ==1 and (dist(valor1,[l,c])<2):
                    adja.append([l,c])
    for pos in adja:
        board[pos[0]][pos[1]] = jog

def numeropecas(board):#faz uma lista com o numero de espacos livres e de pecas que cada jogador tem
    npecas =[0,0,0]
    for l in range(li):
            for c in range(co):
                if board[l][c] == 0:
                    npecas[0] += 1
                elif board[l][c] == 1:
                    npecas[1] += 1
                elif board[l][c] == 2:
                    npecas[2] += 1
    return npecas

def outroJog(jog):#troca a vez do jogador
    if jog==1:
        return 2
    else:
        return 1

def naotemjogadas(jog,board):#ve se um jogador ainda tem jogadas
    for l in range(li):
        for c in range(co):
            if board[l][c]== jog and possimoves(c,l,board):
                return False
    return True          

def telafinal(jog):#desenha a tela final
    jogt = str(jog)
    win.fill(White)
    myfont = pygame.font.SysFont('Italic',90)
    if jog == -1:
        textsurface = myfont.render( "empate", True,Blue)
    else:textsurface = myfont.render('O jogador ' + jogt + " venceu", True, Blue)
    tex = textsurface.get_rect(center=(WIDTH/2,HEIGHT/2))
    win.blit(textsurface,tex)    
    pygame.display.update()

def vencedor(jog,board):#ve se ha algum vencedor
    npecas =numeropecas(board)
    if npecas[0] == 0:
        if npecas[1] == npecas[2]:
            return -1
        elif npecas[1] < npecas[2]:
            return 2
        else: return 1
    elif npecas[1] == 0:
        return 2
    elif npecas[2] == 0:
        return 1
    elif naotemjogadas(jog,board):
        if npecas[jog] < npecas[outroJog(jog)] + npecas[0]:
            return outroJog(jog)
        else: return jog
    return 0
    
def tom(jog,board):#indica todos os movimentos posiveis de um jogador
    tom=[]
    mjf=[]
    pecas = todapecas(jog,board)
    for ini in pecas:
        poss = possimoves(ini[1],ini[0],board)
        for fin in poss:
            if dist(ini,fin)==1:
                if fin in mjf:
                    pass
                else:
                    mjf.append(fin)
                    tom.append([ini,fin])
            else:
                tom.append([ini,fin])
    return tom

def avaliar(joga,board):#diz a diferencia de numero de pecas entre dois jogadores
    npeca = numeropecas(board)
    return npeca[joga]-npeca[outroJog(joga)]

def minimax(depth,alpha,beta,maxplay,joga,compu,tabuleiro):#algaritomo por qual o computador executa o seu movimento
    if depth ==0 or vencedor(compu,tabuleiro)!=0:
        if vencedor(compu,tabuleiro)!=0:
            if vencedor(compu,tabuleiro)==compu:
                return [1,1,1000]
            elif vencedor(compu,tabuleiro)== outroJog(compu):
                return [1,1,-1000]
            else:return [1,1,500]
        return [1,1,avaliar(compu,tabuleiro)]
    if  maxplay:
        best= [-1,-1,-1000000]
    else:
        best = [-1,-1,1000000]
    t = tom(joga,tabuleiro)
    for i in t:
        notabu =deepcopy(tabuleiro)
        movebot(i[0],i[1],joga,notabu)
        if maxplay:
            score = minimax(depth-1,alpha,beta, False,outroJog(joga),compu,notabu)
            if score[2] >best[2]:
                best = i[0],i[1],score[2]
            alpha = max(alpha,best[2])
            if alpha >= beta:
                break
        else:
            score = minimax(depth-1,alpha,beta, True,outroJog(joga),compu,notabu)
            if score[2] < best[2]:
                best = i[0],i[1],score[2]
            beta = min(beta,best[2])
            if alpha >= beta:
                break
    return best

def bot(depth,joga,tabuleiro):#a jogada do computador
    alpha = -math.inf
    beta  =  math.inf
    comp=joga
    jogada = minimax(depth,alpha,beta,True,joga,comp,tabuleiro)
    #time.sleep(0.5)
    move(jogada[0],jogada[1],joga,tabuleiro)
    
def coord(click):#converte as coordenadas posicionais em coordenadas logicas
    posx = click.pos[0]
    posy = click.pos[1]
    col = int(math.floor(posx/tamqua))
    lin = int(math.floor(posy/tamqua))
    return(col,lin)

class Button:#cria um botao
    def __init__(self, width, height,x,y, color, hover_color, text, text_size, text_color):
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.color = color
        self.hover_color = hover_color
        self.text = text
        self.text_size = text_size
                #o texto que vai aparecer no botao
        self.font = pygame.font.SysFont(None, text_size)
        self.screen_text = self.font.render(text, True, text_color)
        self.text_rect = self.screen_text.get_rect()
        self.text_rect.center = (x+self.width/2, y+self.height/2)
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        win.blit(self.screen_text, self.text_rect)
        #inidica a posicao do rato
        mouse = pygame.mouse.get_pos()
        if self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y:
            pygame.draw.rect(win, self.hover_color, (self.x, self.y, self.width, self.height))
            win.blit(self.screen_text, self.text_rect)
    def action(self,funcao,modo,difi):
        mouse = pygame.mouse.get_pos()
        if self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y:
            pygame.draw.rect(win, self.hover_color, (self.x, self.y, self.width, self.height))
            win.blit(self.screen_text, self.text_rect)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if difi == None:
                        funcao()
                    else:
                        funcao(modo,difi)

class Jogador:#define a jogada de um jogador
    def __init__(self,jog):
        self.jog = jog
    def jogada(self,event,board):
         if event.type == pygame.MOUSEBUTTONDOWN:
            col,lin=coord(event)
            if tuapeca(col,lin,self.jog,board):
                global poss
                poss = possimoves(col,lin,board)
                draw_posi(poss)
                global colf,linf
                colf,linf=col,lin
                apagar_poss(poss)
                return False
            if [lin,col] in poss:
                move((linf,colf),(lin,col),self.jog,board)
                poss=[]
                return True

def quit():#sair do menu inicial
    global menuInicial
    menuInicial = False

def jogo(modo,difi):#modo de jogo PvsP e PvsC
    NQ,board = escolhertabu(NB)
    draw_board(NQ,WIDTH/NQ,board,0)
    atax= True
    jog=1
    while atax:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                atax = False
            if modo ==1:
                jogador = Jogador(jog)
                if jogador.jogada(event,board):
                    jog = outroJog(jog)
                if vencedor(jog,board) != 0:
                    telafinal(vencedor(jog,board))
                    jog=0         
            elif modo ==2:
                if event.type == click:
                    if jog == 1:
                        jogador = Jogador(jog)
                        if jogador.jogada(event,board):
                            jog = outroJog(jog)
                        if vencedor(jog,board) != 0:
                            telafinal(vencedor(jog,board))
                            jog=0         
                if jog ==2:
                    bot(difi,jog,board)
                    jog = outroJog(jog)
                if vencedor(jog,board) != 0:
                    telafinal(vencedor(jog,board))

    pygame.display.update()

def jogo2():#modo de jogo CvsC
    NQ,board = escolhertabu(NB)
    draw_board(NQ,WIDTH/NQ,board,0)
    atax= True
    jog=1
    while atax:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
               atax = False
        if jog ==1:
            bot(2,jog,board)
            jog = outroJog(jog)
            if vencedor(jog,board) != 0:
                telafinal(vencedor(jog,board))
                jog = 0
        elif jog == 2:
            bot(2,jog,board)
            jog = outroJog(jog)
            if vencedor(jog,board) != 0:
                telafinal(vencedor(jog,board))
                jog =0
                     
def menu2():#menu de escolha de dificuldade
    menu2= True
    while menu2:
        win.fill(Gray)
        myfont = pygame.font.SysFont(None,80)
        textsurface = myfont.render('Escolhe a Dificuldade', True, Yellow)
        tex = textsurface.get_rect(center=(WIDTH/2,HEIGHT/8))
        win.blit(textsurface,tex)
        facil= Button(180, 80, WIDTH/2-90, HEIGHT -140*3 ,Gray, Lightgray, 'Fácil', 90,Ciano)
        medio = Button(180, 70, WIDTH/2-90, HEIGHT -140*2,Gray, Lightgray, 'Médio', 90,Ciano)    
        dificil =Button(180, 70, WIDTH/2-90, HEIGHT-140,Gray, Lightgray, 'Difícil', 90,Ciano)
        facil.action(jogo,2,1)
        medio.action(jogo,2,2)
        dificil.action(jogo,2,3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu2 = False
            
        pygame.display.update()

def menu():#menu de escolha de modo de jogo
    menu =  True
    while menu:
        win.fill(Gray)
        myfont = pygame.font.SysFont(None,80)
        textsurface = myfont.render('Escolhe o Modo de Jogo', True, Yellow)
        tex = textsurface.get_rect(center=(WIDTH/2,HEIGHT/8))
        win.blit(textsurface,tex)    
        pvsp= Button(590, 80, WIDTH/2-295, HEIGHT-140*3,Gray, Lightgray, 'Jogador vs Jogador', 90,Ciano)
        pvsc= Button(480, 80, WIDTH/2-295, HEIGHT -140*2 ,Gray, Lightgray, 'Jogador vs Cpu', 90,Ciano)
        cvsc= Button(360, 80, WIDTH/2-180, HEIGHT -140*1 ,Gray, Lightgray, ' Cpu vs Cpu ', 90,Ciano)
        pvsp.action(jogo,1,0)
        pvsc.action(menu2,None,None)
        cvsc.action(jogo2,None,None)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu = False
        pygame.display.update()
    
def escreverinstru(surface,text,pos,font,color):#serve para escrever um texto grande na parte grafica
    words = [word.split(' ') for word in text.splitlines()]  
    space = font.size(' ')[0]  
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, True, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  
                y += word_height
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0] 
        y += word_height  

def menuInstrucoes():#menu das instruÃ§Ãµes
    menuInstrucoes= True
    while menuInstrucoes:
        win.fill(Gray)
        myfont = pygame.font.SysFont(None,80)
        textsurface = myfont.render('Instruções', True, Yellow)
        tex = textsurface.get_rect(center=(WIDTH/2,HEIGHT/8))
        win.blit(textsurface,tex)
        myfont2 = pygame.font.SysFont(None,35)
        text='Cada jogador começa com um certo numero igual de peças, azuis e amarelas,sendo,respectivamente, o primeiro e o segundo jogador. Durante a sua jogada,os jogadores movem uma das suas peças uma ou duas casas em qualquer direção. As distâncias diagonais são equivalentes às distâncias ortogonais, ou seja, é legal mover-se para um quadrado cuja posição relativa esteja a dois quadrados de distância na vertical e na horizontal. Se o destino for adjacente ao á peca selecionada, uma nova peça é criada uma peca nesse local. Caso contrário, a peça na origem se move para o destino. Após o movimento, todas as peças do jogador adversário adjacentes ao local jogado são convertidas para a cor do jogador que jogou. Os jogadores são obrigados a mover uma peça, a menos que nao haja movimentos possiveis, caso em que eles devem passar.O jogo termina quando todos os quadrados forem preenchidos ou um dos jogadores não tiver mais peças. O jogador com mais peças vence. Um empate pode ocorrer se no final do jogo,ambos os jogadores tiverem o mesmo numero de peças.'
        escreverinstru(win,text,(15,HEIGHT/8*2),myfont2,Ciano)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuInstrucoes = False
        pygame.display.update()    

def escolhertabu(NQ):#menu de escolha de tabuleiro
    esco = True
    d = 1
    while esco:
        for event in pygame.event.get():
            NQ,board = createboard(d)
            draw_board(NQ,(WIDTH)/NQ,board,1)
            if event.type == pygame.QUIT:
                esco = False
            elif event.type == click:
                global co,li
                co,li = NQ,NQ
                global tamqua
                tamqua = WIDTH/NQ
                esco = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    try:
                        d = d+1
                        createboard(d)
                    except:
                        d = d-1       
                if event.key == pygame.K_LEFT:
                    d = d-1
                    if d ==0:
                        d =1
    return NQ,board   

click=pygame.MOUSEBUTTONDOWN#reconhece o click do botao
NB,Board =createboard(1)
li,co=NB,NB
tamqua= WIDTH/co
pygame.display.update()
pygame.display.set_caption('Attax')
pygame.init()
menuInicial =  True
while menuInicial:#cria o menu inicial
    win.fill(Gray)
    myfont = pygame.font.SysFont(None,200)
    textsurface = myfont.render('ATTAX', True, Yellow)
    tex = textsurface.get_rect(center=(WIDTH/2,HEIGHT/5))
    win.blit(textsurface,tex)    
    jogar= Button(590, 80, WIDTH/2-295, HEIGHT-140*3,Gray, Lightgray, 'Jogar', 90,Ciano)
    instrucoes= Button(560, 80, WIDTH/2-295, HEIGHT -140*2 ,Gray, Lightgray, 'Instruções', 90,Ciano)
    sair= Button(530, 80, WIDTH/2-265, HEIGHT -140*1 ,Gray, Lightgray, 'Sair', 90,Ciano)
    jogar.action(menu,None,None)
    sair.action(quit,None,None)
    instrucoes.action(menuInstrucoes,None,None)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menuInicial = False
    pygame.display.update()
