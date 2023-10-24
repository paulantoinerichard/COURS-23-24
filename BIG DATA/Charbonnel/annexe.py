import re

matching_lines = []
integer_part_list = []  # Liste pour stocker les parties entières des nombres
pattern = r"Temps total : (.*?)$"

with open("app.log", "r") as log_file:
    lines = log_file.readlines()

for line in lines:
    if re.search(r'Temps total :', line):
        matching_lines.append(line)

for line in matching_lines:
    line_matches = re.findall(pattern, line, re.MULTILINE)
    for match in line_matches:
        match = float(match)
        integer_part = int(match)  # Convertir en entier
        integer_part_str = str(integer_part)
        expanded_str = ''.join(char * int(char) if char != '0' else char for char in integer_part_str)  # Étaler les chiffres, conserver les zéros
        integer_part_list.append(expanded_str)

result = ''.join(integer_part_list)  # Joindre les parties entières étalées en une seule chaîne
print(result)




