import pygame
from sys import exit
from random import randint
from pathlib import Path

parent = str(Path(__file__).resolve().parent)

def display_score():
    
    current_time = pygame.time.get_ticks() // 100 - start_time
    range_meter = main_font.render(str(current_time), True, "orange")
    range_meter_rect = range_meter.get_rect(center = (450,50))
    screen.blit(range_meter, range_meter_rect)
    
def obstacle_movement(obstacle_list):

    if obstacle_list:
        for obstacle_rect in obstacle_list:            
            obstacle_rect.x -= 5
            
            if obstacle_rect.bottom == 407:
                screen.blit(obstacle_rock,obstacle_rect)
            else:
                #obstacle_rect.bottom == 408:
                screen.blit(obstacle_cat,obstacle_rect)            
        
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list

    else:
        return []

def collisions (player,obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                collision_effect.play()
                return False
    return True

def vinn_animate():
    global vinn_surface, vinn_index

    vinn_index += 0.3
    if vinn_index >= len(vinn_animation):
        vinn_index = 0
    vinn_surface = vinn_animation[int(vinn_index)]


pygame.init()
pygame.mixer.init()

#### Game Specifics ####
screen = pygame.display.set_mode((900,500))
pygame.display.set_caption("VINNS")
fps = pygame.time.Clock()
game_active = True
vinn_gravity = 0
global_speed = 5
start_time = 0
#### End Of Game Specifics ####

#### Sound ####
jump = pygame.mixer.Sound(parent + "/assets/sounds/jump.wav")
collision_effect = pygame.mixer.Sound(parent + "/assets/sounds/collision.wav")
#### Sound ####

#### Positions ####
vinn_xpos = 75
vinn_ypos = 407
obstacle_rock_xpos = 900
sky_xpos = 0
ground_xpos = 0
#### End Of Positions ####

#### Surfaces & Rectangles ####
## pygame.transform.scale2x()  -  scale 2x module ##
sky = pygame.image.load(parent + "/assets/sky.png").convert()
ground = pygame.image.load(parent + "/assets/ground.png").convert()


vinn_1 = pygame.image.load(parent + "/assets/vinns/dedevinn.png").convert_alpha()
vinn_2 = pygame.image.load(parent + "/assets/vinns/dedevinn_2.png").convert_alpha()
vinn_animation = [vinn_1,vinn_2]
vinn_index = 0
vinn_surface = vinn_animation[vinn_index]
vinn_rect = vinn_surface.get_rect(bottomleft = (vinn_xpos, vinn_ypos))


obstacle_rock = pygame.image.load(parent + "/assets/obstacles/rock_obstacle.png").convert_alpha()
#obstacle_rock_rect = obstacle_rock.get_rect(bottomleft = (800, 407))
obstacle_cat = pygame.image.load(parent + "/assets/obstacles/cat_obstacle.png").convert_alpha()
#obstacle_cat_rect = obstacle_cat.get_rect(bottomleft = (800,407))
obstacle_rect_list = []
main_font = pygame.font.Font(parent + "/assets/font/font.ttf", 40)

#### End Of Surfaces & Rectangles ####

#### Timer ####

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,3000)

while True:    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if  event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and vinn_rect.bottom >= 407:
                    jump.play()
                    vinn_gravity = -25

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                
                game_active = True
                start_time = pygame.time.get_ticks() // 100
        if event.type == obstacle_timer and game_active:
            if randint(0,1):
                obstacle_rect_list.append(obstacle_rock.get_rect(bottomleft = (900, 407)))
            else:
                obstacle_rect_list.append(obstacle_cat.get_rect(bottomleft = (900, 408)))
            
                

    if game_active:
        
        
        #### Sky ####
        screen.blit(sky , (sky_xpos,0))
        screen.blit(sky , (sky_xpos + 1330,0))
        sky_xpos -= 2
        if sky_xpos <= -1330:
            sky_xpos = 0
        #### Sky ####

        #### Ground ####
        screen.blit(ground, (ground_xpos,407))
        screen.blit(ground, (ground_xpos +1330,407))
        ground_xpos -= global_speed
        if ground_xpos <= -1330:
            ground_xpos = 0
        #### Ground ####


        display_score()


        #### Obstacle ####
        # screen.blit(obstacle_rock, obstacle_rock_rect)
        # if  obstacle_rock_rect.right <= 0:
        #     obstacle_rock_rect.left = 900
        # obstacle_rock_rect.centerx -= global_speed
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)
        #### Obstacle ####

        #### Vinn ####
        
        if vinn_gravity <= 50:
            vinn_gravity += 1
        vinn_rect.y += vinn_gravity
        if vinn_rect.bottom >= 407:
            vinn_rect.bottom = 407
        vinn_animate()
        screen.blit(vinn_surface, vinn_rect)
        
        #### Vinn ####

        #### Collision ####
        game_active = collisions(vinn_rect,obstacle_rect_list)
        #if obstacle_rock_rect.colliderect(vinn_rect):
            #game_active = False
        #### Collision ####
    else:
        vinn_rect.bottomleft = (vinn_xpos,407)
        obstacle_rect_list.clear()
        game_over = main_font.render("Game Over", True, "orange")
        game_over_rect = game_over.get_rect(center = (450,250))
        press_space = main_font.render("Press Space", True, "red")
        press_space_rect = press_space.get_rect( center = (450,300))
        screen.blit(press_space,press_space_rect)
        screen.blit(game_over,game_over_rect) 
        

        
        


    pygame.display.update()
    fps.tick(60)


    