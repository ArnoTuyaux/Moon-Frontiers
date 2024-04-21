from settings import *
from button import Button


class Personnel(Enum):
    MINER = ("Miner", 100)
    ENGINEER = ("Engineer", 150)
    AGRICULTURIST = ("Agriculturist", 200)
    TECHNICIAN = ("Technician", 250)

    def __init__(self, name, salary):
        self._name = name
        self._salary = salary

    @property
    def name(self):
        return self._name

    @property
    def salary(self):
        return self._salary

    def __str__(self):
        return f"{self.name} - Salary: {self.salary} per minute"

class Building(Enum):
    MINERAL_EXTRACTOR = ("Mineral Extractor", 1000.0, 500.0, Personnel.MINER, 1)
    HELIUM_3_EXTRACTOR = ("Helium 3 Extractor", 1200.0, 600.0, Personnel.MINER, 2)
    SMELTERY = ("Smeltery", 1500.0, 750.0, Personnel.ENGINEER, 1)
    SOLAR_FARM = ("Solar Farm", 2000.0, 1000.0, Personnel.AGRICULTURIST, 1)
    HELIUM_3_REFINERY = ("Helium-3 Refinery", 2500.0, 1500.0, Personnel.TECHNICIAN, 3)

    def __init__(self, name, cost, income_per_minute, personnel, required_personnel_count):
        self._name = name
        self._cost = cost
        self._income_per_minute = income_per_minute
        self._personnel = personnel
        self._required_personnel_count = required_personnel_count

    @property
    def name(self):
        return self._name

    @property
    def cost(self):
        return self._cost

    @property
    def income_per_minute(self):
        return self._income_per_minute

    @property
    def personnel(self):
        return self._personnel

    @property
    def required_personnel_count(self):
        return self._required_personnel_count

    def __str__(self):
        return f"{self.name} - Cost: {self.cost}, Income per Minute: {self.income_per_minute}, Required Personnel: {self.personnel.name} ({self.required_personnel_count} required)"


def update_planet_money(planet_list):
    for planet in planet_list:
        planet_money = 0.0

        for moon in planet.moons:
            moon.update_moon_money()

            planet_money += moon.money

            # for person in moon.personnel:
            #     total_money += person.salary / 60 d
        planet.money = round(planet_money, 1)


def game(screen, planet_list, current_moon, pos_x_bg):
    clock = pygame.time.Clock()
    font = pygame.font.Font('../font/ethnocentric rg.otf', 25)
    plus_button = pygame.image.load('../assets/Plus_BTN.png').convert_alpha()
    plus_button = pygame.transform.scale(plus_button, (int(plus_button.get_width() * 0.5),
                                                       int(plus_button.get_height() * 0.5)))
    plus_button_off = pygame.image.load('../assets/Plus_BTN_off.png').convert_alpha()
    plus_button_off = pygame.transform.scale(plus_button_off, (int(plus_button_off.get_width() * 0.5),
                                                               int(plus_button_off.get_height() * 0.5)))
    farm_button = pygame.image.load('../assets/Farm_BTN.png').convert_alpha()
    farm_button = pygame.transform.scale(farm_button, (int(farm_button.get_width() * 0.5),
                                                       int(farm_button.get_height() * 0.5)))
    bg_img = pygame.image.load("../assets/Space_Background.png")
    background = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    building_buttons = []

    button_y = 50
    for _ in Building:
        button = Button(100, button_y, plus_button, 0.5)
        building_buttons.append(button)
        button_y += 150

    farm_button = Button(1000, 50, farm_button, 2)

    running = True
    last_update_time = time.time()

    while running:
        clock.tick(60)
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return pos_x_bg
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return pos_x_bg

        if pos_x_bg == -SCREEN_WIDTH:
            pos_x_bg = 0
        pos_x_bg -= 1

        # Calcule le temps depuis la dernière update
        current_time = time.time()
        time_elapsed = current_time - last_update_time

        current_moon.set_passive_income()

        # Update l'argent de la lune en fonction du temps passé
        if time_elapsed >= 1:
            current_moon.update_moon_money()
            last_update_time = current_time

        screen.blit(background, (pos_x_bg, 0))
        screen.blit(background, (SCREEN_WIDTH + pos_x_bg, 0))

        moon_money = font.render(str(round(current_moon.money)), True, CYAN)
        screen.blit(moon_money, (0, 0))
        # screen.blit(font.render(str(current_time), True, CYAN), (100, 100))

        if farm_button.draw(screen):
            current_moon.money += 10

        # Display building buttons and handle purchases
        for button, building in zip(building_buttons, Building):
            building_text = building.name + "       Cout : " + str(round(building.cost))
            text_surface = font.render(building_text, True, (255, 255, 255))
            screen.blit(text_surface, (250, button.rect.y + button.rect.height//2))

            if current_moon.money >= building.cost:
                button.img = plus_button
                button.redefinition_rect()
            else:
                button.img = plus_button_off
                button.redefinition_rect()

            if button.draw(screen):
                if current_moon.money >= building.cost:
                    current_moon.money -= building.cost
                    round(current_moon.money, 1)
                    current_moon.buildings.append(building)

        pygame.display.update()

