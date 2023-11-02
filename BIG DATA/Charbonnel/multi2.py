import os, sys, glob, time, importlib, logging, multiprocessing, shutil
# sous windows : set PYTHONPATH=.\jobs
# Lancer avec python multi2.py .\jobs 3

def run_job(job):
    # Dans cette fonction, on va créer le app.log, tester si les jobs fonctionnent et ajouter toutes les informations dans le app.log
    logging.basicConfig(level=logging.DEBUG, filename="app.log", filemode="a", format='%(asctime)s - %(levelname)s - %(message)s')
    index, module_name = job  # Découpez le tuple en index et nom_de_module
    start_time = time.time()
    current_process = multiprocessing.current_process()
    process_name = current_process.name

    try:
        module = importlib.import_module(module_name)
        resultat = module.run()
        finish_time = time.time()
        status = "Le lancement a bien fonctionné."
    except Exception as e:
        finish_time = time.time()
        resultat = str(e)
        status = "Ne s'est pas exécuté correctement."

    with open(f"{module_name}.result", "w") as fichier:
        fichier.write(str(resultat))
    logging.info(f'{module_name} executed by process {process_name}')            # Pour savoir quel processeur a effectué quel tâche
    logging.info(f"File_name = {module_name}.py,\t Début : {start_time},\t Fin : {finish_time}")
    logging.info(f"Temps total : {finish_time - start_time}")
    logging.info(f"Statut : {status}")
    logging.info(f" ")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Utilisation : python multi2.py <chemin vers jobs> <nombre de processus>")
        sys.exit(1)
    begin=time.time()                                                        # Début du compte du temps total

    script_path = sys.argv[1]                                                # On récupère les infos de chemin et de n
    nb_processes = int(sys.argv[2])

    os.chdir(script_path)                                                    # On fait une liste de tous les noms des fichiers jobs
    jobs_files = glob.glob('*.py')
    jobs = [module[:-3] for module in jobs_files]
    job_list = list(enumerate(jobs))

    with multiprocessing.Pool(processes=nb_processes) as pool:               # On fait du multiprocessing
        pool.map(run_job, job_list)

    fichier_log_source = 'C:\\Users\\rpaul\\Desktop\\MULTTT\\jobs\\app.log'  # On déplace dans le dossier supérieur le app.log pour le modifier
    dossier_de_destination = 'C:\\Users\\rpaul\\Desktop\\MULTTT'

    shutil.move(fichier_log_source, dossier_de_destination)
    logging.basicConfig(level=logging.DEBUG, filename=os.path.join(dossier_de_destination, 'app.log'), filemode="a", format='%(asctime)s - %(levelname)s - %(message)s')

    logging.info(f"Nombre de processeurs : {nb_processes}, temps total : {time.time()-begin}")     # On ajoute au log le nombre de processeurs ainsi que le temps total

