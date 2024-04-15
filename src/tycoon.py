from settings import *


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
    MINERAL_EXTRACTOR = ("Mineral Extractor", 1000, 50, Personnel.MINER, 1)
    SMELTERY = ("Smeltery", 1500, 75, Personnel.ENGINEER, 1)
    SOLAR_FARM = ("Solar Farm", 2000, 100, Personnel.AGRICULTURIST, 1)
    HELIUM_3_EXTRACTOR = ("Helium 3 Extractor", 1200, 60, Personnel.MINER, 2)
    HELIUM_3_REFINERY = ("Helium-3 Refinery", 2500, 150, Personnel.TECHNICIAN, 3)

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
        # Initialize total money earned for the planet
        total_money = 0

        # Calculate money earned from buildings on the planet
        for moon in planet.moons:
            # Initialize total money earned for the moon
            total_money_moon = 0

            # Calculate money earned from buildings on the moon
            for building in moon.buildings:
                total_money_moon += building.income_per_minute

            # Calculate money earned from personnel on the moon
            for person in moon.personnel:
                total_money_moon += person.salary

            # Update moon's money
            moon.money += total_money_moon

            # Add moon's money to the total money earned for the planet
            total_money += moon.money

        # Update planet's money
        planet.money += total_money


def game(screen, planet_list, current_moon):
    clock = pygame.time.Clock()
    font = pygame.font.Font('../font/ethnocentric rg.otf', 25)

    running = True
    last_update_time = time.time()

    while running:
        clock.tick(60)
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        # Calculate time since last update
        current_time = time.time()
        time_elapsed = current_time - last_update_time

        current_moon.set_passive_income()

        # Update the player's money based on passive income
        if time_elapsed >= 1:
            current_moon.money += round(current_moon.passive_income / 60, 1)
            last_update_time = current_time
            current_moon.money = round(current_moon.money, 1)
        screen.fill((0, 0, 0))  # Clear the screen
        moon_money = font.render(str(current_moon.money), True, CYAN)
        screen.blit(moon_money, (0, 0))
        # screen.blit(font.render(str(current_time), True, CYAN), (100, 100))

        pygame.display.update()

