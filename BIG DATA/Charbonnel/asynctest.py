import time
import asyncio
from abc import ABC
import argparse

# Créer un objet ArgumentParser pour gérer les arguments en ligne de commande
parser = argparse.ArgumentParser(description='Script de gestion des commandes de bar')
parser.add_argument('commandes', nargs='+', help='Liste des commandes à exécuter')
parser.add_argument('--verb1', action='store_true', help='Niveau de verbosité 1')
parser.add_argument('--verb2', action='store_true', help='Niveau de verbosité 2')
parser.add_argument('--verb3', action='store_true', help='Niveau de verbosité 3')


def format_time(seconds):
    return f"{seconds:.2f}s"

start_time = time.time()
def temps():
    return format_time(time.time() - start_time)


class Accessoire(ABC):
    def __init__(self):
        self.etat = []

    def ajouter(self, item):
        self.etat.append(item)
        time.sleep(0.3)
        if args.verb2 or args.verb3:  
            print(f"[{temps()} - {self.__class__.__name__}] '{item}' ajouté")
        if args.verb3:  
            print(f"[{temps()} - {self.__class__.__name__}] état={self.etat}")

    def retirer(self):
        time.sleep(0.8)
        if args.verb3:  
            print(f"[{temps()} - {self.__class__.__name__}] état={self.etat}")
        if not self.est_vide():
            item = self.etat.pop()
            if args.verb2 or args.verb3:  
                print(f"[{temps()} - {self.__class__.__name__}] '{item}' retiré")
            return item
        else:
            if args.verb2 or args.verb3:  
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

    async def prendre_commande(self):
        if self.commandes:
            commande = self.commandes.pop()
            print(f"[{temps()} - {self.__class__.__name__}] je prends commande de '{commande}'")
            self.pic.ajouter(commande)
            await asyncio.sleep(1.5)  # Use asyncio.sleep for non-blocking sleep
        else:
            print(f"[{temps()} - {self.__class__.__name__}] il n'y a plus de commande à prendre")
            if args.verb2 or args.verb3:
                print("plus de commande à prendre")

    async def servir(self):
        if self.bar.etat:
            cocktail = self.bar.retirer()
            print(f"[{temps()} - {self.__class__.__name__}] je sers '{cocktail}'")
            await asyncio.sleep(0.7)  # Use asyncio.sleep for non-blocking sleep
        else:
            if args.verb2 or args.verb3:
                print("Bar est vide")

class Barman:
    def __init__(self, pic, bar):
        self.pic = pic
        self.bar = bar

    async def preparer(self, commande):
        if commande is not None:
            print(f"[{temps()} - {self.__class__.__name__}] je commence la fabrication de '{commande}'")
            print(f"[{temps()} - {self.__class__.__name__}] je termine la fabrication de '{commande}'")
            await asyncio.sleep(2.0)
            self.bar.ajouter(commande)
        else:
            return

async def main():
    if args.verb1:
        print("Niveau de verbosité 1 activé")
    elif args.verb2:
        print("Niveau de verbosité 2 activé")
    elif args.verb3:
        print("Niveau de verbosité 3 activé")

    commandes = args.commandes
    pic = Pic()
    bar = Bar()
    serveur = Serveur(pic, bar, commandes)
    barman = Barman(pic, bar)

    print(f"[{temps()} - Serveur] prêt pour le service !")
    print(f"[{temps()} - Barman] prêt pour le service")

    await asyncio.gather(
        *[serveur.prendre_commande() for _ in range(len(commandes) + 1)],
        *[barman.preparer(pic.retirer()) for _ in range(len(pic.etat) + 1)],
        *[serveur.servir() for _ in range(len(bar.etat) + 1)]
    )

if __name__ == "__main__":
    args = parser.parse_args()
    start_time = time.time()
    asyncio.run(main())
