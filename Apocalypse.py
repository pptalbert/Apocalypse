import os
import pygame
import random
import time
from pygame import mixer

pygame.init()

# CREATING CANVAS
screen_width = 1000
print("How to play: wasd to move and remember this: Don't touch the border")
canvas = pygame.display.set_mode((screen_width, screen_width))
# TITLE OF CANVAS
pygame.display.set_caption("Apocalypse")

# play background music
cwd=os.getcwd()
mixer.music.load(f'{cwd}/background.wav')
mixer.music.play(-1)

#create the weapon
gun_width=2 
gun_length=1

# set player size
left = 0
top = 0
length = 20
width = 20
human_x_ = width/2
human_y_ = width/2
human_radius_ = width/2

zombie_width_: int = width 
zombie_length_: int = length 
diamond_width_ = width/2
diamond_length_= length/2
zombie_moving_step: int = 10
human_moving_step: int = 10
update_frames_per_second_: int = 10
zombie_moving_counter_: int = 0
# generate a zombie every 15 seconds
zombie_generate_counter_: int = 15
zombie_health_: int = 20

# colorcode
colorR = 255
colorG = 255
colorB = 255
blue = (0, 0, 255)
black = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 255, 102)
red = (255, 0, 0)
green = (0, 255, 0)
grey = (128, 128, 128)

# initialize zombie
# list of zombies with parameters
# [left_top_x, left_top_y, width, length, health]
zombie_location_ = []

# store score
score_ = 0
# store the previous score that we have generated a zombie. Without it, multiple zombie_creator(True) will be called and multiple new zombies are created.
prev_score_ = 0
bullet_score_ = 0
live_score_ = 1
# power up the weapon. power up block is generated every 5 seconds.
# pick one power_up block, power_up_score_ added by 1. 
# when power_up_score_ reach multiplier of 5, weapon_power_up_level_ increased by 1
# weapon_power_up_level_: 1 means normal, 2 means double bullet, 3 means triple bullet
power_up_block_generate_counter_ = 5
power_up_score_ = 1
power_up_multiplier_ = 5
weapon_power_up_level_ = 1

# exit status
exit_ = False

clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 50)
score_style = pygame.font.SysFont("comicsansms", 35)

# find right diamond position
def locate_diamond():
    diamond_found = True
    while (True):
        diamond_found = True
        diamondx = max(round(random.randrange(0, (screen_width - width - 1)) / 10.0) * 10.0, width)
        diamondy = max(round(random.randrange(0, (screen_width - width - 1)) / 10.0) * 10.0, length)
        diamondx = min(diamondx, screen_width - width)
        diamondy = min(diamondy, screen_width - length)
        print(f"diamond location {diamondx}, {diamondy}")   
        return (diamondx, diamondy)


def hit_zombie(human_left, human_top):
    for each_zombie in zombie_location_:
        zombie_left = each_zombie[0]
        zombie_top = each_zombie[1]
        zombie_right = zombie_left + each_zombie[2]
        zombie_bottom = zombie_top + each_zombie[3]
        human_right = human_left + width
        human_bottom = human_top + length
        for corner_x, corner_y in [(human_left, human_top), (human_right, human_top), (human_left, human_bottom), (human_right,human_bottom)]:
            if (corner_x >= zombie_left and corner_x < zombie_right) and (
                    corner_y >= zombie_top and corner_y < zombie_bottom):
                return True
    return False


def circle_hit_zombie(radius_x, radius_y):
    for each_zombie in zombie_location_:
        zombie_left = each_zombie[0]
        zombie_top = each_zombie[1]
        zombie_right = zombie_left + each_zombie[2]
        zombie_bottom = zombie_top + each_zombie[3]
        if (radius_x >= zombie_left and radius_x <= zombie_right) and (
            radius_y >= zombie_top and radius_y <= zombie_bottom):
            return True
    return False


def hit_zombie_by_zombie(left, top, zombie_location):
    for each_zombie in zombie_location:
        zombie_left = each_zombie[0]
        zombie_top = each_zombie[1]
        zombie_right = zombie_left + each_zombie[2]
        zombie_bottom = zombie_top + each_zombie[3]
        if (left >= zombie_left and left <= zombie_right) and (top >= zombie_top and top <= zombie_bottom):
            return True
    return False

def hit_human_by_zombie(zombie_left, zombie_top):
    circle_external_square_left = human_x_ - width/2
    circle_external_square_top = human_y_ - width/2
    if circle_external_square_left + 2*width >= zombie_left and circle_external_square_left - width < (zombie_left + zombie_width_) and circle_external_square_top + 2*width >= zombie_top and circle_external_square_top - width < (
    zombie_top + zombie_length_):
        print("Hit human by zombie. Relocating")
        return True
    return False

def draw_updated_zombies(zombie_moving_counter, update_frames_per_second):
    for i in range(len(zombie_location_)):
        zombie_location = zombie_location_[i]
        zombiex = zombie_location[0]
        zombiey = zombie_location[1]
        zombie_health = zombie_location[4]
        if zombie_moving_counter % update_frames_per_second == 0:
            if zombiex >= human_x_:
                zombiex -= zombie_moving_step
            if zombiex <= human_x_:
                zombiex += zombie_moving_step
            if zombiey >= human_y_:
                zombiey -= zombie_moving_step
            if zombiey <= human_y_:
                zombiey += zombie_moving_step
            while hit_zombie_by_zombie(zombiex, zombiey, zombie_location_[:i] if i >=1 else []):
                # shift the zombie randomly
                zombiex += (round(random.randrange(-zombie_width_, zombie_width_)) / 10.0) * 10.0
                zombiey += (round(random.randrange(-zombie_length_, zombie_length_)) / 10.0) * 10.0

            zombie_location_[i][0]=zombiex
            zombie_location_[i][1]=zombiey
        pygame.draw.rect(canvas, green if zombie_health>zombie_health_/2 else grey, [zombiex, zombiey, zombie_width_, zombie_length_])

def generate_zombie():
    while (True):
        zombiex = round(random.randrange(0, (screen_width - zombie_width_ - 1)) / 10.0) * 10.0
        zombiey = round(random.randrange(0, (screen_width - zombie_length_ - 1)) / 10.0) * 10.0
        if not hit_zombie_by_zombie(zombiex, zombiey, zombie_location_) and not hit_human_by_zombie(zombiex, zombiey):
            break
    random_zombie_health = round(random.randrange(1, zombie_health_))
    zombie_location_.append([zombiex, zombiey, zombie_width_, zombie_length_, random_zombie_health])


def zombie_creator(create_new, zombie_moving_counter, update_frames_per_second):
    # generate zombie
    # if zombie_location is empty, draw the first zombie.
    # every time, redraw the zombie in the zombie_location.
    # otherwise, wait until reaching score level and draw the next zombie and put it in the zombie_location.
    if not zombie_location_ or create_new:
        generate_zombie()
    draw_updated_zombies(zombie_moving_counter, update_frames_per_second)


def your_score():
    nowtime = time.time()
    score = int(nowtime - starttime)
    value = score_style.render("Your score: " + str(score) + "    #Bullets: " + str(bullet_score_) + "  #lives: " + str(live_score_) + "   #power: " + str(weapon_power_up_level_), True, yellow)
    canvas.blit(value, [0, 0])
    return score


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    canvas.blit(mesg, [200, 500])

def kill_zombie():
    to_be_removed_zombie_index=[]
    print(human_x_, human_y_)
    for i in range(len(zombie_location_)): 
        zombie_left = zombie_location_[i][0]
        zombie_top = zombie_location_[i][1]
        zombie_right = zombie_left + zombie_location_[i][2]
        zombie_bottom = zombie_top + zombie_location_[i][3]
        zombie_health = zombie_location_[i][4]
        print(zombie_left, zombie_right,zombie_top, zombie_bottom, zombie_health)
        if (zombie_left <= human_x_ and zombie_right >= human_x_) or (zombie_top <= human_y_ and zombie_bottom > human_y_):
            zombie_health = zombie_health - zombie_health_/4
            if zombie_health <= 0:
                # health is gone, zombie should be removed
                print(i)
                to_be_removed_zombie_index.append(i)
            zombie_location_[i][4] = zombie_health
    # remove zombie from the zombie_location_, from tail to head
    print(to_be_removed_zombie_index)
    to_be_removed_zombie_index.reverse()
    for idx in to_be_removed_zombie_index:
        zombie_location_.pop(idx)




# initialize diamonds
bulletx, bullety = locate_diamond()
livex, livey = locate_diamond()
powerx, powery = locate_diamond()

# record start time
starttime = time.time()
# entrance
while not exit_:
    # refresh the canvas
    canvas.fill((0, 0, 0))
    score_ = your_score()        
    # draw current zombies
    zombie_moving_counter_ += 1
    zombie_creator(False, zombie_moving_counter_, update_frames_per_second_)
    # draw diamond
    pygame.draw.rect(canvas, blue, [bulletx, bullety, diamond_width_, diamond_length_])
    pygame.draw.rect(canvas, red, [livex, livey, diamond_width_, diamond_length_])
    if powerx != 0 and powery != 0:
        pygame.draw.rect(canvas, yellow, [powerx, powery, diamond_width_, diamond_length_ ])
    pygame.draw.circle(canvas, yellow, (human_x_, human_y_), human_radius_)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_ = True
        if event.type == pygame.MOUSEMOTION:
            continue
        
        pressed = pygame.key.get_pressed()
        moved = False
        shoot = False
        # Hit boundary
        if human_x_ > (screen_width - width) or human_x_ < 0 or human_y_ > (screen_width - width) or human_y_ < 0:
            message("You lost. Thanks for playing Apocalypse", (255, 250, 130))
            pygame.display.update()
            Death_sound = mixer.Sound('explosion.wav')
            Death_sound.play()
            human_x_ = 2
            human_y_ = 2
            score_ = 0
            live_score_ = live_score_-1 if live_score_-1>0 else 0
            bullet_score_ = 0 if live_score_ == 0 else bullet_score_
            weapon_power_up_level_ = 1 if live_score_ == 0 else weapon_power_up_level_
            power_up_score_ = 0 if live_score_ == 0 else power_up_score_
            starttime = time.time()
            zombie_location_ = []
            break
        # check key press
        if pressed[pygame.K_w]:
            human_y_ -= human_moving_step
            moved=True
        elif pressed[pygame.K_s]:
            human_y_ += human_moving_step
            moved=True
        elif pressed[pygame.K_a]:
            human_x_ -= human_moving_step
            moved=True
        elif pressed[pygame.K_d]:
            human_x_ += human_moving_step
            moved=True
        elif pressed[pygame.K_SPACE]: 
            shoot = True
        # take actions based on key press
        if moved:
            # draw current zombies
            zombie_creator(False, zombie_moving_counter_, update_frames_per_second_)
            # draw diamond
            pygame.draw.rect(canvas, blue, [bulletx, bullety, diamond_width_, diamond_length_])
            pygame.draw.rect(canvas, red, [livex, livey, diamond_width_, diamond_length_])
            if powerx != 0 and powery != 0:
              pygame.draw.rect(canvas, yellow, [powerx, powery, diamond_width_, diamond_length_])       
            pygame.draw.circle(canvas, yellow, (human_x_, human_y_), human_radius_)
            pygame.display.update()
            # check whether we hit the zombie
            if circle_hit_zombie(human_x_, human_y_):
                message("aaaahhh", red)
                zombie_location_ = []
                human_x_ = 2
                human_y_ = 2
                score_ = 0
                live_score_ = live_score_-1 if live_score_-1>0 else 0
                bullet_score_ = 0 if live_score_ == 0 else bullet_score_
                weapon_power_up_level_ = 1 if live_score_ == 0 else weapon_power_up_level_
                power_up_score_ = 0 if live_score_ == 0 else power_up_score_
                starttime = time.time()
                pygame.display.update()
                Death_sound = mixer.Sound('explosion.wav')
                Death_sound.play()
                break

            # check whether we hit bullets or lives
            circle_external_square_left = human_x_ - width/2
            circle_external_square_top = human_y_ - width/2
            if (bulletx >= circle_external_square_left and bulletx <= (circle_external_square_left + width)) and (bullety >= circle_external_square_top and bullety <= (circle_external_square_top + width)):
                print("Pick bullets(:!!")
                bulletx, bullety = locate_diamond()
                bullet_score_ += 10
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
            if (livex >= circle_external_square_left and livex <= (circle_external_square_left + width)) and (livey >= circle_external_square_top and livey <= (circle_external_square_top + width)):
                print("Gain live(:!!")
                livex, livey = locate_diamond()
                live_score_ += 1
                live_sound = mixer.Sound('laser.wav')
                live_sound.play()
            if (powerx >= circle_external_square_left and powerx <= (circle_external_square_left + width)) and (powery >= circle_external_square_top and powery <= (circle_external_square_top + width)):
                print("accumulating power up")
                powerx, powery = 0, 0
                power_up_score_ += 1
                if power_up_score_ % power_up_multiplier_ == 0:
                    print("Power up!!")
                    weapon_power_up_level_ += 1
                power_sound = mixer.Sound('laser.wav')
                power_sound.play()
        if shoot:
            # draw diamond
            pygame.draw.rect(canvas, blue, [bulletx, bullety, diamond_width_, diamond_length_])
            pygame.draw.rect(canvas, red, [livex, livey, diamond_width_, diamond_length_])
            if powerx != 0 and powery != 0:
                pygame.draw.rect(canvas, yellow, [powerx, powery, diamond_width_, diamond_length_])       
            pygame.draw.circle(canvas, yellow, (human_x_, human_y_), human_radius_)
            # draw shooting lines.
            if bullet_score_ > 0:
                bullet_score_ -= 10
                pygame.draw.line(canvas, red, (human_x_,0), (human_x_, screen_width))
                pygame.draw.line(canvas, red, (0, human_y_), (screen_width, human_y_))
                # check whether we hit a zombie!
                kill_zombie()
            # draw current zombies
            zombie_creator(False, zombie_moving_counter_, update_frames_per_second_)
            pygame.display.update()
            
    # draw new zombie 
    if score_ != 0 and (score_ % zombie_generate_counter_ == 0 or score_ % power_up_block_generate_counter_ == 0) and score_ != prev_score_:
        # without comparing prev_score and score_, multiple zombie_creator(True) will be called and multiple new zombies are created. because the update_frames_per_second_ = 10, which means we will reach this location 10 times when score_ is multiplier of 20
        prev_score_ = score_
        if score_ % zombie_generate_counter_ == 0:
            # generate a new zombie
            zombie_creator(True, zombie_moving_counter_, update_frames_per_second_)
        elif score_ % power_up_block_generate_counter_ == 0:
            # generate a new power up block
            if powerx == 0 and powery == 0:
                powerx, powery = locate_diamond()
    clock.tick(update_frames_per_second_)

pygame.quit()
quit()