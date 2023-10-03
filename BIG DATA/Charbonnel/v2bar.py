import time, sys
from abc import ABC, abstractmethod
import argparse

# Créer un objet ArgumentParser pour gérer les arguments en ligne de commande
parser = argparse.ArgumentParser(description='Script de gestion des commandes de bar')
parser.add_argument('commandes', nargs='+', help='Liste des commandes à exécuter')
parser.add_argument('--verb1', action='store_true', help='Niveau de verbosité 1')
parser.add_argument('--verb2', action='store_true', help='Niveau de verbosité 2')
parser.add_argument('--verb3', action='store_true', help='Niveau de verbosité 3')

class Accessoire(ABC):
    def __init__(self):
        self.etat = []

    def ajouter(self, item):
        self.etat.append(item)
        if args.verb2 or args.verb3:  # Afficher uniquement si verb2 ou verb3
            print(f"[{self.__class__.__name__}] '{item}' ajouté")
        if args.verb3:  # Afficher uniquement si verb2 ou verb3
            print(f"[{self.__class__.__name__}] état={self.etat}")

    def retirer(self):
        if args.verb3:  # Afficher uniquement si verb2 ou verb3
            print(f"[{self.__class__.__name__}] état={self.etat}")
        if not self.est_vide():
            item = self.etat.pop()
            if args.verb2 or args.verb3:  # Afficher uniquement si verb2 ou verb3
                print(f"[{self.__class__.__name__}] '{item}' retiré")
            return item
        else:
            if args.verb1 or args.verb2 or args.verb3:  # Afficher uniquement si verb1, verb2 ou verb3
                print(f"{self.__class__.__name__} est vide")

    def est_vide(self):
        return not bool(self.etat)

class Pic(Accessoire):
    pass

class Bar(Accessoire):
    pass

class Serveur:
    def __init__(self, pic, bar, commandes):
        self.pic = pic
        self.bar = bar
        self.commandes = commandes

    def prendre_commande(self):
        if self.commandes:
            commande = self.commandes.pop()
            print(f"[{self.__class__.__name__}] je prends commande de '{commande}'")
            self.pic.ajouter(commande)
            time.sleep(1)  # Pause d'une seconde pour simuler la prise de commande
        else:
            print(f"[{self.__class__.__name__}] il n'y a plus de commande à prendre")
            print("plus de commande à prendre")

    def servir(self):
        if self.bar.etat:
            cocktail = self.bar.retirer()
            print(f"[{self.__class__.__name__}] je sers '{cocktail}'")
        else:
            print("Bar est vide")

class Barman:
    def __init__(self, pic, bar):
        self.pic = pic
        self.bar = bar

    def preparer(self, commande):
        if commande!=None:
            print(f"[{self.__class__.__name__}] je commence la fabrication de '{commande}'")
            time.sleep(2.0 * int(commande.split()[0]))
            print(f"[{self.__class__.__name__}] je termine la fabrication de '{commande}'")
            self.bar.ajouter(commande)
        else:
            return

def main():
    args = parser.parse_args()

    commandes = args.commandes
    pic = Pic()
    bar = Bar()
    serveur = Serveur(pic, bar, commandes)
    barman = Barman(pic, bar)

    print("[Serveur] prêt pour le service !")
    print("[Barman] prêt pour le service")

    for _ in range(len(commandes) +1):
        serveur.prendre_commande()

    for _ in range(len(pic.etat) + 1):
        commande = pic.retirer()
        barman.preparer(commande)

    for _ in range(len(bar.etat) + 1):
        serveur.servir()

    if args.verb1:
        # Afficher des informations de verbosité de niveau 1
        print("Niveau de verbosité 1 activé")
    elif args.verb2:
        # Afficher des informations de verbosité de niveau 2
        print("Niveau de verbosité 2 activé")
    elif args.verb3:
        # Afficher des informations de verbosité de niveau 3
        print("Niveau de verbosité 3 activé")

if __name__ == "__main__":
    main()

