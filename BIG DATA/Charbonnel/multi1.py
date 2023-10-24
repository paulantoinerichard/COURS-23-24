#!/bin/env python3
import os, sys, glob, time, importlib, logging


# POUR LANCER, DEFINIR UNE VARIABLE DANS LE TERMINAL
# export PYTHONPATH="./jobs"
# PUIS LANCER AVEC : python3 multi1.py './jobs'

logging.basicConfig(level=logging.DEBUG, filename="app.log", filemode="w", format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    path_jobs = sys.argv[1]
    os.chdir(path_jobs)
    jobs_files = glob.glob('*.py')
    jobs = [module[:-3] for module in jobs_files]
    for job in jobs:
        module = importlib.import_module(job)
        start_time = time.time()
        try:
            resultat = module.run()
            finish_time = time.time()
            status = "Le lancement a bien fonctionné."
        except Exception as e:
            finish_time = time.time()
            resultat = str(e)
            status = "Ne s'est pas exécuté correctement."

        logging.info(f"File_name = {job}.py,\t Début : {start_time},\t Fin : {finish_time}")
        logging.info(f"Temps total : {finish_time-start_time}")
        logging.info(f"Statut : {status}")
        logging.info(f" ")
        with open(f"{job}.result", "w") as fichier:
            fichier.write(str(resultat))