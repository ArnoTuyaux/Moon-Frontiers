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


def game():
    pass

