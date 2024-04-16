import pygame


class Button:
    def __init__(self, x, y, img, scale):
        width = img.get_width()
        height = img.get_height()
        self.x = x
        self.y = y
        self.img = pygame.transform.scale(img, (int(width * scale), int(height * scale)))
        self.rect = self.img.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.clicked = False

    def draw(self, surface):
        action = False

        # Récupérer position souris
        pos = pygame.mouse.get_pos()

        # Tester si souris au dessus de l'image et image cliquée
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
        surface.blit(self.img, (self.rect.x, self.rect.y))

        return action

    def redefinition_rect(self):
        self.rect = self.img.get_rect()
        self.rect.topleft = (self.x, self.y)
