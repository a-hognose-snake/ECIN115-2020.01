import pygame,sys,random

# Función que dibuja el piso en la pantalla
def draw_floor():
    screen.blit(floor_surface,(floor_x_pos,450))
    screen.blit(floor_surface,(floor_x_pos + 288,450))

# Función que crea los obstáculos
def create_soap():
    random_soap_pos = random.choice(soap_height)
    bottom_soap = soap_surface.get_rect(midtop = (450,random_soap_pos))
    top_soap = soap_surface.get_rect(midbottom = (450,random_soap_pos-150))
    return bottom_soap,top_soap

# Función que mueve los obstáculos hacia la izquierda
def move_soaps(soaps):
    for soap in soaps:
        soap.centerx -= 5
    return soaps
  
#   Función que dibuja los obstáculos en la pantalla  
def draw_soaps(soaps):
    for soap in soaps:
        screen.blit(soap_surface,soap)
        
# Función que chequea por colisiones 
def check_collision(soaps):
    for soap in soaps:
        if virus_rect.colliderect(soap):
            #print("choque")
            death_sound.play()
            return False 
    if virus_rect.top <= -30 or  virus_rect.bottom >= 450:
        #print("choque")
        # Al retornar falso, se muestra la pantalla de puntajes (“game over”)
        return False
    # Al retornar verdadero, se sigue el juego, ya que no ha chocado con nada
    return True

# Función que dibuja los puntajes en la pantalla   
def score_display(game_state):
    # Pantalla juego 
    if game_state == "main_game":
        score_surface= game_font.render(str(int(score)),True,(0,0,0)) 
        score_rect = score_surface.get_rect(center=(144,50))   
        screen.blit(score_surface,score_rect) 
    # Pantalla game over   
    if game_state == "game_over":
        score_surface= game_font.render((f'Puntaje ({int(score)})'),True,(0,0,0)) 
        score_rect = score_surface.get_rect(center=(144,50))   
        screen.blit(score_surface,score_rect) 
        
        high_score_surface= game_font.render((f'Récord ({int(high_score)})'),True,(0,0,0)) 
        high_score_rect = high_score_surface.get_rect(center=(144,425))   
        screen.blit(high_score_surface,high_score_rect) 

# Función que actualiza el puntaje record 
def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

# Inicia todos los módulos de pygame
pygame.init()
# Tamaño de pantalla: 288x512
screen= pygame.display.set_mode((288,512))
# Define tiempo
clock = pygame.time.Clock()

game_font = pygame.font.Font("joystix monospace.ttf",20)

# Variables
gravity = 0.40
virus_movement = 0 
game_active = True
score = 0
high_score = 0
####################

# Fondo de pantalla 
bg_surface = pygame.image.load("assets/bg_virus.png").convert()
bg_surface = pygame.transform.scale(bg_surface,(294,512))

# Piso
floor_surface = pygame.image.load("assets/base.png").convert()
floor_surface = pygame.transform.scale(floor_surface,(288,200))
floor_x_pos = 0

# Virus
virus_surface = pygame.image.load("assets/coronavirus.png")
virus_surface = pygame.transform.scale(virus_surface,(20,20))
virus_rect = virus_surface.get_rect(center = (100,256))

# Obstáculos 
soap_surface = pygame.image.load("assets/soap.png").convert_alpha()
soap_surface = pygame.transform.scale(soap_surface,(90,90))

# Lista de obstáculos 
soap_list = []

# Evento: Nuevo obstáculo 
SPAWNSOAP = pygame.USEREVENT
# Obstáculo aparece cada 1200 milisegundos 
pygame.time.set_timer(SPAWNSOAP,1200)
# Alturas al que aparecerán los obstaculos 
soap_height = [180,200,300]

# Imagen de game over
game_over_surface = pygame.image.load("assets/message.png").convert_alpha()
game_over_rect = game_over_surface.get_rect(center = (144,256))


#sonido
whoosh_sound = pygame.mixer.Sound("sound/sfx_swooshing.wav")
death_sound = pygame.mixer.Sound("sound/sfx_hit.wav")
score_sound = pygame.mixer.Sound("sound/sfx_point.wav")
score_sound_countdown = 100

while True:
    for event in pygame.event.get():
        # Al cerrar la pantalla 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Al apretar la tecla space
        if event.type == pygame.KEYDOWN:
            # Al apretar tecla space y estar en la pantalla de juego
            if event.key == pygame.K_SPACE and game_active:
                #print("volar")
                virus_movement = 0
                virus_movement -= 5
                whoosh_sound.play()
            # Al apretar tecla space y estar en la pantalla de game over
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                soap_list.clear()
                virus_rect.center = (100,256)
                virus_movement = 0
                score = 0
                
        # Al momento que aparece un nuevo obstáculo   
        if event.type == SPAWNSOAP:
            #print("jabon")
            soap_list.extend(create_soap())
            #print(soap_list)
    # Mostrar fondo en pantalla de juego y game over            
    screen.blit(bg_surface,(0,0)) 
    
    # Al estar en pantalla de juego
    if game_active:
        #virus
        virus_movement += gravity
        virus_rect.centery += virus_movement
        screen.blit(virus_surface,virus_rect)
        game_active = check_collision(soap_list)
        
        #jabon
        soap_list = move_soaps(soap_list)
        draw_soaps(soap_list)
    
        #piso
        floor_x_pos -= 1
        draw_floor()
        if floor_x_pos <= -288:
            floor_x_pos = 0
            
        score += 0.01    
        score_display("main_game")
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 100
    # Al estar en game over       
    else:
        screen.blit(game_over_surface,game_over_rect)
        high_score = update_score(score,high_score)
        score_display("game_over")
    # Actualizar pantalla
    pygame.display.update()
    # El programa nunca va a correr a más de 120 frames por segundo
    clock.tick(100)
pygame.quit()
sys.exit()
    
    