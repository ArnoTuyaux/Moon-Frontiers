import time

from settings import *
from classes import Sun, Planet, Moon
from menu_planet import menu_planet


def draw_solar_system(screen, pos_x_bg):
    clock = pygame.time.Clock()

    # Initialisation des images
    font = pygame.font.Font('../font/ethnocentric rg.otf', 45)
    bg_img = pygame.image.load("../assets/Space_Background.png")
    background = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    cursor = pygame.image.load('../assets/cursor.png')
    stats_bar = pygame.image.load('../assets/Stats_Bar.png')

    sun = Sun()
    running = True
    current_planet = 1

    planet_list = []
    for planet_name, planet_data in planets_data.items():
        moons = [Moon(moon_name, i + 1, (308.0, 194)) for i, moon_name in enumerate(planet_data['moons'])]
        planet = Planet(planet_name, moons, planet_data['position'])
        planet_list.append(planet)

    # planet_test = Planet("Mars", planets_data["Mars"]["moons"], planets_data["Mars"]["position"])

    # Calcul de positions
    available_space = SCREEN_WIDTH - 300  # Calcul de l'éspace de l'écran restant (soleil)
    spacing = available_space / 9  # Distance entre chaque planetes
    intial_c_position = 300 + spacing  # Position initial du curseur

    stats_bar_pos = (SCREEN_WIDTH // 2 - stats_bar.get_width() // 2, 0)

    time.sleep(0.065)

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
            if planet.draw(screen):
                pos_x_bg = menu_planet(screen, pos_x_bg, planet_list, current_planet)
            if planet.over:
                current_planet = planet.number
            # print(planet.name, planet.moons, planet.number)

        # Affichage curseur
        cursor_position_x = intial_c_position + (current_planet-1) * spacing - cursor.get_width()//2
        screen.blit(cursor, (cursor_position_x, SCREEN_HEIGHT//2 - cursor.get_height()//2))

        screen.blit(stats_bar, stats_bar_pos)

        # Display current planet name in the middle of the stats bar
        current_planet_name = planet_list[current_planet - 1].name
        text_surface = font.render(current_planet_name, True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, stats_bar_pos[1] + stats_bar.get_height() // 2))
        screen.blit(text_surface, text_rect)

        # print(planet_list[6].moons[0].name)
        # print(planet_test)

        pygame.display.update()