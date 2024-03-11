import pygame

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