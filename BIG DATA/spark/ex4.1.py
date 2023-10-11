import json
import pandas as pd

# Question 1 

page_visits, user_visits = {}, {}

with open('/users/2024/ds2/118004830/Téléchargements/anonymous-msweb/anonymous-msweb.data', 'r') as f:
    for line in f:
        if line.startswith("A,"):
            partss = line.split(",")
            page_id = partss[1]
            title = partss[3].strip('"')
            page_visits[page_id] = page_visits.get(page_id, 0) + 1

        elif line.startswith("V,"):
            parts = line.split(",")  
            id=parts[1]
            if id in page_visits:
                user_visits[id] = user_visits.get(id, 0) + 1

for _ in range (len(user_visits)):
    if user_visits[1] >600:
        print(user_visits)


#Question 1
page_visits = {}

with open('/users/2024/ds2/118004830/Téléchargements/anonymous-msweb/anonymous-msweb.data', 'r') as f:
    for line in f:
        if line.startswith("V,"):
            parts = line.split(",")  
            page_id = parts[1]
            page_visits[page_id] = page_visits.get(page_id, 0) + 1

for page_id, visit_count in page_visits.items():
    if visit_count > 600:
        print(f"Page ID {page_id} a été visitée plus de 600 fois : {visit_count}")

#Question 2









