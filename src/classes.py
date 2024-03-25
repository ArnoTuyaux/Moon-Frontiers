from settings import *


class Sun:
    def __init__(self):
        self.img_load = pygame.image.load('../assets/Soleil.png').convert_alpha()
        self.image = pygame.transform.scale(self.img_load, (self.img_load.get_width() * 2,
                                                            self.img_load.get_height() * 2))
        self.pos_x = 0 - self.image.get_width()//2
        self.pos_y = SCREEN_HEIGHT//2 - self.image.get_height()//2


class Moon:
    def __init__(self, name, number, pos):
        self.name = name
        self.number = number
        self.image = pygame.image.load(f'../assets/moons/{self.name}.png').convert_alpha()
        self.cursor_img = pygame.image.load(f'../assets/Table.png').convert_alpha()
        self.colonized = False
        self.colonizer = 'None'
        self.rect = self.image.get_rect()
        self.pos = pos
        self.clicked = False
        self.over_text = False
        self.selected = False
        self.rect.topleft = self.pos

    def __str__(self):
        return f'{self.name}, {self.number}, {self.colonized}'

    def deselect_others(self, moons):
        for other_moon in moons:
            if other_moon != self and other_moon.selected:
                other_moon.selected = False

    def draw(self, surface, font, x, y, moons):
        # Render moon's name text
        moon_name_text = font.render(self.name, True, WHITE)
        text_rect = moon_name_text.get_rect(topleft=(x, y))
        cursor = pygame.transform.scale(self.cursor_img, (text_rect.width, 2))

        # Check if mouse is over the text
        if text_rect.collidepoint(pygame.mouse.get_pos()):
            self.over_text = True
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                print(self.name)  # Print moon's name to console when clicked
                self.selected = True
                self.deselect_others(moons)  # Deselect other moons
        else:
            self.over_text = False

        # Draw moon image
        if self.selected:
            surface.blit(self.image, self.pos)  # Adjust position as needed
            surface.blit(cursor, (x, y + text_rect.height))

        # Reset clicked attribute when mouse button is released
        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        surface.blit(moon_name_text, text_rect)


class Planet:
    def __init__(self, name, moons, number):
        self.name = name
        self.moons = moons
        self.number = number
        self.image = pygame.image.load(f'../assets/planets/{self.name}.png').convert_alpha()
        self.pos_x = 0
        self.pos_y = SCREEN_HEIGHT//2 - self.image.get_height()//2
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.pos_x, self.pos_y)
        self.clicked = False
        self.over = False
        self.colonized = False
        self.colonizer = 'None'

    def __str__(self):
        return f'{self.name}, {self.moons}, {self.number}'

    def calc_position(self, initial_pos, spacing):
        # Calcul de la position x de la planete
        self.pos_x = initial_pos + (self.number - 1) * spacing - self.image.get_width() // 2

        self.rect.topleft = (self.pos_x, self.pos_y)

    def draw(self, surface):
        # surface.blit(self.image, (self.pos_x, self.pos_y))  # Affichage

        action = False

        # Récupérer position souris
        pos = pygame.mouse.get_pos()

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
