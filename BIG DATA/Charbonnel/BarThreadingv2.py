import time, asyncio, argparse, threading
from threading import Lock

# Gérer les arguments de la ligne de commande
parser = argparse.ArgumentParser(description='Script de gestion des commandes de bar')
parser.add_argument('commandes', nargs='+', help='Liste des commandes à exécuter')
parser.add_argument('--verb1', action='store_true', help='Niveau de verbosité 1')
parser.add_argument('--verb2', action='store_true', help='Niveau de verbosité 2')
parser.add_argument('--verb3', action='store_true', help='Niveau de verbosité 3')


# Variable globale utile pour vérifier ou en sont le barman et le serveur
gl_work={'ser':1,'prep':1,'cmd':1, 'ecs':1}

# Fonctions temps qui permettent de rendre la durée depuis le départ
def format_time(seconds):
    return f"{seconds:.2f}s"
start_time = time.time()
def temps():
    return format_time(time.time() - start_time)



# Classe abstraite qui nous permet la création du pic, du bar et du second pic "Servi" pour l'encaissement
class Accessoire(threading.Thread):
    def __init__(self):
        super().__init__()
        self.etat = []
        self.etat_lock = Lock()

    def ajouter(self, item):                                                            # Fonction qui permet d'ajouter un nouvel élément à la liste
        with self.etat_lock:
            self.etat.append(item)
            if args.verb2 or args.verb3:  
                print(f"[{temps()} - {self.__class__.__name__}] '{item}' ajouté")
            if args.verb3:  
                print(f"[{temps()} - {self.__class__.__name__}] état={self.etat}")

    def retirer(self):                                                                  # Fonction qui permet d'enlever le dernier élément de la liste,
        with self.etat_lock:
            if self.etat:                                                               # nécessaire car le dernier embroché est le premier récupéré.
                item = self.etat.pop()
                if args.verb2 or args.verb3:
                    print(f"[{temps()} - {self.__class__.__name__}] '{item}' retiré")
                return item
            else:
                if args.verb2 or args.verb3:
                    print(f"{self.__class__.__name__} est vide")

class Pic(Accessoire):
    pass
class Bar(Accessoire):
    pass
class Servi(Accessoire):
    pass

# On définit les locks
pic_lock = Lock()
bar_lock = Lock()
servi_lock = Lock()
commandes_lock = Lock()

# Classe serveur, pour la prise de commande et le service
class Serveur(threading.Thread):
    def __init__(self, pic, bar, servi, commandes):
        super().__init__()
        self.pic = pic
        self.bar = bar
        self.servi = servi
        self.commandes = commandes

    async def prendre_commande(self):                                   # La prise de commande est la première étape du programme, et donc du serveur
        global gl_work, c
        while self.commandes:                                           # On souhaite prendre des commandes tant qu'il reste une commande dans ma liste commande
            with commandes_lock:
                if self.commandes:
                    commande = self.commandes.pop() 
                    print(f"[{temps()} - {self.__class__.__name__}] je prends commande de '{commande}'")
                    self.pic.ajouter(commande)
                    await asyncio.sleep(1.0)
        gl_work['cmd']=0 
        print(f"[{temps()} - {self.__class__.__name__}] Il n'y a plus de commande à prendre")
        if args.verb2 or args.verb3:                                   
            print("Plus de commande à prendre.")
        

    async def servir(self):                                             # Programme pour servir les coktails
        global gl_work, s
        while self.bar.etat or gl_work['prep']!=0 :                     # Tant que le service ou la préparation n'est pas finie
            with bar_lock:
                if len(self.bar.etat)>0:                              
                    gl_work['ser']=1
                    cocktail = self.bar.retirer()
                    print(f"[{temps()} - {self.__class__.__name__}] sert '{cocktail}'")
                    self.servi.ajouter(cocktail)                
                    await asyncio.sleep(1.5)
                else:
                    await asyncio.sleep(0.0)
        gl_work['ser']=0
        print(f"[{temps()} - {self.__class__.__name__}] Fin de service.")
        if args.verb2 or args.verb3:                                   
            print("Fin de service.")


    def run(self):
        asyncio.run(self.prendre_commande())
        asyncio.run(self.servir())


# Classe Barman, qui récupère les infos des coktails sur le pic, les prépare et les pose sur le bar ; puis qui encaisse
class Barman(threading.Thread):
    def __init__(self, pic, bar, servi):
        super().__init__()
        self.pic = pic
        self.bar = bar
        self.servi = servi

    async def preparer(self):                                   # Préparation des commandes par le barman
        global gl_work, p
        while self.pic.etat or gl_work['cmd']!=0:               # Tant que le service ou la préparation n'est pas finie
            with pic_lock:
                if len(self.pic.etat)>0 :             
                    commande = self.pic.retirer()
                    print(f"[{temps()} - {self.__class__.__name__}] je commence la fabrication de '{commande}'")
                    await asyncio.sleep(3.0)
                    print(f"[{temps()} - {self.__class__.__name__}] je termine la fabrication de '{commande}'")
                    self.bar.ajouter(commande)
                else:
                    await asyncio.sleep(0.0)
        gl_work['prep']=0
        print(f"[{temps()} - {self.__class__.__name__}] Plus de préparations.")
        if args.verb2 or args.verb3:                                   
            print("Fin des préparations.")


    async def encaisser(self):                                  # Fonction pour encaisser les commandes
        global gl_work, e
        while self.servi.etat or gl_work['cmd']!=0 or gl_work['prep']!=0 or gl_work['ser']!=0:
            with servi_lock:           
                if self.servi.etat: 
                    commande = self.servi.retirer()
                    print(f"[{temps()} - {self.__class__.__name__}] '{commande}' encaissé.")
                    await asyncio.sleep(1.2)
                else:
                    await asyncio.sleep(0)
        gl_work['ecs']=0
        print(f"[{temps()} - {self.__class__.__name__}] Plus d'encaissements.")
        if args.verb2 or args.verb3:                                   
            print("Fin des encaissements.")

    def run(self):
        asyncio.run(self.preparer())
        asyncio.run(self.encaisser())


async def main():
    commandes = args.commandes
    pic = Pic()
    bar = Bar()
    servi = Servi()
    serveur = Serveur(pic, bar, servi, commandes)
    barman = Barman(pic, bar, servi)

    print(f"[0.00s - Serveur] prêt pour le service !")
    print(f"[0.00s - Barman] prêt pour le service")

    serveur.start()
    barman.start()

    serveur.join()  
    barman.join()  


if __name__ == "__main__":
    args = parser.parse_args()
    start_time = time.time()
    asyncio.run(main())


# exemples : python3 ProjetBar.py --verb2 "4 mojito" "3 tequila sunrise"
#            python3 ProjetBar.py "4 cafés" "1 planteur" "1 saucisson" --verb3

