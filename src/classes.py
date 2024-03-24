from settings import *



class Sun:
    def __init__(self):
        self.img_load = pygame.image.load('../assets/Soleil.png').convert_alpha()
        self.image = pygame.transform.scale(self.img_load, (self.img_load.get_width() * 2,
                                                            self.img_load.get_height() * 2))
        self.pos_x = 0 - self.image.get_width()//2
        self.pos_y = SCREEN_HEIGHT//2 - self.image.get_height()//2


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

    def draw(self, surface):
        available_space = SCREEN_WIDTH - 300  # Calcul de l'éspace de l'écran restant (soleil)
        spacing = available_space / 9  # Distance entre chaque planetes
        intial_position = 300 + spacing  # Position initial de la planete

        # Calcul de la position x de la planete
        self.pos_x = intial_position + (self.number-1) * spacing - self.image.get_width()//2

        self.rect.topleft = (self.pos_x, self.pos_y)

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