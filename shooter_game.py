from pygame import *
from random import randint
font.init()
font1 = font.SysFont('verdana',80)
win = font1.render('YOU WIN!', True, (255,255,255))
lose = font1.render('YOU LOSE!', True, (180,0,0))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

img_bullet = 'bullet.png'
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shmup")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

font.init()
font2 = font.SysFont('verdana',36)

img_back = "galaxy.jpg"
img_bullet = "bullet.png"
img_hero = "rocket.png"
img_enemy = "ufo.png"

lost = 0
score = 0
goal = 10
max_lost = 3



class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top,15,20,-15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0 :
            self.kill()


ship = Player('rocket_1.png',5,win_height - 100,80, 100, 10) 

monsters = sprite.Group()
for i in range(5):
    monster = Enemy("ufo_1.png", randint(80, win_width-80),-40,80,50, randint(1,5))
    monsters.add(monster)

bullets = sprite.Group()

game = True
finish = False

FPS = 60
clock = time.Clock()
 

 
#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
 
 
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()


    if finish != True:
        window.blit(background,(0,0))
        ship.update()
        ship.reset()
        monsters.update()
        monsters.draw(window)
        bullets.draw(window)
        collides = sprite.groupcollide(monsters,bullets, True, True)
        for c in collides:
            score = score +1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80,50,randint(1,5))
            monsters.add(monster)
        if sprite.spritecollide(ship,monsters,False) or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))
        if score >= goal:
            finish = True
            window.blit(win,(200,200))
        text = font2.render("Счёт:"+ str(score),1,(255,255,255))
        window.blit(text,(10,20))
        bullets.update()
        text_lose = font2.render('Пропущено:' +str(lost),1, (255,255,255))
        window.blit(text_lose,(10,50))
        display.update()
    clock.tick(FPS)
