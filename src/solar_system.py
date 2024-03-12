from settings import *

class Sun:
    def __init__(self):
        self.img_load = pygame.image.load('../assets/Soleil.png').convert_alpha()
        self.image = pygame.transform.scale(self.img_load, (self.img_load.get_width() * 2,
                                                            self.img_load.get_height() * 2))
        self.pos_x = 0 - self.image.get_width()//2
        self.pos_y = SCREEN_HEIGHT//2 - self.image.get_height()//2


class Planet:
    def __init__(self, name, moons, number):
        self.name = name
        self.moons = moons
        self.number = number
        self.image = pygame.image.load(f'../assets/planets/{self.name}.png').convert_alpha()
        self.pos_x = 0
        self.pos_y = SCREEN_HEIGHT//2 - self.image.get_height()//2
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos_x, self.pos_y)
        self.clicked = False
        self.over = False

    def __str__(self):
        return f'{self.name}, {self.moons}, {self.number}'

    def draw(self, surface):
        available_space = SCREEN_WIDTH - 300  # Calcul de l'éspace de l'écran restant (soleil)
        spacing = available_space / 9  # Distance entre chaque planetes
        intial_position = 300 + spacing  # Position initial de la planete

        # Calcul de la position x de la planete
        self.pos_x = intial_position + (self.number-1) * spacing - self.image.get_width()//2

        self.rect.topleft = (self.pos_x, self.pos_y)

        # surface.blit(self.image, (self.pos_x, self.pos_y))  # Affichage

        action = False

        # Récupérer position souris
        pos = pygame.mouse.get_pos()

        # Tester si souris au dessus de l'image
        if self.rect.collidepoint(pos):
            self.over = True
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked is False:
                self.clicked = True
                action = True
        else:
            self.over = False
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # Afficher le bouton à l'écran
        surface.blit(self.image, (self.pos_x, self.pos_y))

        return action



def draw_solar_system(screen, pos_x_bg):
    clock = pygame.time.Clock()

    # Initialisation des images
    font = pygame.font.Font('../font/ethnocentric rg.otf', 52)
    bg_img = pygame.image.load("../assets/Space_Background.png")
    background = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    cursor = pygame.image.load('../assets/cursor.png')
    stats_bar = pygame.image.load('../assets/Stats_Bar.png')

    sun = Sun()
    running = True
    current_planet = 1

    planet_list = []
    for planet_name, planet_data in planets_data.items():
        planet = Planet(planet_name, planet_data['moons'], planet_data['position'])
        planet_list.append(planet)

    # planet_test = Planet("Mars", planets_data["Mars"]["moons"], planets_data["Mars"]["position"])

    # Calcul de positions
    available_space = SCREEN_WIDTH - 300  # Calcul de l'éspace de l'écran restant (soleil)
    spacing = available_space / 9  # Distance entre chaque planetes
    intial_c_position = 300 + spacing  # Position initial du curseur

    stats_bar_pos = (SCREEN_WIDTH // 2 - stats_bar.get_width() // 2, 0)


    while running:
        if pos_x_bg == -SCREEN_WIDTH:
            pos_x_bg = 0
        pos_x_bg -= 1

        clock.tick(60)  # Taux de rafraichissement
        # Check for quit event and handle key presses
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return pos_x_bg
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return pos_x_bg
                elif event.key == pygame.K_LEFT:
                    if current_planet > 1:
                        current_planet -= 1
                elif event.key == pygame.K_RIGHT:
                    if current_planet < 8:
                        current_planet += 1

        ## AFFICHAGE PLANETES / SOLEIL DANS WHILE POUR ANIMATION POTENTIELLE ##
        screen.blit(background, (pos_x_bg, 0))
        screen.blit(background, (SCREEN_WIDTH + pos_x_bg, 0))
        # Affichage soleil
        # pygame.draw.circle(screen, YELLOW, (0, SCREEN_HEIGHT//2), 240)
        screen.blit(sun.image, (sun.pos_x, sun.pos_y))
        # print(sun.get_width(), sun.get_height())


        # Affichage planetes
        for planet in planet_list:
            planet.draw(screen)
            if planet.over:
                current_planet = planet.number
            # print(planet.name, planet.moons, planet.number)

        # Affichage curseur
        cursor_position_x = intial_c_position + (current_planet-1) * spacing - cursor.get_width()//2
        screen.blit(cursor, (cursor_position_x, SCREEN_HEIGHT//2 - cursor.get_height()//2))

        screen.blit(stats_bar, stats_bar_pos)

        # print(planet_test)

        pygame.display.update()