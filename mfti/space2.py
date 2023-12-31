import pygame as pg
import random


pg.init()

screen_width, screen_height = 800, 600

FPS = 24    # frame per second
clock = pg.time.Clock()

# изображения
bg_img = pg.image.load('src/background.png')
icon_img = pg.image.load('src/ufo.png')

display = pg.display.set_mode((screen_width, screen_height))
pg.display.set_icon(icon_img)
pg.display.set_caption('Космическое вторжение')

sys_font = pg.font.SysFont('arial', 150)
font = pg.font.Font('src/04B_19.TTF', 50)

display.blit(bg_img, (0, 0))
for i in range(3, 0 ,-1):
    text = sys_font.render(str(i), True, 'white')
    display.blit(text, (screen_width / 2 - text.get_width()/2, screen_height / 2 - text.get_height()/2))
    pg.display.flip()
    display.blit(bg_img, (0, 0))
    pg.time.wait(1500)
text = sys_font.render('start', True, 'white')
display.blit(text, (screen_width / 2 - text.get_width()/2, screen_height / 2 - text.get_height()/2))
pg.display.flip()
pg.time.wait(1000)

# игрок
player_img = pg.image.load('src/player.png')
player_width, player_height = player_img.get_size()
player_gap = 10
player_velocity = 10
player_dx = 0
player_x = screen_width/2 - player_width/2
player_y = screen_height - player_height - player_gap

# пуля
bullet_img = pg.image.load('src/bullet.png')
bullet_width, bullet_height = bullet_img.get_size()
bullet_dy = -5
bullet_x = 0
bullet_y = 0
bullet_alive = False    # есть пуля?

# противник
enemy_img = pg.image.load('src/enemy.png')
enemy_width, enemy_height = enemy_img.get_size()
enemy_dx = 0
enemy_dy = 4
enemy_x = 0
enemy_y = 0

def enemy_create():
    """ Создаем противника в случайном месте вверху окна."""
    global enemy_y, enemy_x
    enemy_x = random.randint(0, screen_width - enemy_width)   # screen_width / 2 - enemy_width / 2
    enemy_y = 0

def game_over():
    font = pg.font.Font('src/04B_19.TTF', 50)
    game_over_text = font.render('Game Over', True, 'red')
    w, h = game_over_text.get_size()
    display.blit(bg_img, (0, 0))
    display.blit(game_over_text, (screen_width / 2 - w / 2, screen_height / 2 - h / 2))
    pg.display.flip()
    pg.time.wait(3000)
    pg.quit

def model_update():
    palayer_model()
    bullet_model()
    enemy_model()

def palayer_model():
    global player_x
    player_x += player_dx
    if player_x < 0:
        player_x = 0
    elif player_x > screen_width - player_width:
        player_x = screen_width - player_width

def bullet_model():
    """ Изменяется положение пули."""
    global bullet_y, bullet_alive
    bullet_y += bullet_dy
    # пуля улетела за верх экрана
    if bullet_y < 0:
        bullet_alive = False

def bullet_create():
    global bullet_y, bullet_x, bullet_alive
    bullet_alive = True
    bullet_x = player_x + player_width/2 - bullet_width/2
    bullet_y = player_y - bullet_height

def enemy_model():
    """ Изменение положения противника, рассчет поражений."""
    global enemy_y, enemy_x, bullet_alive
    enemy_x += enemy_dx
    enemy_y += enemy_dy
    if enemy_y > screen_height:
        game_over()
    # пересечение с пулей
    if bullet_alive:
        re = pg.Rect(enemy_x, enemy_y, enemy_width, enemy_height)
        rb = pg.Rect(bullet_x, bullet_y, bullet_width, bullet_height)
        is_crossed = re.colliderect(rb)
        # попал!
        if is_crossed:
            print('BANG!')
            enemy_create()
            bullet_alive = False

def display_redraw():
    display.blit(bg_img, (0, 0))
    display.blit(player_img, (player_x, player_y))
    display.blit(enemy_img, (enemy_x, enemy_y))
    if bullet_alive:
        display.blit(bullet_img, (bullet_x, bullet_y))
    pg.display.update()

def event_processing():
    global player_dx
    running = True
    for event in pg.event.get():
        # нажали крестик на окне
        if event.type == pg.QUIT:
            running = False
        # тут нажимаем на клавиши
        if event.type == pg.KEYDOWN:
            # нажали на q
            if event.key == pg.K_q:
                running = False
            if event.key == pg.K_SPACE:
                if not bullet_alive:
                    bullet_create()
        # движение игрока
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_a or event.key == pg.K_LEFT:
                player_dx = -player_velocity
            if event.key == pg.K_d or event.key == pg.K_RIGHT:
                player_dx = player_velocity
        if event.type == pg.KEYUP:
            player_dx = 0
            # по левому клику мыши стреляем
        if event.type == pg.MOUSEBUTTONDOWN:
            key = pg.mouse.get_pressed()  # key[0] - left, key[2] - right
            print(f'(key[0]=) (bullet_alive=)')
            if not bullet_alive:
                bullet_create()

    clock.tick(FPS)
    return running

running = True
while running:
    model_update()
    display_redraw()
    running = event_processing()
pg.quit()