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
gl_work={'ser':1,'bar':1,'com':1}

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
        if args.verb2 or args.verb3:  
            print(f"[{temps()} - {self.__class__.__name__}] '{item}' ajouté")
        if args.verb3:  
            print(f"[{temps()} - {self.__class__.__name__}] état={self.etat}")

    def retirer(self):
        if not self.est_vide():
            item = self.etat.pop()
            if args.verb2 or args.verb3:
                print(f"[{temps()} - {self.__class__.__name__}] '{item}' retiré")
            return item
        else:
            if args.verb2 or args.verb3:
                print(f"{self.__class__.__name__} est videee")

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
        global gl_cmd,gl_work
        while self.commandes!=[] and gl_cmd:
            commande = self.commandes.pop() 
            print(f"[{temps()} - {self.__class__.__name__}] je prends commande de '{commande}'")
            self.pic.ajouter(commande)
            await asyncio.sleep(0.5)

        print(f"[{temps()} - {self.__class__.__name__}] il n'y a plus de commande à prendre")
        gl_work['com']=0
        if args.verb2 or args.verb3:
            print("plus de commande à prendre")
        gl_cmd = False  # Modifier gl_cmd à False ici
        


    async def servir(self):
        global gl_sv, gl_prep, gl_work
        while not (gl_work['ser']==0 and gl_work['bar']==0 and gl_work['com']==0):
            if len(self.bar.etat)>0:
                gl_work['ser']=1
                cocktail = self.bar.retirer()
                print(f"[{temps()} - {self.__class__.__name__}] je sers '{cocktail}'")
                await asyncio.sleep(0.7)
            elif gl_work['bar']==1:
                gl_work['ser']=1
                await asyncio.sleep(0)
            else:
                gl_work['ser']=0
                await asyncio.sleep(0)
        gl_sv = False
        #print("Bar est vide")


class Barman:
    def __init__(self, pic, bar):
        self.pic = pic
        self.bar = bar

    async def preparer(self):
        global gl_prep,gl_work
        while not (gl_work['ser']==0 and gl_work['bar']==0 and gl_work['com']==0):
            if len(self.pic.etat)>0 or gl_work['com']==1:  # Vérifiez si la liste pic n'est pas vide
                gl_work['bar']=1
                commande = self.pic.retirer()
                print(f"[{temps()} - {self.__class__.__name__}] je commence la fabrication de '{commande}'")
                await asyncio.sleep(2.0)
                print(f"[{temps()} - {self.__class__.__name__}] je termine la fabrication de '{commande}'")
                self.bar.ajouter(commande)
            else:
                gl_work['bar']=0
                await asyncio.sleep(0)
        print('plus de preparations en cours')
        gl_prep = False


async def main():
    try:
        commandes = args.commandes
        pic = Pic()
        bar = Bar()
        serveur = Serveur(pic, bar, commandes)
        barman = Barman(pic, bar)

        async def fin_journee():
            global gl_work
            while True:
                if gl_work['ser']==0 and gl_work['bar']==0 and gl_work['com']==0:
                    quit()
                else:
                    await asyncio.sleep(0)


        print(f"[{temps()} - Serveur] prêt pour le service !")
        print(f"[{temps()} - Barman] prêt pour le service")

        # Exécutez les tâches en séquence
        await asyncio.gather(serveur.prendre_commande(), barman.preparer(), serveur.servir())
    except Exception as e:
        #print(f"Exception: {e}")
        pass

if __name__ == "__main__":
    args = parser.parse_args()
    start_time = time.time()
    asyncio.run(main())
