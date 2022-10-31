from operator import contains
import re
from tarfile import REGULAR_TYPES
import pygame
import random
from os import path
import math
import sys
import shelve
import time
from pygame import mixer

pygame.init()
relogio = pygame.time.Clock()

tela = pygame.display.set_mode((800, 600))
pontos_atuais = 0

level1 = pygame.image.load("./images/jesuis.png").convert_alpha()
main_menu = pygame.image.load("./images/07.png").convert_alpha()
fonte = pygame.font.Font('disposabledroid-bb.regular.ttf', 108)
image_sprite = [pygame.image.load("./images/00.png"),
                pygame.image.load("./images/01.png"),
                pygame.image.load("./images/02.png"),
                pygame.image.load("./images/03.png"),
                pygame.image.load("./images/04.png"),
                pygame.image.load("./images/05.png"),
                pygame.image.load("./images/06.png"),
                pygame.image.load("./images/07.png"),
                pygame.image.load("./images/08.png"),
                pygame.image.load("./images/09.png"),
                pygame.image.load("./images/10.png"),
                pygame.image.load("./images/11.png"),
                pygame.image.load("./images/12.png"),
                pygame.image.load("./images/13.png"),
                pygame.image.load("./images/14.png"),
                pygame.image.load("./images/15.png"),
                pygame.image.load("./images/16.png"),
                pygame.image.load("./images/17.png"),
                pygame.image.load("./images/18.png"),
                pygame.image.load("./images/19.png"),
                pygame.image.load("./images/20.png")]

start = False
pontuacao = 0
textoX = 10
textoY = 10
recorde = 15
recordeX = 10
recordeY = 100
vacilos = 0 
vacilosX = 10
vacilosY = 55
intervaloA = 2.8
intervaloB = 3.8
frame_atual = 0
reagulador_de_fps = 0

class Bloco:
    def __init__(self, Img, ImgX, ImgY):
        self.Img = Img
        self.ImgX = ImgX
        self.ImgY = ImgY

    def Insert(self, Img, ImgX, ImgY): # Função add Bloco
        tela.blit(Img, (ImgX, ImgY))

def Pressione_Start():
    Enter_Start = fonte.render("Pressione ENTER P/ Iniciar")  # Mensagem
    tela.blit(Enter_Start, (130, 280))  # Localização da Mensagem

def Mostrar_Pontos(x, y):
    Ponto = fonte.render("Pontuação: " + str(pontos_atuais), True, (0, 255, 0))
    tela.blit(Ponto, (x, y))

def Recorde_Pessoal(x, y, level):
    AltoS = fonte.render("Recorde: " + str(recorde)[level], True, (255, 255, 0))
    tela.blit(AltoS, (x, y))

def Mostrar_Vacilos(x, y, num):
    Vacilo = fonte.render("Vacilos: " + str(vacilos) + "/" + str(num), True, (255, 0, 0))
    tela.blit(Vacilo, (x, y))

def Game_Over():
    Game_Over_Texto = fonte.render("Perdeu Playboy", True, (255, 0, 0))
    tela.blit(Game_Over_Texto, (160, 250))
    Reset_Text = fonte.render("Pressione 'R' P/ REINICIAR", True, (255, 255, 255))
    tela.blit(Reset_Text, (200, 350))
    Retorno_Texto = fonte.render("Pressione 'F' P/ SAIR")
    tela.blit(Retorno_Texto, (205, 400))

# Blocos Vermelhos
RedImg = pygame.image.load(path.join("images", "bloco_vermelho.png")).convert()
RedX = 274
RedY = 274
RedY = random.randint(-1472, -128)
Red_Movimento = random.uniform(intervaloA, intervaloB)
Bloco_Red = Bloco(RedImg, RedX, RedY)

# Blocos Azul
AzulImg = pygame.image.load(path.join("images", "bloco_azul.png")).convert()
AzulX = 462
AzulY = random.randint(-1472, -128)
Azul_Movimento = random.uniform(intervaloA, intervaloB)
Bloco_Azul = Bloco(AzulImg, AzulX, AzulY)

# Blocos Roxo
RoxoImg = pygame.image.load(path.join("images", "bloco_roxo.png")).convert()
RoxoX = 402
RoxoY = random.randint(-1472, -128)
Roxo_Movimento = random.uniform(intervaloA, intervaloB)
Bloco_Roxo = Bloco(RoxoImg, RoxoX, RoxoY)

# Botão Esquerdo
EsquerdoImg = pygame.image.load(path.join("images", "botao_esquerdo.png")).convert_alpha()
Esquerdo_Pressionado_Img = pygame.image.load(path.join("images", "botao_esquerdo_pressionado.png"))
EsquerdoB = [EsquerdoImg, Esquerdo_Pressionado_Img]
Esquerdo_Pressionado = False

# Botão Direito
DireitoImg = pygame.image.load(path.join("images", "botao_direito.png")).convert_alpha()
Direito_Pressionado_Img = pygame.image.load(path.join("images", "botao_direito_pressionado.png"))
DireitoB = [DireitoImg, Direito_Pressionado_Img]
Direito_Pressionado = False

# Botão Up
UpImg = pygame.image.load(path.join("images", "botao_cima.png")).convert_alpha()
Up_Pressionado_Img = pygame.image.load(path.join("images", "botao_cima_pressionado.png"))
UpB = [UpImg, Up_Pressionado_Img]
Up_Pressionado = False

# Sistema de Colisão
def Colisao(BlocoX, BlocoY, BotaoX, BotaoY):
    distancia = math.sqrt((math.pow(BlocoX - BotaoX, 2)) + (math.pow(BlocoY - BotaoY, 2)))  # Cálculo de Colisão
    if distancia < 72:
        return True
    else:
        return False

# Mudança de Dificuldade
def Aumentar_Dificuldade():
    global IntervaloA
    global IntervaloB
    if pontos_atuais % 10 == 0:  # A Dificuldade aumenta a cada 10 pontos Conquistados
        IntervaloA += 0.45
        IntervaloB += 0.45

# Reseta Tudo
def Reset():
    global IntervaloA, IntervaloB, RedX,RedY, Red_Movimento, AzulX, Azul_Movimento, RoxoX, Roxo_Movimento
    IntervaloA = 2.8
    IntervaloB = 3.8

    RedY = random.randint(-1472, -128)
    Red_Movimento = random.uniform(IntervaloA, IntervaloB)

    AzulX = random.randint(-1472, -128)
    Azul_Movimento = random.uniform(IntervaloA, IntervaloB)

    RoxoX = random.randint(-1472, -128)
    Roxo_Movimento = random.uniform(IntervaloA, IntervaloB)

# Classe Status do Game
class Status_Game:
    def __init__(self):
        self.done = False
        self.next = None
        self.quit = False
        self.previous = None

class Menu(Status_Game):
    def __init__(self):
        Status_Game.__init__(self)
        self.next = "main_menu"
        mixer.music.load(path.join("sounds","favela_bc.mp3"))
        mixer.music.play(1,0.0)

        
    def Pygame_Evento(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            position = pygame.mouse.get_pos() 

            # Se o mouse clicar e estiver na área do start, tocar efeito sonoto e desativa menu
            if ((position[0] > 25 and position[0] < 220) and (position[1] > 373 and position[1] < 449)):
                mixer.music.load(path.join("sounds","entrada_leaderboard.wav"))
                mixer.music.play(1,0.0)
                self.next = "leaderBoard"
                self.done = True
            
            # se o mouse clicar e estivar no quit, tocar efeito sonoro e sair
            elif ((position[0] > 25 and position[0] < 220) and (position[1] > 510 and position[1] < 585)):
                mixer.music.load(path.join("sounds","entrada_leaderboard.wav"))
                mixer.music.play(1,0.0)
                pygame.quit()
                exit()


    def update(self, screen, dt):
        global frame_atual
        global reagulador_de_fps

        Game.clock.tick(13)
        # Volta para primeira imagem, gerando o loop
        if frame_atual >= len(image_sprite):
            frame_atual = 0

        # Seta a imagem atual
        image = image_sprite[frame_atual]
        frame_atual += 1
    
        # Da o update na tela
        screen.blit(image, (0, 0))

    def draw(self, screen):
        screen.fill((0,0,0))
        screen.blit(main_menu, (0, 0))

class leaderBoard(Status_Game):
    def __init__(self):
        Status_Game.__init__(self)
        self.next = "leaderBoard"
    def Pygame_Evento(self, event):

        level_1 = pygame.Rect(50, 290, 190, 200)

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if level_1.collidepoint(pos):
                select = mixer.Sound(path.join("sounds","entrada_leaderboard.wav"))
                select.play()
                time.sleep(.25)
                self.next = "leaderBoard"
                self.done = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                select = mixer.Sound(path.join("sounds","entrada_leaderboard.wav"))
                select.play()
                time.sleep(.25)
                self.next = "main_menu"
                self.done = True

    def update(self, screen, dt):
        self.draw(screen)
    def draw(self, screen):
        screen.fill((0,0,0))
        screen.blit(level1, (0, 0))






# Classe do Nível
# class Level(Status_Game):
#     def __init__(self):
#         Status_Game.__init__(self)
#         self.next = "leaderBoard"

#     def Pygame_Evento(self, event):
#         global Start, RedY, AzulY, RoxoY, Vacilos, Red_Movimento, \
#             Azul_Movimento, Roxo_Movimento, Pontos, Direito_Pressionado, \
#             Esquerdo_Pressionado, Up_Pressionado
#         Colisao_Red = Colisao(RedX, RedY, 306, 532)
#         Colisao_Azul = Colisao(AzulX, AzulY, 434, 532)
#         Colisao_Roxo = Colisao(530, RoxoY, 562, 532)

#         if event.type == pygame.KEYDOWN:

#             # Botão para Iniciar
#             if event.key == pygame.K_SPACE:
#                 Start = True

#             # Botão Esquerdo
#             if event.key == pygame.K_LEFT:
#                 Esquerdo_Pressionado = True
#                 if Colisao_Red:
#                     # SOM sound = mixer.Sound(path.join("Game Assets", "collison.wav"))
#                     # sound.play()
#                     Pontos += 1
#                     RedY = random.randint(-1472, -128)
#                     Aumentar_Dificuldade()
#                     Red_Movimento = random.uniform(IntervaloA, IntervaloB)

#             # Botão Direiro
#             if event.key == pygame.K_RIGHT:
#                 Direito_Pressionado = True
#                 if Colisao_Azul:
#                     # SOM sound = mixer.Sound(path.join("Game Assets", "collison.wav"))
#                     # sound.play()
#                     Pontos += 1
#                     AzulY = random.randint(-1472, -128)
#                     Aumentar_Dificuldade()
#                     Azul_Movimento = random.uniform(IntervaloA, IntervaloB)

#             # Botão UP
#             if event.key == pygame.K_UP:
#                 Up_Pressionado = True
#                 if Colisao_Roxo:
#                     # SOM sound = mixer.Sound(path.join("Game Assets", "collison.wav"))
#                     # sound.play()
#                     Pontos += 1
#                     RoxoY = random.randint(1472, -128)
#                     Aumentar_Dificuldade()
#                     Roxo_Movimento = random.uniform(IntervaloA, IntervaloB)

#             # Botão de Reset
#             if event.key == pygame.K_r:
#                 Pontos = 0
#                 Vacilos = 0
#                 Reset()

            # Adiciocar opção de voltar a tela anterior com botão
            # if event.key == pygame.K_q:
            #     Vacilos = 0
            #     Pontos = 0
            #     Reset()
            #     # select = mixer.Sound(path.join("Game Assets","select.wav"))
            #     # select.play()
            #     time.sleep(.25)
            #     Start = False
            #     self.done = True
            #     self.next = "Ver o q é"

            # Setando Teclas False como default
    #         if event.type == pygame.KEYUP:
    #             if event.key == pygame.K_LEFT:
    #                 Esquerdo_Pressionado = False

    #             if event.key == pygame.K_RIGHT:
    #                 Direito_Pressionado = False

    #             if event.key == pygame.K_UP:
    #                 Up_Pressionado = False

    # def Update(self, Tela):
    #     self.draw(Tela)
    #     global RedY, AzulY, RoxoY, Vacilos, Red_Movimento, Roxo_Movimento, Azul_Movimento, Recorde

    #     if Start == False:
    #         Pressione_Start()

    #     if RedY >= 574:
    #         # Percas = mixer.Sound(path.join("Game Assets","missed.wav"))
    #         # Percas.play()
    #         Vacilos += 1
    #         RedY = random.randint(-1472, -128)

    #     if AzulY >= 574:
    #         # Percas = mixer.Sound(path.join("Game Assets","missed.wav"))
    #         # Percas.play()
    #         Vacilos += 1
    #         AzulY = random.randint(-1472, -128)

    #     if RoxoY >= 574:
    #         # Percas = mixer.Sound(path.join("Game Assets","missed.wav"))
    #         # Percas.play()
    #         Vacilos += 1
    #         RoxoY = random.randint(-1472, -128)

    #     if Vacilos == 7:  # Número de Vidas
    #         Game_Over()

    #         RedY = -64
    #         Red_Movimento = 0

    #         AzulY = -64
    #         Azul_Movimento = 0

    #         RoxoY = -64
    #         Roxo_Movimento = 0

    #         if Pontos > Recorde:
    #             Recorde = Pontos

    #     while Start:
    #         RedY += Red_Movimento
    #         RoxoY += Roxo_Movimento
    #         AzulY += Azul_Movimento
    #         break

    # def draw(self, Tela):

    #     Fundo_Fase = pygame.image.load(path.join("images", "jesuis.png"))

    #     global Esquerdo_Pressionado, Direito_Pressionado, Up_Pressionado
    #     Tela.fill((0, 0, 0))
    #     Tela.blit(Fundo_Fase, (0, 0))  # Imagem de fundo da Fase
    #     Bloco_Red.Insert(RedImg, RedX, RedY), Bloco_Azul.Insert(AzulImg, AzulX, AzulY), Bloco_Roxo.Insert(RoxoImg,RoxoX, RoxoY)

    #     if Esquerdo_Pressionado == True:
    #         Tela.blit(EsquerdoB[1], (274, 532))
    #     elif Esquerdo_Pressionado == False:
    #         Tela.blit(EsquerdoB[0], (274, 532))

    #     elif Direito_Pressionado == True:
    #         Tela.blit(DireitoB[1], (530, 532))
    #     elif Direito_Pressionado == False:
    #         Tela.blit(DireitoB[0], (530, 532))

    #     elif Up_Pressionado == True:
    #         Tela.blit(UpB[1], (530, 532))
    #     elif Up_Pressionado == False:
    #         Tela.blit(UpB[0], (530, 532))

    #     Mostrar_Pontos(TextoX, TextoY), Mostrar_Vacilos(VacilosX, VacilosY, 6), Recorde_Pessoal(AltoX, AltoY, "Level")


class Controle_Jogo:
    def __init__(self):
        self.__dict__.update()
        self.done = False
        self.Tela = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()

    def Setup(self, Levels, Menu_Principal):
        self.Levels = Levels
        self.Levels_Nome = Menu_Principal
        self.state = self.Levels[self.Levels_Nome]

    def Troca(self):
        self.state.done = False
        previous = self.Levels_Nome
        self.Levels_Nome = self.state.next
        self.state = self.Levels[self.Levels_Nome]
        self.state.previous = previous

    def Update(self, df):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.Troca()
        self.state.update(self.Tela, df)

    def Loop_De_Eventos(self):
        for Eventos in pygame.event.get():
            if Eventos.type == pygame.QUIT:
                self.done = True
            self.state.Pygame_Evento(Eventos)

    def Loop_Principal(self):
        while not self.done:
            Tempo = self.clock.tick(120) / 1000.0
            self.Loop_De_Eventos()
            self.Update(Tempo)
            pygame.display.update()

Game = Controle_Jogo()
levels = {
    'main_menu': Menu(),
    'leaderBoard': leaderBoard()
}

Game.Setup(levels, 'main_menu')
Game.Loop_Principal()
pygame.quit()
sys.exit()