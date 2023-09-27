from collections.abc import Callable, Iterable, Mapping
import time, threading
from typing import Any

'''class MyThread(threading.Thread):
    def __init__(self, m, s, n):
        threading.Thread.__init__(self)
        self.m=m
        self.n=n
        self.s=s

    def run(self):
        for i in range(self.n):
            print(self.m)
            time.sleep(self.s)

mytask = MyThread('aaaaa',2,25)
mytask2 = MyThread('bbbbb',2,10)
mytask.start()
mytask2.start()
'''
######################EXERCICE mt.2

'''class MyThread(threading.Thread):
    def __init__(self, chiffre):
        threading.Thread.__init__(self)
        self.c=chiffre

    def run(self):
        print(self.c)

for i in range(100):
    mytask = MyThread(i)
    mytask.start()
    time.sleep(0.1)
'''

'''class Add(threading.Thread):
  mon_verrou = threading.Lock()
  s = 0
  def __init__(self,i):
    threading.Thread.__init__(self)
    self.i = i

  def run(self):
    Add.mon_verrou.acquire()
    x = Add.s
    time.sleep(0.001)
    x += self.i
    time.sleep(0.001)
    Add.s = x
    Add.mon_verrou.release()

if __name__=="__main__":
  tasks = []

  for i in range(1,101):
    tasks.append(Add(i))

  for t in tasks:
    t.start()

  for t in tasks:
    t.join()

  print(f"s={Add.s}")
'''

################## EXERCICE mt.3

'''import threading,sys

class Serie(threading.Thread):
  results = {}

  def __init__(self,i,k):
    threading.Thread.__init__(self)
    self.k = k
    self.i = i

  def run(self):
    s = 0
    s2 = -1
    i = self.i
    while s!=s2:
      s2 = s
      s += 1./(i*i)
      # if i%10000==0: print(f"{self.i:2d} : {s} ", end="\n", flush=True)
      i += self.k
    Serie.results[self.i] = s

nbtache = int(sys.argv[1])

taches = []
for i in range(1,nbtache+1):
    taches.append(Serie(i,nbtache))

for t in taches:
    t.start()

for t in taches:
    t.join()

s = 0
for r in Serie.results:
    s += Serie.results[r]

print(s)'''


########## EXERCICE mt.4


'''import threading,subprocess

class C(threading.Thread):
  def __init__(self,ip):
    threading.Thread.__init__(self)
    self.ip = ip

  def ping(self, host, count=1, wait_sec=1):
    cmd = f"ping -c {count} -W {wait_sec} {host}".split(' ')
    try:
      output = subprocess.check_output(cmd).decode().strip()
      lines = output.split("\n")
      total = lines[-2].split(',')[3].split()[1]
      loss = lines[-2].split(',')[2].split()[0]
      timing = lines[-1].split()[3].split('/')
      return {
        'type': 'rtt',
        'min': timing[0],
        'avg': timing[1],
        'max': timing[2],
        'mdev': timing[3],
        'total': total,
        'loss': loss,
      }
    except subprocess.CalledProcessError :
      return None
    except Exception as e:
      print(type(e),e)
      return None

  def run(self):
    if self.ping(self.ip):
      print(f"{self.ip} is reachable")

net = "172.20.45."
tasks = []

for i in range(1, 255):
tasks.append(C(f"{net}{i}"))

for t in tasks:
t.start()

for t in tasks:
t.join()
'''
  








