'''import json
import pandas as pd

with open('stop_areas.json', 'r') as f:
    data=json.load(f)

#from pprint import pprint

#pprint(data)

#pour visualiser les clés principales  data.keys 
#ce qu'on cherche   type(data['stop_areas'])

df = pd.DataFrame(columns=['nomGare','latitude','longitude'])

for gare in data['stop_areas']:
    nom= gare['name']
    lat= gare['coord']['lat']
    long= gare['coord']['lon']
    df = df.append({'nomGare': nom, 'latitude': lat, 'longitude': long}, ignore_index=True)

print(df.head(10))
print(len(df))

df.to_csv("ex1_out.csv", index=False)'''

#EXERCICE 1
"""from random import uniform
from statistics import mean, variance
from functools import reduce

def calcul_moy_var(X):
    moy = reduce(lambda x1,x2:x1+x2 , X)/n
    var = (reduce(lambda x1,x2:x1+ (x2*x2), X))/n - moy**2
    return(moy,var)

n = 1000
X = [uniform(2.5, 10.0) for i in range(n)]



print("Résultats attendus")
print(f"Moyenne : {mean(X):.3f}, Variance : {variance(X)*(n-1)/(n):.3f}")

print("\nRésultats obtenus")
res = calcul_moy_var(X)
print(f"Moyenne : {res[0]:.3f} - Variance : {res[1]:.3f}")
"""

#EXERCICE 2   map.py
'''import sys
import re

def map(text):
    words = re.findall(r'\b\w+\b', text)
    for word in words:
        print(f'{word}')

if __name__ == "__main__":
    input_text = sys.stdin.read()
    map(input_text)


#reduce.py
import sys

def reduce():
    letter_count = 0
    word_count = 0
    line_count = 0
    
    for line in sys.stdin:

        word_count += 1
        letter_count += (len(line)-1)         
        line_count =
    
    print(f'lettres\t{letter_count}')
    print(f'mots\t{word_count}')
    print(f'lignes\t{line_count}')

if __name__ == "__main__":
    reduce()'''


#EXERCICE 3
'''from mrjob.job import MRJob, MRStep
import re

WORD_RE = re.compile(r"[\w]+")

class MRWordFreqCount(MRJob):
    def mapper1(self, _, line):
        for word in WORD_RE.findall(line):
            if len(word)>=5 :
                yield word.lower(), 1

    def combiner1(self, word, counts):
        yield word, sum(counts)

    def reducer1(self, word, counts):
        yield None, (sum(counts),word)

    def reducer2(self, _, compteur): 
        yield max(compteur)

    def steps(self):
        return [
           MRStep(mapper=self.mapper1,
                  combiner=self.combiner1,
                  reducer=self.reducer1),
           MRStep(reducer=self.reducer2)
        ]

if __name__ == '__main__' :
    MRWordFreqCount.run()'''


#EXERCICE 4