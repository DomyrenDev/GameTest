import pygame
import random
pygame.init()

background = pygame.image.load('assets/bg/bg.png')
redbird = pygame.image.load('assets/bg/redbird.png')
base = pygame.image.load('assets/bg/base.png')
go = pygame.image.load('assets/bg/gameover.png')
pipe = pygame.image.load('assets/bg/pipe-green.png')
pipeup = pygame.transform.flip(pipe, False, True) 

display = pygame.display.set_mode((288, 512))
FPS = 60
velav = 3
FONT = pygame.font.SysFont('Comic Sans MS', 50, bold = True)

class tubi_casse:
    def __init__(self):
        self.x = 300
        self.y = random.randint(-75,150)
        
    def avanza_e_disegna(self):
        self.x -= velav
        display.blit(pipe, (self.x, self.y + 210))
        display.blit(pipeup, (self.x, self.y - 210))
        
    def collisione(self, redbird, uccellox, uccelloy):
        tolleranza = 5
        uccello_lato_dx = uccellox + redbird.get_width() - tolleranza
        uccello_lato_sx = uccellox + tolleranza
        tubi_lato_dx = self.x + pipe.get_width()
        tubi_lato_sx = self.x
        uccello_lato_su = uccelloy + tolleranza
        uccello_lato_giu = uccelloy + redbird.get_height() - tolleranza
        tubi_lato_su = self.y + 110
        tubi_lato_giu = self.y + 210
        if uccello_lato_dx > tubi_lato_sx and uccello_lato_sx < tubi_lato_dx:
            if uccello_lato_su < tubi_lato_su or uccello_lato_giu > tubi_lato_giu:
                hai_perso()
                
    def fra_i_tubi(self, redbird, uccellox, uccelloy):
        tolleranza = 5
        uccello_lato_dx = uccellox + redbird.get_width() - tolleranza
        uccello_lato_sx = uccellox + tolleranza
        tubi_lato_dx = self.x + pipe.get_width()
        tubi_lato_sx = self.x
        uccello_lato_su = uccelloy + tolleranza
        uccello_lato_giu = uccelloy + redbird.get_height() - tolleranza
        tubi_lato_su = self.y + 110
        tubi_lato_giu = self.y + 210
        if uccello_lato_dx > tubi_lato_sx and uccello_lato_sx < tubi_lato_dx:
            if uccello_lato_su < tubi_lato_su or uccello_lato_giu > tubi_lato_giu:
                return True
        return False

def disegna_oggetti():
    display.blit(background, (0, 0))
    for t in tubi :
        t.avanza_e_disegna()
    display.blit(redbird, (uccellox, uccelloy))
    display.blit(base, (basex, 400))
    punti_render = FONT.render(str(punti), 1, (255, 255, 255))
    display.blit(punti_render, (144, 0))
   

def aggiorna():
    pygame.display.update()
    pygame.time.Clock().tick(FPS)
    
def  inizializza():
    global uccellox, uccelloy, uccello_vely
    global basex
    global tubi
    global punti
    global fra_i_tubi
    uccellox, uccelloy = 60, 150
    uccello_vely = 0
    basex = 0
    punti = 0
    tubi = []
    tubi.append(tubi_casse())
    fra_i_tubi = False

def hai_perso():
    display.blit (go, (50, 180))
    aggiorna()
    ricomicia = False
    while not ricomicia:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                inizializza()
                ricomicia = True
            if event.type == pygame.QUIT:
                pygame.quit()
    
    inizializza()
# Inizializzo Variabili
inizializza()

# Ciclo di gioco
while True:
    # Eventi
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            uccello_vely = -10

    # Gravità
    basex -= velav
    if basex < -45:
        basex = 0
    uccello_vely += 1
    uccelloy += uccello_vely

    # Controllo passaggio tra i tubi
    was_between_pipes = fra_i_tubi
    fra_i_tubi = any(t.fra_i_tubi(redbird, uccellox, uccelloy) for t in tubi)
    if was_between_pipes and not fra_i_tubi:
        punti += 1

    # Controllo collisioni
    for t in tubi:
        t.collisione(redbird, uccellox, uccelloy)
    
    # Gestione tubi
    if len(tubi) > 0 and tubi[-1].x < 150:
        tubi.append(tubi_casse())
    if len(tubi) > 0 and tubi[0].x < -pipe.get_width():
        tubi.pop(0)

    # Collisioni con tubi
    if uccelloy > 380:
        hai_perso ()

    
    disegna_oggetti()
    aggiorna()
            

