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
mixer.music.load('/Users/guyingjie/Documents/albert_python_projects/Apocalypse/background.wav')
mixer.music.play(-1)
# set player size
left = 0
top = 10
length = 20
width = 20
rock_width_: int = width 
rock_length_: int = length 
diamond_width_ = width/2
diamond_length_= length/2
rock_moving_step: int = 10
human_moving_step: int = 10
update_frames_per_second_: int = 10
rock_moving_counter_: int = 0

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

# initialize rock
# list of rocks
rock_location_ = []

# store score
score_ = 0
# store the previous score that we have generated a rock. Without it, multiple rock_creator(True) will be called and multiple new rocks are created.
prev_score_ = 0
bullet_score_ = 0
live_score_ = 1
power_up_score_ = 0
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


def hit_rock(human_left, human_top):
    for each_rock in rock_location_:
        rock_left = each_rock[0]
        rock_top = each_rock[1]
        rock_right = rock_left + each_rock[2]
        rock_bottom = rock_top + each_rock[3]
        human_right = human_left + width
        human_bottom = human_top + length
        for corner_x, corner_y in [(human_left, human_top), (human_right, human_top), (human_left, human_bottom), (human_right,human_bottom)]:
            if (corner_x >= rock_left and corner_x < rock_right) and (
                    corner_y >= rock_top and corner_y < rock_bottom):
                return True
    return False


def hit_rock_by_rock(left, top, rock_location):
    for each_rock in rock_location:
        rock_left = each_rock[0]
        rock_top = each_rock[1]
        rock_right = rock_left + each_rock[2]
        rock_bottom = rock_top + each_rock[3]
        if (left >= rock_left and left <= rock_right) and (top >= rock_top and top <= rock_bottom):
            print("Hit rock by rock. Relocating")
            return True
    return False

def hit_human_by_rock(rock_left, rock_top):
    if left + 2*width >= rock_left and left - width < (rock_left + rock_width_) and top + 2*width >= rock_top and top - width < (
    rock_top + rock_length_):
        print("Hit human by rock. Relocating")
        return True
    return False

def draw_updated_rocks(rock_moving_counter, update_frames_per_second):
    for i in range(len(rock_location_)):
        rock_location = rock_location_[i]
        rockx = rock_location[0]
        rocky = rock_location[1]
        if rock_moving_counter % update_frames_per_second == 0:
            if rockx > left:
                rockx -= rock_moving_step
            if rockx < left:
                rockx += rock_moving_step
            if rocky > top:
                rocky -= rock_moving_step
            if rocky < top:
                rocky += rock_moving_step
            while hit_rock_by_rock(rockx, rocky, rock_location_[:i] if i >=1 else []):
                # shift the rock randomly
                rockx += (round(random.randrange(-rock_width_, rock_width_)) / 10.0) * 10.0
                rocky += (round(random.randrange(-rock_length_, rock_length_)) / 10.0) * 10.0

            rock_location_[i][0]=rockx
            rock_location_[i][1]=rocky
        pygame.draw.rect(canvas, green, [rockx, rocky, rock_width_, rock_length_])

def generate_rock():
    while (True):
        rockx = round(random.randrange(0, (screen_width - rock_width_ - 1)) / 10.0) * 10.0
        rocky = round(random.randrange(0, (screen_width - rock_length_ - 1)) / 10.0) * 10.0
        if not hit_rock_by_rock(rockx, rocky, rock_location_) and not hit_human_by_rock(rockx, rocky):
            break
    rock_location_.append([rockx, rocky, rock_width_, rock_length_])


def rock_creator(create_new, rock_moving_counter, update_frames_per_second):
    # generate rock
    # if rock_location is empty, draw the first rock.
    # every time, redraw the rock in the rock_location.
    # otherwise, wait until reaching score level and draw the next rock and put it in the rock_location.
    if not rock_location_ or create_new:
        generate_rock()
    draw_updated_rocks(rock_moving_counter, update_frames_per_second)


def your_score():
    nowtime = time.time()
    score = int(nowtime - starttime)
    value = score_style.render("Your score: " + str(score) + "    # of Bullets: " + str(bullet_score_) + "  # of lives: " + str(live_score_), True, yellow)
    canvas.blit(value, [0, 0])
    return score


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    canvas.blit(mesg, [200, 500])


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
    # draw current rocks
    rock_moving_counter_ += 1
    rock_creator(False, rock_moving_counter_, update_frames_per_second_)
    # draw diamond
    pygame.draw.rect(canvas, blue, [bulletx, bullety, diamond_width_, diamond_length_])
    pygame.draw.rect(canvas, red, [livex, livey, diamond_width_, diamond_length_])
    pygame.draw.rect(canvas, yellow, [powerx, powery, diamond_width_, diamond_length_ ])
    pygame.draw.rect(canvas, yellow, [left, top, width, length])
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_ = True
        if event.type == pygame.MOUSEMOTION:
            continue
        
        pressed = pygame.key.get_pressed()
        moved = False
        # Hit boundary
        if left > (screen_width - width) or left < 0 or top > (screen_width - width) or top < 0:
            message("You lost. Thanks for playing Apocalypse", (255, 250, 130))
            pygame.display.update()
            Death_sound = mixer.Sound('explosion.wav')
            Death_sound.play()
            left = 2
            top = 2
            score_ = 0
            live_score_ = live_score_-1 if live_score_-1>0 else 0
            bullet_score_ = 0 if live_score_ ==1 else bullet_score_
            starttime = time.time()
            rock_location_ = []
            break
        # check key press
        if pressed[pygame.K_w]:
            top -= human_moving_step
            moved=True
        elif pressed[pygame.K_s]:
            top += human_moving_step
            moved=True
        elif pressed[pygame.K_a]:
            left -= human_moving_step
            moved=True
        elif pressed[pygame.K_d]:
            left += human_moving_step
            moved=True
        if moved:
            # draw current rocks
            rock_creator(False, rock_moving_counter_, update_frames_per_second_)
            # draw diamond
            pygame.draw.rect(canvas, blue, [bulletx, bullety, diamond_width_, diamond_length_])
            pygame.draw.rect(canvas, red, [livex, livey, diamond_width_, diamond_length_])
            pygame.draw.rect(canvas, yellow, [powerx, powery, diamond_width_, diamond_length_])
            pygame.draw.rect(canvas, yellow, [left, top, width, width])
            pygame.display.update()
            # check whether we hit the rock
            if hit_rock(left, top):
                message("aaaahhh", red)
                rock_location_ = []
                left = 2
                top = 2
                score_ = 0
                live_score_ = live_score_-1 if live_score_-1>0 else 0
                bullet_score_ = 0 if live_score_ ==1 else bullet_score_
                starttime = time.time()
                pygame.display.update()
                Death_sound = mixer.Sound('explosion.wav')
                Death_sound.play()
                break

            # check whether we hit bullets or lives
            if (bulletx >= left and bulletx <= (left + width)) and (bullety >= top and bullety <= (top + width)):
                print("Pick bullets(:!!")
                bulletx, bullety = locate_diamond()
                bullet_score_ += 10
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
            if (livex >= left and livex <= (left + width)) and (livey >= top and livey <= (top + width)):
                print("Gain live(:!!")
                livex, livey = locate_diamond()
                live_score_ += 1
                live_sound = mixer.Sound('laser.wav')
                live_sound.play()
            if (powerx >= left and powerx <= (left + width)) and (powery >= top and powery <= (top + width)):
                print("Power up!!")
                powerx, powery = locate_diamond()
                power_up_score_ += 1
                power_sound = mixer.Sound('laser.wav')
                power_sound.play()
    # draw new rock 
    if score_ != 0 and score_ % 15 == 0 and score_ != prev_score_:
        # without comparing prev_score and score_, multiple rock_creator(True) will be called and multiple new rocks are created. because the update_frames_per_second_ = 10, which means we will reach this location 10 times when score_ is multiplier of 20
        prev_score_ = score_
        rock_creator(True, rock_moving_counter_, update_frames_per_second_)
    clock.tick(update_frames_per_second_)

pygame.quit()
quit()
