import pygame


class Area:
    def __init__(self, x=0, y=0, width=10, height=10, color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.fill_color = back
        if color:
            self.fill_color = color

    def set_color(self, new_color):
        self.fill_color = new_color

    def set_color_out(self, new_color, thickness):
        pygame.draw.rect(mw, new_color, self.rect, thickness)

    def fill(self):
        pygame.draw.rect(mw, self.fill_color, self.rect)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

    def colliderect(self, rect):
        return self.rect.colliderect(rect)


class Picture(Area):
    def __init__(self, filename, x=0, y=0, width=10, height=10):
        Area.__init__(self, x=x, y=y, width=width, height=height)
        self.image = pygame.image.load(filename)

    def draw(self, shift_x=0, shift_y=0):
        pygame.draw.rect(mw, self.fill_color, self.rect)
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


class Label(Area):
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.text = text
        self.image = pygame.font.SysFont('gabriola', fsize, True, False).render(text, True, text_color)

    def draw(self, shift_x=0, shift_y=0):
        pygame.draw.rect(mw, self.fill_color, self.rect)
        mw.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))


pygame.init()
back = 87, 80, 255
mw = pygame.display.set_mode((500, 500))
mw.fill(back)
ball = Picture('ball.png', 250, 270, 50, 50)
platform = Picture('platform.png', 260, 410, 100, 25)
backside = Picture('backside.jpg', 0, 0, 500, 500)
game_over = False
move_right = False
move_left = False
speed_x = 3
speed_y = 3
clock = pygame.time.Clock()
monsters = list()
n = 9

for j in range(3):
    x = 5 + (27 * j)
    y = 5 + (55 * j)

    for i in range(n):
        enemy = Picture('enemy.png', x, y, 50, 50)
        monsters.append(enemy)
        x += 55
    n -= 1

while not game_over:
    ball.fill()
    platform.fill()

    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.QUIT:
                game_over = True

            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move_right = True

            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_left = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.QUIT:
                game_over = True

            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                move_right = False

            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                move_left = False

    if move_right:
        platform.rect.x += 3

    elif move_left:
        platform.rect.x -= 3

    ball.rect.x += speed_x
    ball.rect.y += speed_y

    if ball.rect.y < 0:
        speed_y *= -1

    if ball.rect.x > 450 or ball.rect.x < 0:
        speed_x *= -1

    if ball.colliderect(platform.rect):
        speed_y *= -1

    for m in monsters:
        m.draw()

        if m.rect.colliderect(ball.rect):
            monsters.remove(m)
            m.fill()
            speed_y *= -1

    if ball.rect.y > (platform.rect.y + 10):
        time_text = Label(150, 200, 50, 50, back)
        time_text.set_text('YOU    LOSE', 70, (255, 0, 0))
        time_text.draw(10, 10)
        print('YOU LOSE')
        game_over = True

    if len(monsters) == 0:
        time_text = Label(150, 200, 50, 50, back)
        time_text.set_text('YOU    WIN', 70, (200, 255, 200))
        time_text.draw(10, 10)
        print('YOU WIN')
        game_over = True

    ball.draw()
    platform.draw()
    clock.tick(70)
    pygame.display.update()