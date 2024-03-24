from settings import *
from button import Button

def menu_planet(screen, pos_x_bg, planet_list, current_planet):
    clock = pygame.time.Clock()

    # Initialisation des images
    main_font = pygame.font.Font('../font/ethnocentric rg.otf', 45)
    moon_font = pygame.font.Font('../font/ethnocentric rg.otf', 35)
    bg_img = pygame.image.load("../assets/Space_Background.png").convert_alpha()
    background = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    return_img = pygame.image.load("../assets/Exit_BTN.png").convert_alpha()
    list_bar = pygame.image.load('../assets/Window.png').convert_alpha()
    list_bar = pygame.transform.scale_by(list_bar, 0.75)
    stat_bar = pygame.image.load('../assets/Window2.png').convert_alpha()
    stat_bar = pygame.transform.scale_by(stat_bar, 0.75)
    back_button = pygame.image.load("../assets/Backward_BTN.png").convert_alpha()
    forward_button = pygame.image.load("../assets/Forward_BTN.png").convert_alpha()

    list_bar_pos = (SCREEN_WIDTH // 2 - list_bar.get_width() // 2, 0)
    stat_bar_l_pos = (SCREEN_WIDTH // 2 - list_bar.get_width() // 2 - stat_bar.get_width(), 90)
    stat_bar_r_pos = (SCREEN_WIDTH // 2 + list_bar.get_width() // 2, 90)

    back_button = Button(SCREEN_WIDTH // 2 - list_bar.get_width() // 2 - back_button.get_width() // 2,
                         list_bar.get_height() + back_button.get_height() * 0.45, back_button, 0.45)
    forward_button = Button(SCREEN_WIDTH // 2 + list_bar.get_width() // 2, list_bar.get_height()
                            + forward_button.get_height() * 0.45, forward_button, 0.45)
    return_btn = Button(SCREEN_WIDTH // 2 - return_img.get_width() // 2 * 0.8, list_bar.get_height()
                        + return_img.get_height() * 0.8, return_img, 0.8)

    planet_image_pos = (SCREEN_WIDTH // 2 + list_bar.get_width() // 2 + stat_bar.get_width() //2, 50)

    running = True

    while running:
        if pos_x_bg == -SCREEN_WIDTH:
            pos_x_bg = 0
        pos_x_bg -= 1

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return pos_x_bg
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return pos_x_bg

        clock.tick(60)  # Taux de rafraichissement

        # Affichage
        screen.blit(background, (pos_x_bg, 0))
        screen.blit(background, (SCREEN_WIDTH + pos_x_bg, 0))
        screen.blit(list_bar, list_bar_pos)
        screen.blit(stat_bar, stat_bar_r_pos)
        screen.blit(stat_bar, stat_bar_l_pos)

        # Initial position to start blitting the moons
        x_moon_pos = SCREEN_WIDTH // 2 - list_bar.get_width() // 2.5
        y_moon_pos = list_bar.get_height() // 6

        # Loop through the moons of the current planet
        for moon in planet_list[current_planet - 1].moons:

            # Display the name of the moon
            moon_name_text = moon_font.render(moon, True, WHITE)
            screen.blit(moon_name_text, (x_moon_pos, y_moon_pos))  # Place the moon name above the moon image
            # Update the y position for the next moon
            y_moon_pos += 100

        screen.blit(planet_list[current_planet-1].image, planet_image_pos)

        if return_btn.draw(screen):
            return pos_x_bg
        if back_button.draw(screen):
            if current_planet > 1:
                current_planet -= 1
        if forward_button.draw(screen):
            if current_planet < 8:
                current_planet += 1

        # Affichage du nom de la planete sélectionnée
        current_planet_name = planet_list[current_planet - 1].name
        text_surface = main_font.render(current_planet_name, True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, list_bar_pos[1] + list_bar.get_height() // 15))
        screen.blit(text_surface, text_rect)



        pygame.display.update()