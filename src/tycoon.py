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
    MINERAL_EXTRACTOR = ("Mineral Extractor", 1000, 500, Personnel.MINER, 1)
    SMELTERY = ("Smeltery", 1500, 750, Personnel.ENGINEER, 1)
    SOLAR_FARM = ("Solar Farm", 2000, 1000, Personnel.AGRICULTURIST, 1)
    HELIUM_3_EXTRACTOR = ("Helium 3 Extractor", 1200, 600, Personnel.MINER, 2)
    HELIUM_3_REFINERY = ("Helium-3 Refinery", 2500, 1500, Personnel.TECHNICIAN, 3)

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

        # Calculate money earned from buildings and personnel on each moon
        for moon in planet.moons:
            moon.update_moon_money()

            planet_money += moon.money

            # # Add personnel salaries
            # for person in moon.personnel:
            #     total_money += person.salary / 60  # Convert salary to per second
        planet.money += round(planet_money, 1)


def game(screen, planet_list, current_moon):
    clock = pygame.time.Clock()
    font = pygame.font.Font('../font/ethnocentric rg.otf', 25)
    plus_button = pygame.image.load('../assets/Plus_BTN.png')
    building_buttons = []

    button_y = 50
    for building in Building:
        button = Button(100, button_y, plus_button, 0.5)
        building_buttons.append(button)
        button_y += 150

    running = True
    last_update_time = time.time()

    while running:
        clock.tick(60)
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        # Calcule le temps depuis la dernière update
        current_time = time.time()
        time_elapsed = current_time - last_update_time

        current_moon.set_passive_income()

        # Update l'argent de la lune en fonction du temps passé
        if time_elapsed >= 1:
            current_moon.update_moon_money()
            last_update_time = current_time
        screen.fill((0, 0, 0))
        moon_money = font.render(str(current_moon.money), True, CYAN)
        screen.blit(moon_money, (0, 0))
        # screen.blit(font.render(str(current_time), True, CYAN), (100, 100))

        # Display building buttons and handle purchases
        for button, building in zip(building_buttons, Building):
            text_surface = font.render(building.name, True, (255, 255, 255))
            screen.blit(text_surface, (250, button.rect.y + button.rect.height//2))
            if button.draw(screen):
                if current_moon.money >= building.cost:
                    current_moon.money -= building.cost
                    round(current_moon.money, 1)
                    current_moon.buildings.append(building)

        pygame.display.update()

