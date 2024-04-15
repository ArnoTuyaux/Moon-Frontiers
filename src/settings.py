import pygame
import json
import os
import time
from enum import Enum


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
fps = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREY = (100, 100, 100)
ORANGE = (255, 0, 255)
CYAN = (0, 255, 255)

planets_data = {
    "Mercure": {"moons": [], "position": 1},
    "Venus": {"moons": [], "position": 2},
    "Terre": {"moons": ["Lune"], "position": 3},
    "Mars": {"moons": ["Phobos", "Deimos"], "position": 4},
    "Jupiter": {"moons": ["Io", "Europe", "Ganymède", "Callisto"], "position": 5},
    "Saturne": {"moons": ["Titan", "Encelade", "Rhéa", "Mimas"], "position": 6},
    "Uranus": {"moons": ["Titania", "Obéron", "Umbriel", "Ariel"], "position": 7},
    "Neptune": {"moons": ["Triton"], "position": 8},
}

class EnumEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.name
        return super().default(obj)

# Function to load game state from a JSON file
def load_game_state():
    if os.path.exists("game_state.json"):
        with open("game_state.json", "r") as file:
            game_state = json.load(file)
        return game_state
    else:
        return None

# Function to save game state to a JSON file
def save_game_state(planet_list):
    game_state = []
    for planet in planet_list:
        planet_data = {
            'name': planet.name,
            'money': planet.money,
            'moons': []
        }
        for moon in planet.moons:
            moon_data = {
                'name': moon.name,
                'position': moon.pos,
                'buildings': [building._name_ for building in moon.buildings],
                'personnel': [personnel._name_ for personnel in moon.personnel],
                'money': moon.money,
                'passive_income': moon.passive_income
            }
            planet_data['moons'].append(moon_data)
        game_state.append(planet_data)

    with open("game_state.json", "w") as file:
        json.dump(game_state, file, cls=EnumEncoder)
