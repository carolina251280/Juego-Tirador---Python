from pygame import *
from random import randint
#música de fondo
mixer.init()
mixer.music.load('space.mp3')
mixer.music.play()
sonido_fuego = mixer.Sound('fire.ogg')
sonido_derrota = mixer.Sound('derrota.mp3')
sonido_victoria = mixer.Sound('victoria.mp3')
#fuentes y subtítulos
font.init()
font1 = font.Font(None, 36) #Tabla de puntuación
font2 = font.Font(None, 80) #Mensaje final
mensaje_ganar = font2.render('¡YOU WIN!', True, (10, 255, 10))
mensaje_perder = font2.render('¡YOU LOST!', True, (255, 0, 0))

#Imágenes
img_fondo = 'fondo.jpg'
img_jugador = 'rocket.png'  
img_enemigo = 'ufo.png'
img_bala = 'bala.png'
score = 0 #naves destruidas
lost = 0 #naves falladas

#Crear una ventana
ancho_ventana = 700
alto_ventana = 500
display.set_caption("Tirador")
ventana = display.set_mode((ancho_ventana, alto_ventana))
fondo = transform.scale(image.load(img_fondo),(ancho_ventana, alto_ventana))

#clase padre para otros objetos
class GameSprite(sprite.Sprite):
 #constructor de clase
   def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
       #Llamada al constructor de la clase (Sprite):
       sprite.Sprite.__init__(self)


       #cada objeto debe almacenar la propiedad image
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed


       #cada objeto debe tener la propiedad rect – el rectángulo en el que está
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y
 #método de dibujo del personaje en la ventana
   def reset(self):
       ventana.blit(self.image, (self.rect.x, self.rect.y))

#clase de jugador principal
class Player(GameSprite):
   #método para controlar el objeto con las teclas de las flechas
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < ancho_ventana - 80:
            self.rect.x += self.speed
    #método para “disparar” (usa la posición del jugador para crear una bala)
    def fire(self):
        bullet = Bullet(img_bala, self.rect.centerx, self.rect.top, 30, 35, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    #movimiento del enemigo
    def update(self):
        self.rect.y += self.speed
        global lost

        if self.rect.y > alto_ventana:
            self.rect.x = randint(80, ancho_ventana - 80)
            self.rect.y = 0
            lost +=1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()



jugador = Player(img_jugador,5, alto_ventana - 100, 80, 100, 10)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemigo,randint(80, ancho_ventana - 80), -40, 80, 50, randint(1,5))
    monsters.add(monster)

bullets = sprite.Group()

finish = False
run = True
while run:
    #Evento de pulsado del botón "cerrar"
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                jugador.fire()
                sonido_fuego.play()

    if not finish:
        #actualizar el fondo
        ventana.blit(fondo,(0,0))

        #escribe texto en la pantalla
        text_lose = font1.render("Fallos: " + str(lost), 1, (39, 211, 245))
        ventana.blit(text_lose, (10, 50))

        text = font1.render("Puntos: " + str(score), 1, (39, 211, 245))
        ventana.blit(text, (10, 20)) 

        jugador.update()
        monsters.update()
        bullets.update()
        jugador.reset()
        monsters.draw(ventana)
        bullets.draw(ventana)

        colision = sprite.groupcollide(monsters, bullets, True, True)
        for c in colision:
            score += 1
            monster = Enemy(img_enemigo,randint(80, ancho_ventana - 80), -40, 80, 50, randint(1,5))
            monsters.add(monster)

        if sprite.spritecollide(jugador, monsters, False) or lost >= 3:
            sonido_derrota.play()
            finish = True
            ventana.blit(mensaje_perder, (200, 200))

        if score >= 10:
            finish = True
            ventana.blit(mensaje_ganar, (200, 200))
            sonido_victoria.play()

        display.update()
    
    #el ciclo se ejecuta cada 0.05seg
    time.delay(50)