##EXERCICE ge1
#ouvrir la console; taper 'python'
#python s'ouvre; taper def fibo(): ....
#next(suite)
'''
def fibo():
    x = 0
    y = 1
    yield x
    yield y
    while True:
        x,y = y, x+y
        yield y
        
suite = fibo()
next(suite)
#for _ in range(10):
#    print( next(suite) )


##EXERCICE ge2
import time 

def chrono():
    t0=time.time()
    while True:
        T=time.time()-t0
        yield T

mon_chrono = chrono()
next(mon_chrono)         # déclenche le chrono
time.sleep(5)
print(next(mon_chrono))  # affiche le temps écoulé depuis le déclenchement
time.sleep(2)
print(next(mon_chrono))  # affiche le temps écoulé depuis le déclenchement

##EXERCICE ge3


def palindrome(n):
    path = "/usr/share/dict/words"
    with open(path,'r') as file:
        ligne= file.readline()
        while ligne:
            ligne=ligne.strip()
            if ligne== ligne[::-1] and len(ligne)==n:
                yield ligne
            ligne= file.readline()


pal=palindrome(5)
next(pal)
'''

##EXERCICE ge4

def termes(n):
    liste=[]
    for _ in range(n):
        liste.append(1)


termes(4)

'''def termes(n,l):
  for i in range(1,n):
    l2 = l + [i]
    if sum(l2)==n:
      print(l2)
      return
    elif sum(l2)<n:
      termes(n,l2)
    else:
      return 
if __name__=="__main__":
  l = []
  termes(5,l)

