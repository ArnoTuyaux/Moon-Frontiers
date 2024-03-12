from settings import *
from button import Button
from solar_system import draw_solar_system

# Définition de la fenêtre de jeu
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moon Frontiers")
bg_img = pygame.image.load("../assets/Space_Background.png")
background = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.Font("../font/ethnocentric rg.otf", 104)

# Définitions des images des boutons
start_img = pygame.image.load("../assets/Start_BTN.png").convert_alpha()
exit_img = pygame.image.load("../assets/Exit_BTN.png").convert_alpha()

# Positionnement des boutons
start_btn = Button(SCREEN_WIDTH//3 + start_img.get_width() * 0.8 / 2, SCREEN_HEIGHT//2, start_img, 0.8)
exit_btn = Button(SCREEN_WIDTH//3 + exit_img.get_width() * 0.8 / 2, SCREEN_HEIGHT//2 + exit_img.get_height(), exit_img, 0.8)


def main():
    clock = pygame.time.Clock()
    pos_x_bg = 0  # Position initiale du background
    running = True

    while running:
        clock.tick(fps)  # Taux de rafraichissement de l'image

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False


        # Affichage du background
        screen.blit(background, (pos_x_bg, 0))
        screen.blit(background, (SCREEN_WIDTH + pos_x_bg, 0))

        # Gère l'actualisation de l'image d'arrière plan
        if pos_x_bg == -SCREEN_WIDTH:
            pos_x_bg = 0
        pos_x_bg -= 1

        # Affichage du titre
        title1 = font.render("Moon", True, 'white')
        title2 = font.render(" Frontiers", True, 'white')
        screen.blit(title1, (SCREEN_WIDTH//2 - title1.get_width()//2, SCREEN_HEIGHT//5))
        screen.blit(title2, (SCREEN_WIDTH//2 - title2.get_width()//2, SCREEN_HEIGHT//5 + 104))

        # Affichage des boutons
        if start_btn.draw(screen):
            pos_x_bg = draw_solar_system(screen, pos_x_bg)
        if exit_btn.draw(screen):
            running = False

        # Mise à jour de l'affichage
        pygame.display.flip()


if __name__ == "__main__":
    main()
    pygame.quit()
