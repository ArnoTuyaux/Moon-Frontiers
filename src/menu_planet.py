from settings import *
from settings import *
from button import Button
from tycoon import *


def menu_planet(screen, pos_x_bg, planet_list, current_planet):
    clock = pygame.time.Clock()

    # Calcul revenu passif
    update_planet_money(planet_list)

    # Initialisation des images
    main_font = pygame.font.Font('../font/ethnocentric rg.otf', 45)
    moon_font = pygame.font.Font('../font/ethnocentric rg.otf', 35)
    list_moon_text_font = pygame.font.Font('../font/ethnocentric rg.otf', 25)
    bg_img = pygame.image.load("../assets/Space_Background.png").convert_alpha()
    background = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

    return_img = pygame.image.load("../assets/Exit_BTN.png").convert_alpha()
    start_img = pygame.image.load("../assets/Start_BTN.png").convert_alpha()
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
                        + return_img.get_height() * 0.8 * 1.5, return_img, 0.8)
    start_btn = Button(SCREEN_WIDTH // 2 - start_img.get_width() // 2 * 0.8, list_bar.get_height()
                       + start_img.get_height() * 0.8 // 2, start_img, 0.8)

    planet_image_pos = (SCREEN_WIDTH // 2 + list_bar.get_width() // 2 + stat_bar.get_width() // 2.5,
                        stat_bar.get_height() // 5 + 50)
    saturn_image_pos = (SCREEN_WIDTH // 2 + list_bar.get_width() // 2 + stat_bar.get_width() // 2.5 - 100,
                        stat_bar.get_height() // 5 - 50)

    cant_buy_planet_txt1 = "Vous ne possédez pas"
    cant_buy_planet_txt2 = "toutes les lunes de"
    cant_buy_planet_txt3 = "cette planete"
    cant_buy_planet_txt1 = list_moon_text_font.render(cant_buy_planet_txt1, True, RED)
    cant_buy_planet_txt2 = list_moon_text_font.render(cant_buy_planet_txt2, True, RED)
    cant_buy_planet_txt3 = list_moon_text_font.render(cant_buy_planet_txt3, True, RED)

    list_moon_text_1 = "Lunes de cette planète :"
    list_moon_text_2 = "Pas de lunes"
    list_moon_text_1 = list_moon_text_font.render(list_moon_text_1, True, CYAN)
    list_moon_text_2 = list_moon_text_font.render(list_moon_text_2, True, CYAN)

    stat_bar_l = True
    running = True
    last_update_time = time.time()

    while running:
        if pos_x_bg == -SCREEN_WIDTH:
            pos_x_bg = 0
        pos_x_bg -= 1

        # MAJ money chaque seconde
        current_time = time.time()
        if current_time - last_update_time >= 1:
            update_planet_money(planet_list)
            last_update_time = current_time

        # for i, planet in enumerate(planet_list):
        #     money_text = main_font.render(f"Money on {planet.name}: ${game_state['planet_money'][planet.name]}", True, WHITE)
        #     screen.blit(money_text, (10, 10 + i * 30))

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
        if stat_bar_l:
            screen.blit(stat_bar, stat_bar_l_pos)

        # Position initale de l'affichage du nom des lunes
        x_moon_pos = SCREEN_WIDTH // 2 - list_bar.get_width() // 2.5
        y_moon_pos = list_bar.get_height() // 6

        if planet_list[current_planet - 1].moons:
            screen.blit(list_moon_text_1, (x_moon_pos, y_moon_pos))
            stat_bar_l = True
        else:
            screen.blit(list_moon_text_2, (x_moon_pos, y_moon_pos))
            stat_bar_l = False

        y_moon_pos += 100

        # Boucle à travers les lunes de la planete pour écrire leur nom
        first_iteration = True
        for moon in planet_list[current_planet - 1].moons:
            if first_iteration and planet_list[current_planet - 2].colonized and not moon.colonized:
                moon.colonized = True
            first_iteration = False
            buy_button_moon = Button(moon.pos[0] // 2, (moon.pos[1] + moon.rect.height * 1.5 + 300),
                                     moon.buy_img, 1)
            buy_button_planet = Button(planet_image_pos[0] - 150, planet_image_pos[1] + 450, moon.buy_img,  1)
            moon.draw(screen, moon_font, x_moon_pos, y_moon_pos, planet_list[current_planet - 1].moons)

            if not moon.colonized:
                if moon.selected:
                    if moon.price > planet_list[current_planet - 1].money:
                        moon_price_txt = list_moon_text_font.render("Cout : " + str(moon.price), True, RED)
                    else:
                        moon_price_txt = list_moon_text_font.render("Cout : " + str(moon.price), True, WHITE)

                    screen.blit(moon_price_txt, (buy_button_moon.x, buy_button_moon.y - 100))
                    if buy_button_moon.draw(screen):
                        if planet_list[current_planet - 1].money >= moon.price:
                            moon.colonized = True
                            planet_list[current_planet - 1].money -= moon.price
            if not planet_list[current_planet - 1].colonized:
                if buy_button_planet.draw(screen):
                    if planet_list[current_planet - 1].are_all_moons_colonized():
                        if planet_list[current_planet - 1].money >= planet_list[current_planet - 1].price:
                            planet_list[current_planet - 1].money -= planet_list[current_planet - 1].price
                            planet_list[current_planet - 1].colonized = True
                    else:
                        screen.blit(cant_buy_planet_txt1, (buy_button_planet.x - 5, buy_button_planet.y - 100))
                        screen.blit(cant_buy_planet_txt2, (buy_button_planet.x - 5, buy_button_planet.y - 75))
                        screen.blit(cant_buy_planet_txt3, (buy_button_planet.x - 5, buy_button_planet.y - 50))

            y_moon_pos += 100  # Change la valeur de y pour la prochaine lune à afficher

        # Si planete = Jupiter alors position différente (taille de l'image différente)
        if current_planet != 6:
            screen.blit(planet_list[current_planet-1].image, planet_image_pos)
        else:
            screen.blit(planet_list[current_planet-1].image, saturn_image_pos)
        planet_list[current_planet - 1].draw_infos(screen, planet_image_pos)

        # Affichage du nom de la planete sélectionnée
        current_planet_name = planet_list[current_planet - 1].name
        if planet_list[current_planet-1].colonized:
            current_planet_name = planet_list[current_planet - 1].name + " (Colonized)"
        text_surface = main_font.render(current_planet_name, True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, list_bar_pos[1] + list_bar.get_height() // 15))
        screen.blit(text_surface, text_rect)

        current_moon = None
        for moon in planet_list[current_planet - 1].moons:
            if moon.selected:
                current_moon = moon
                break

        # Gestion des boutons
        if return_btn.draw(screen):
            return pos_x_bg
        if start_btn.draw(screen):
            if current_moon:
                if current_moon.colonized:
                    pos_x_bg = game(screen, planet_list, current_moon, pos_x_bg)
        if back_button.draw(screen):
            for moon in planet_list[current_planet - 1].moons:
                if moon.selected:
                    moon.selected = False
            if current_planet > 1:
                current_planet -= 1
        if forward_button.draw(screen):
            for moon in planet_list[current_planet - 1].moons:
                if moon.selected:
                    moon.selected = False
            if current_planet < 8:
                current_planet += 1

        # for planet in planet_list:
        #     print(game_state["planet_money"][planet.name])

        pygame.display.update()
