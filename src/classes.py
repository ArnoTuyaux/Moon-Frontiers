from settings import *
from collections import Counter
from button import Button

class Sun:
    def __init__(self):
        self.img_load = pygame.image.load('../assets/Soleil.png').convert_alpha()
        self.image = pygame.transform.scale(self.img_load, (self.img_load.get_width() * 2,
                                                            self.img_load.get_height() * 2))
        self.pos_x = 0 - self.image.get_width() // 2
        self.pos_y = SCREEN_HEIGHT // 2 - self.image.get_height() // 2


class Moon:
    def __init__(self, name, number, pos, buildings=None, personnel=None):
        if personnel is None:
            personnel = []
        if buildings is None:
            buildings = []
        self.name = name
        self.number = number
        self.image = pygame.image.load(f'../assets/moons/{self.name}.png').convert_alpha()
        self.cursor_img = pygame.image.load(f'../assets/Table.png').convert_alpha()
        self.buy_img = pygame.image.load(f'../assets/Buy_BTN.png').convert_alpha()
        self.colonized = False
        self.colonizer = 'None'
        self.price = 9999999
        self.money = 0.0
        self.passive_income = 0
        self.rect = self.image.get_rect()
        self.pos = pos
        self.clicked = False
        self.over_text = False
        self.selected = False
        self.rect.topleft = self.pos
        self.buildings = buildings
        self.personnel = personnel

    def __str__(self):
        return f'{self.name}, {self.number}, {self.colonized}'

    def deselect_others(self, moons):
        for other_moon in moons:
            if other_moon != self and other_moon.selected:
                other_moon.selected = False

    def draw(self, surface, font, x, y, moons):
        # Affiche le nom de la lune
        moon_name_text = font.render(self.name, True, WHITE)

        text_rect = moon_name_text.get_rect(topleft=(x, y))
        cursor = pygame.transform.scale(self.cursor_img, (text_rect.width, 2))

        # Test si souris au dessus du texte
        if text_rect.collidepoint(pygame.mouse.get_pos()):
            self.over_text = True
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                # print(self.name)
                self.selected = True
                self.deselect_others(moons)  # Deselctionne les autres lunes
        else:
            self.over_text = False

        # Dessine la lune
        if self.selected:
            surface.blit(self.image, self.pos)
            surface.blit(cursor, (x, y + text_rect.height))
            self.draw_infos(surface)


        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        surface.blit(moon_name_text, text_rect)

    def count_buildings_by_type(self):
        building_counts = Counter(building.name for building in self.buildings)
        return building_counts

    def draw_infos(self, surface):
        font = pygame.font.Font('../font/ethnocentric rg.otf', 25)
        if self.colonized:
            # Count buildings by type
            building_counts = self.count_buildings_by_type()
            if building_counts != Counter():
                # Render each building type separately
                building_surfaces = []
                for building_type, count in building_counts.items():
                    building_text = f"{building_type}: {count}"
                    building_surface = font.render(building_text, True, WHITE)
                    building_surfaces.append(building_surface)

                # Blit sur ecran
                x = self.pos[0] // 2
                y = self.pos[1] + self.rect.height * 1.5
                for building_surface in building_surfaces:
                    surface.blit(building_surface, (x, y))
                    y += building_surface.get_height() + 5  # Espace chaque batiment
            else:
                text1 = font.render("Vous ne possédez", True, WHITE)
                text2 = font.render("pas de batiment", True, WHITE)
                text3 = font.render("sur cette lune", True, WHITE)
                surface.blit(text1, (self.pos[0] // 2, self.pos[1] + self.rect.height * 1.5))
                surface.blit(text2, (self.pos[0] // 2, self.pos[1] + self.rect.height * 1.5 + text1.get_height() + 5))
                surface.blit(text3, (self.pos[0] // 2, self.pos[1] + self.rect.height * 1.5 + text1.get_height() * 2 + 10))

        else:
            text1 = font.render("Vous ne possédez pas", True, RED)
            text2 = font.render("encore cette lune", True, RED)
            surface.blit(text1, (self.pos[0]//2, self.pos[1] + self.rect.height * 1.5))
            surface.blit(text2, (self.pos[0] // 2, self.pos[1] + self.rect.height * 1.5 + text1.get_height() + 5))





    def set_passive_income(self):
        total_income = 0
        for building in self.buildings:
            total_income += building.income_per_minute
        self.passive_income = total_income

    def update_moon_money(self):
        self.money += round(self.passive_income / 60, 1)
        self.money = round(self.money, 1)

    def add_building(self, building):
        self.buildings.append(building)

    def remove_building(self, building):
        self.buildings.remove(building)

    def add_personnel(self, personnel):
        self.personnel.append(personnel)

    def remove_personnel(self, personnel):
        self.personnel.remove(personnel)




class Planet:
    def __init__(self, name, moons, number):
        self.name = name
        self.moons = moons
        self.number = number
        self.image = pygame.image.load(f'../assets/planets/{self.name}.png').convert_alpha()
        self.pos_x = 0
        self.pos_y = SCREEN_HEIGHT // 2 - self.image.get_height() // 2
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos_x, self.pos_y)
        self.clicked = False
        self.over = False
        self.colonized = False
        self.colonizer = 'None'
        self.money = 0.0
        self.price = 0.0
        self.passive_income_rate = 1

    def __str__(self):
        return f'{self.name}, {self.moons}, {self.number}'

    def are_all_moons_colonized(self):
        for moon in self.moons:
            if not moon.colonized:
                return False
        return True

    def calc_position(self, initial_pos, spacing):
        # Calcul de la position x de la planete
        self.pos_x = initial_pos + (self.number - 1) * spacing - self.image.get_width() // 2

        self.rect.topleft = (self.pos_x, self.pos_y)

    def draw(self, surface, pos):
        # surface.blit(self.image, (self.pos_x, self.pos_y))  # Affichage

        action = False

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

    def draw_infos(self, surface, img_pos):
        font = pygame.font.Font('../font/ethnocentric rg.otf', 25)
        money_txt = font.render(str(round(self.money)) + " Crédits", True, WHITE)

        # Blit sur ecran
        x = img_pos[0] - self.rect.width // 2
        y = img_pos[1] + self.rect.height * 1.5
        if self.name == "Saturne":
            x = img_pos[0] - self.rect.width // 6
            y = img_pos[1] + self.rect.height * 0.5
        surface.blit(money_txt, (x, y))

    def buy(self):
        self.colonized = True
        self.colonizer = 'None'