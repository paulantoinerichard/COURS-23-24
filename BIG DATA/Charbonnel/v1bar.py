import time, sys
from abc import ABC, abstractmethod
import argparse

class Accessoire(ABC):
    def __init__(self):
        self.etat = []

    def ajouter(self, item):
        self.etat.append(item)
        print(f"[{self.__class__.__name__}] '{item}' ajouté")
        print(f"[{self.__class__.__name__}] état={self.etat}")

    def retirer(self):
        print(f"[{self.__class__.__name__}] état={self.etat}")
        if not self.est_vide():
            item = self.etat.pop()
            print(f"[{self.__class__.__name__}] '{item}' retiré")
            return item
        else:
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
    if len(sys.argv) < 2:
        print("Utilisation : python v2bar.py [liste de commandes]")
        return

    commandes = sys.argv[1:]
    pic = Pic()
    bar = Bar()
    serveur = Serveur(pic, bar, commandes)
    barman = Barman(pic, bar)

    print("[Serveur] prêt pour le service !")
    print("[Barman] prêt pour le service")

    for _ in range(len(commandes)+1):
        serveur.prendre_commande()

    for _ in range(len(pic.etat) + 1):
        commande = pic.retirer()
        barman.preparer(commande)

    for _ in range(len(bar.etat) + 1):
        serveur.servir()

if __name__ == "__main__":
    main()

