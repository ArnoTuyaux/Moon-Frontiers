import time

from settings import *
from classes import Sun, Planet, Moon
from menu_planet import menu_planet
from tycoon import *


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

    saved_game_state = load_game_state()

    planet_list = []
    for planet_name, planet_data in planets_data.items():
        saved_moons = None
        if saved_game_state:
            saved_planet = next((planet for planet in saved_game_state if planet['name'] == planet_name), None)
            if saved_planet:
                saved_moons = saved_planet['moons']

        moons = []

        # ------- GESTION DE RECUP DES DONNEES -------
        for i, moon_name in enumerate(planet_data['moons']):
            moon_position = (308.0, 194)
            saved_buildings = []
            saved_personnel = []
            saved_money = 1000.0
            saved_passive_income = 0
            saved_colonized = False

            if saved_moons and i < len(saved_moons):
                moon_data = saved_moons[i]
                moon_position = moon_data.get('position', (308.0, 194))
                saved_buildings = moon_data.get('buildings', [])
                saved_personnel = moon_data.get('personnel', [])
                saved_money = moon_data.get('money', 1000.0)
                saved_passive_income = moon_data.get('passive_income', 0)
                saved_colonized = moon_data.get('colonized', False)

            buildings = []
            if saved_buildings:
                for building_key in saved_buildings:
                    building = Building[building_key]
                    buildings.append(building)

            personnel = []
            if saved_personnel:
                for personnel_data in saved_personnel:
                    if isinstance(personnel_data, dict) and 'name' in personnel_data:
                        personnel_member = Personnel[personnel_data['name']]
                        personnel_count = personnel_data.get('count', 0)
                        personnel.append((personnel_member, personnel_count))
                    else:
                        print("Invalid personnel data:", personnel_data)

            moon = Moon(moon_name, i + 1, moon_position, buildings, personnel)
            moon.money = saved_money
            moon.colonized = saved_colonized
            if moon.name == 'Lune':
                if not moon.colonized:
                    moon.colonized = True
                if moon.money == 0.0:
                    moon.money = 1000.0
            # if moon.name == 'Phobos': # DEBUG
            #     moon.price = 1000.0
            moon.passive_income = saved_passive_income
            moons.append(moon)

        planet_money = 0
        if saved_game_state:
            saved_planet = next((planet for planet in saved_game_state if planet['name'] == planet_name), None)
            if saved_planet:
                planet_money = saved_planet['money']

        planet = Planet(planet_name, moons, planet_data['position'])
        planet.money = planet_money

        planet_list.append(planet)


    planet_surfaces = {}
    for planet in planet_list:
        planet_surfaces[planet.name] = pygame.image.load(f'../assets/planets/{planet.name}.png').convert_alpha()

    # planet_test = Planet("Mars", planets_data["Mars"]["moons"], planets_data["Mars"]["position"])

    # Calcul de positions
    available_space = SCREEN_WIDTH - 300  # Calcul de l'éspace de l'écran restant (soleil)
    spacing = available_space / 9  # Distance entre chaque planetes
    intial_c_position = 300 + spacing  # Position initial du curseur

    for planet in planet_list:
        planet.calc_position(initial_pos=intial_c_position, spacing=spacing)

    stats_bar_pos = (SCREEN_WIDTH // 2 - stats_bar.get_width() // 2, 0)



    time.sleep(0.065)
    last_update_time = time.time()

    while running:
        if pos_x_bg == -SCREEN_WIDTH:
            pos_x_bg = 0
        pos_x_bg -= 1

        clock.tick(60)  # Taux de rafraichissement

        # Check des events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game_state(planet_list)
                return pos_x_bg
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    save_game_state(planet_list)
                    return pos_x_bg
                elif event.key == pygame.K_LEFT:
                    if current_planet > 1:
                        current_planet -= 1
                elif event.key == pygame.K_RIGHT:
                    if current_planet < 8:
                        current_planet += 1

        # MAJ money chaque seconde
        current_time = time.time()
        if current_time - last_update_time >= 1:
            update_planet_money(planet_list)
            last_update_time = current_time

        # ---- AFFICHAGE PLANETES / SOLEIL DANS WHILE POUR ANIMATION POTENTIELLE A L'AVENIR ----
        screen.blit(background, (pos_x_bg, 0))
        screen.blit(background, (SCREEN_WIDTH + pos_x_bg, 0))
        # Affichage soleil
        # pygame.draw.circle(screen, YELLOW, (0, SCREEN_HEIGHT//2), 240)
        screen.blit(sun.image, (sun.pos_x, sun.pos_y))
        # print(sun.get_width(), sun.get_height())

        # Affichage planetes
        # Récupérer position souris
        pos = pygame.mouse.get_pos()
        for planet in planet_list:
            if planet.draw(screen, pos):
                pos_x_bg = menu_planet(screen, pos_x_bg, planet_list, current_planet)
            if planet.over:
                current_planet = planet.number
            # print(planet.name, planet.moons, planet.number)

        # Affichage curseur
        cursor_position_x = intial_c_position + (current_planet-1) * spacing - cursor.get_width()//2
        screen.blit(cursor, (cursor_position_x, SCREEN_HEIGHT//2 - cursor.get_height()//2))

        screen.blit(stats_bar, stats_bar_pos)

        # Nom current_planet sur statbar
        current_planet_name = planet_list[current_planet - 1].name
        text_surface = font.render(current_planet_name, True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, stats_bar_pos[1] + stats_bar.get_height() // 2))
        screen.blit(text_surface, text_rect)

        # print(planet_list[6].moons[0].name)
        # print(planet_test)

        pygame.display.update()
