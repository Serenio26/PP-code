import pygame
import random
from button import *
pygame.init()

#set Frame rate
clock = pygame.time.Clock()
fps=60

#game window
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

#to run window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Battle screen')

#define game variables 
current_fighter = 1 
total_fighters = 3 
action_cooldown = 0
action_wait_time = 90
attack = False
postion = False
potion_effect = 10
clicked = False
game_over = 0

#define fonts
font = pygame.font.SysFont('Times New Roman', 26)

#define color
red = (255, 0, 0)
green = (0, 255, 0)

#load image
#backgroud images
background_img = pygame.image.load('img/Background/background.png').convert_alpha()
#panel image
panel_img = pygame.image.load('img/Icons/panel.png').convert_alpha()
#buttom image
potion_img = pygame.image.load('img/Icons/potion.png').convert_alpha()
restart_img = pygame.image.load('img/Icons/restart.png').convert_alpha()
#load victory and defeat image
victory_img = pygame.image.load('img/Icons/victory.png').convert_alpha()
defeat_img = pygame.image.load('img/Icons/defeat.png').convert_alpha()
#sword image
sword_img = pygame.image.load('img/Icons/sword.png').convert_alpha()


#function for drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

#function for drawing background
def draw_bg():
    screen.blit(background_img, (0,0))

#function for panel
def draw_panel():
    #draw panel rectengale
    screen.blit(panel_img, (0,screen_height - bottom_panel))
    #show knight stats
    draw_text(f'{knight.name} HP: {knight.hp}', font, red, 100, screen_height - bottom_panel +10)
    for count, i in enumerate(bandit_list):
        #show name and health
        draw_text(f'{i.name} HP: {i.hp}', font, red, 550, (screen_height - bottom_panel +10) + count *60)


#fighter class
class Fighter():
    def __init__(self,x,y,name, max_hp, strength, potions):
        self.name = name
        self.max_hp=max_hp
        self.hp=max_hp
        self.strength=strength
        self.start_potions = potions
        self.potions=potions
        self.alive= True
        self.animation_list=[]
        self.frame_index = 0
        self.action = 0 #0:idle, 1:attack, 2:hurt, 3:dead
        self.update_time = pygame.time.get_ticks()
        #load idelimages
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/{self.name}/Idle/{i}.png')
            img = pygame.transform.scale(img,(img.get_width()*3,img.get_height()*3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load attack images
        temp_list = []
        for i in range(8):
            img = pygame.image.load(f'img/{self.name}/Attack/{i}.png')
            img = pygame.transform.scale(img,(img.get_width()*3,img.get_height()*3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
         #load hurt images
        temp_list = []
        for i in range(3):
            img = pygame.image.load(f'img/{self.name}/Hurt/{i}.png')
            img = pygame.transform.scale(img,(img.get_width()*3,img.get_height()*3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        #load death images
        temp_list = []
        for i in range(10):
            img = pygame.image.load(f'img/{self.name}/Death/{i}.png')
            img = pygame.transform.scale(img,(img.get_width()*3,img.get_height()*3))
            temp_list.append(img)
        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center=(x,y)


#update image
    def update(self):
        animation_cooldown=100
        #handle information 
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index +=1 
        #if the imformation has run out then back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.idle()


    def idle(self):
        #set variables to idle action
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def attack(self, target):
     # Deal damage to enemy
        rand = random.randint(-5, 5)
        damage = self.strength + rand
        target.hp -= damage
        #run enemy hurt animetion
        target.hurt()
        #check if target died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
            target.death()
        damage_text = DamageText(target.rect.centerx, target.rect.y, str(damage), red)
        damage_text_group.add(damage_text)
        #set variables to attack action
        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def hurt(self):
        #set variables to hurt action
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()


    def death(self):
        #set variables to hurt action
        self.action = 3
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def reset(self):
        self.alive = True 
        self.potions = self.start_potions
        self.hp = self.max_hp
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()


#draw image 
    def draw(self):
        screen.blit(self.image, self.rect)

class HealthBar():
    def __init__ (self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self,hp):
        #update with new health
        self.hp = hp
        #cal health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio , 20))


class DamageText(pygame.sprite.Sprite):
    def __init__(self, x, y, damage, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, colour)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.counter = 0

    def update(self):
        #morve damage text up
        self.rect.y -= 1
        #delete text
        self.counter += 1
        if self.counter > 38:
            self.kill()

damage_text_group = pygame.sprite.Group()


knight=Fighter(200, 260, 'Knight', 50, 10, 3)
bandit1=Fighter(550,260, 'Bandit', 10, 6, 1)
bandit2=Fighter(700,260, 'Bandit', 10, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, bandit2.hp, bandit2.max_hp)

#button class
class Button():
	def __init__(self, surface, x, y, image, size_x, size_y):
		self.image = pygame.transform.scale(image, (size_x, size_y))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False
		self.surface = surface

	def draw(self):
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		self.surface.blit(self.image, (self.rect.x, self.rect.y))

		return action
    
#create button
potion_button = Button(screen, 100, screen_height - bottom_panel + 70, potion_img, 64, 64)
restart_button = Button(screen, 330, 120, restart_img, 120, 30)

#main game runnign system
run = True
while run:
    clock.tick(fps)

    #draw background
    draw_bg()

    #draw panel
    draw_panel()
    knight_health_bar.draw(knight.hp)
    bandit1_health_bar.draw(bandit1.hp)
    bandit2_health_bar.draw(bandit2.hp)

    #draw fighter
    knight.update()
    knight.draw()
    for bandit in bandit_list:
        bandit.update()
        bandit.draw()

    #draw damage text 
    damage_text_group.update()
    damage_text_group.draw(screen)

    #control player action
    #resert action variables 
    attack = False
    potion = False
    target = None 
    #make sure mouse is visible
    pygame.mouse.set_visible(True)
    pos = pygame.mouse.get_pos()
    for count, bandit in enumerate(bandit_list):
        if bandit.rect.collidepoint(pos):
            #hide mouse 
            pygame.mouse.set_visible(False)
            #show sowrd in place of mouse cursor
            screen.blit(sword_img, pos)
            if clicked == True and bandit.alive == True:
                attack = True
                target = bandit_list[count]
    if potion_button.draw():
        potion = True
    #show how many left 
    draw_text(str(knight.potions), font, red, 150, screen_height - bottom_panel + 70)


    if game_over == 0:
        #player action
        if knight.alive == True:
            if current_fighter == 1:
                action_cooldown += 1
                if action_cooldown >= action_wait_time:
                    #look for player action 
                    #attack 
                    if attack == True and target != None:
                        knight.attack(target)
                        current_fighter += 1
                        action_cooldown = 0
                    #potion
                    if potion == True:
                        if knight.potions > 0:
                            #check if potion will heal player beond mx health 
                            if knight.max_hp - knight.hp > potion_effect:
                                heal_amount= potion_effect
                            else:
                                heal_amount = knight.max_hp - knight.hp
                            knight.hp += heal_amount
                            knight.potions -= 1
                            damage_text = DamageText(knight.rect.centerx, knight.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
        else: 
            game_over = -1
        

        #enemy action 
        for count, bandit in enumerate(bandit_list):
            if current_fighter == 2 + count:
                if bandit.alive == True:
                    action_cooldown += 1
                    if action_cooldown >= action_wait_time:
                    #check if bandit need to heal first
                        if(bandit.hp / bandit.max_hp) < 0.5 and bandit.potions > 0:
                            if bandit.max_hp - bandit.hp > potion_effect:
                                heal_amount= potion_effect
                            else:
                                heal_amount = bandit.max_hp - bandit.hp
                            bandit.hp += heal_amount
                            bandit.potions -= 1
                            damage_text = DamageText(bandit.rect.centerx, bandit.rect.y, str(heal_amount), green)
                            damage_text_group.add(damage_text)
                            current_fighter += 1
                            action_cooldown = 0
                        #attack
                        else:
                            bandit.attack(knight)
                            current_fighter +=1
                            action_cooldown = 0
                else:
                    current_fighter +=1


    #if all fighter have turn then reset 
        if current_fighter > total_fighters:
            current_fighter = 1

#check if all bandit are dead
    alive_bandit = 0
    for bandit in bandit_list:
        if bandit.alive == True:
            alive_bandit +=1
    if alive_bandit == 0:
        game_over = 1

#check if game is over 
    if game_over != 0:
        if game_over == 1:
            screen.blit(victory_img, (250, 50))
        if game_over == -1:
            screen.blit(defeat_img, (250, 50))
        if restart_button.draw():
            knight.reset()
            for bandit in bandit_list:
                bandit.reset()
            current_fighter = 1
            action_cooldown
            game_over = 0
    


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run= False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        else: 
            clicked = False

    pygame.display.update()

pygame.quit()