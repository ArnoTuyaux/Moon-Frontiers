import pygame
import sys

pygame.init()

# Paramètres du jeu
largeur_fenetre = 800
hauteur_fenetre = 600
fenetre = pygame.display.set_mode((largeur_fenetre, hauteur_fenetre))
pygame.display.set_caption("Reconstruction Spatiale")

blanc = (255, 255, 255)
noir = (0, 0, 0)

# Classe représentant une colonie
class Colonie:
    def __init__(self, nom, position):
        self.nom = nom
        self.position = position
        self.lab_recherche = 1
        self.support_vie = 1
        self.foreuses = 4
        self.centrale_energie = 1
        self.usine_materiel = 1
        self.defense = 1
        self.population = 100

    def afficher_info(self):
        print(f"Colonie {self.nom}: Population - {self.population}, Labo - {self.lab_recherche}, "
              f"Support de vie - {self.support_vie}, Foreuses - {self.foreuses}, "
              f"Centrale d'énergie - {self.centrale_energie}, Usine de matériel - {self.usine_materiel}, "
              f"Défense - {self.defense}")

# Fonction principale
def jeu():
    colonies = [Colonie("Lune", (100, 100))]  # Initialisation avec une colonie sur la Lune

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Affichage de la carte
        fenetre.fill(blanc)
        for colonie in colonies:
            pygame.draw.circle(fenetre, noir, colonie.position, 10)

        # Affichage des informations sur la colonie (à améliorer)
        colonies[0].afficher_info()

        pygame.display.flip()

# Lancement du jeu
jeu()
