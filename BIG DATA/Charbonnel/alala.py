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

global gl_cmd, gl_prep, gl_sv
gl_cmd, gl_prep, gl_sv= True, True, True


def format_time(seconds):
    return f"{seconds:.2f}s"

start_time = time.time()
def temps():
    return format_time(time.time() - start_time)


class Accessoire(ABC):
    def __init__(self):
        self.etat = []

    async def ajouter(self, item):
        self.etat.append(item)
        if args.verb2 or args.verb3:  
            print(f"[{temps()} - {self.__class__.__name__}] '{item}' ajouté")
        if args.verb3:  
            print(f"[{temps()} - {self.__class__.__name__}] état={self.etat}")
        await asyncio.sleep(1)

    async def retirer(self):
        if not self.est_vide():
            item = self.etat.pop()
            if args.verb2 or args.verb3:
                print(f"[{temps()} - {self.__class__.__name__}] '{item}' retiré")
            return item
        else:
            if args.verb2 or args.verb3:
                print(f"{self.__class__.__name__} est videee")
        await asyncio.sleep(1)

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
        global gl_cmd
        while self.commandes and gl_cmd:
            commande = self.commandes.pop() if self.commandes else None
            print(f"[{temps()} - {self.__class__.__name__}] je prends commande de '{commande}'")
            await self.pic.ajouter(commande)
            await asyncio.sleep(0.5)

        print(f"[{temps()} - {self.__class__.__name__}] il n'y a plus de commande à prendre")
        if args.verb2 or args.verb3:
            print("plus de commande à prendre")
        gl_cmd = False  # Modifier gl_cmd à False ici

    async def servir(self):
        global gl_sv, gl_prep
        while self.bar or gl_prep:
            if not gl_cmd:
                if self.bar:
                    cocktail = await self.bar.retirer()
                    if cocktail is not None:
                        print(f"[{temps()} - {self.__class__.__name__}] je sers '{cocktail}'")
                        await asyncio.sleep(0.7)
                    else:
                        break  # Ignorer les cocktails None
                else:
                    await asyncio.sleep(1.0)
            else:
                await asyncio.sleep(1.0)
        gl_sv = False
        print("Bar est vide")


class Barman:
    def __init__(self, pic, bar):
        self.pic = pic
        self.bar = bar

    async def preparer(self):
        global gl_prep
        while (self.pic != None or gl_cmd == True) and gl_prep == True:
            if self.pic and gl_prep:  # Vérifiez si la liste pic n'est pas vide
                commande = await self.pic.retirer()
                print(f"[{temps()} - {self.__class__.__name__}] je commence la fabrication de '{commande}'")
                await asyncio.sleep(2.0)
                print(f"[{temps()} - {self.__class__.__name__}] je termine la fabrication de '{commande}'")
                await self.bar.ajouter(commande)
            else:
                await asyncio.sleep(1.0)
        print('plus de preparations en cours')
        gl_prep = False
        print(gl_prep)


async def main():
    try:
        commandes = args.commandes
        pic = Pic()
        bar = Bar()
        serveur = Serveur(pic, bar, commandes)
        barman = Barman(pic, bar)

        print(f"[{temps()} - Serveur] prêt pour le service !")
        print(f"[{temps()} - Barman] prêt pour le service")

        # Exécutez les tâches en séquence
        await asyncio.gather(serveur.prendre_commande(), barman.preparer(), serveur.servir())
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    args = parser.parse_args()
    start_time = time.time()
    asyncio.run(main())
