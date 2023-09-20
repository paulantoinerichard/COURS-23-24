import time
'''
async def say(n,what):
  for i in range(n):
    time.sleep(0.1)
    print(what, end=" ", flush=True)

import asyncio

async def main():
  async with asyncio.TaskGroup() as tg:
      task1 = tg.create_task(say(6, '-'))
      task2 = tg.create_task(say(9, '*'))
      print(f"début : {time.strftime('%X')}")
  
  print(f"fin : {time.strftime('%X')}")

asyncio.run(main())

async def main2():
    await asyncio.gather(
      say(6, '-'),
      say(9, '|')
    )

asyncio.run(main2())
'''
#EXERCICE 1
'''
import time,asyncio

async def say(n,what):
  for i in range(n):
    await asyncio.sleep(0.1)
    print(what, end=" ", flush=True)

async def main():
    await asyncio.gather(
      say(6, '-'),
      say(9, '|')
    )

asyncio.run(main())'''


'''import time,asyncio

delay = 1                   # attentes d'1 seconde
starttime = time.time()

def elapsed(i):
  """ renvoie le temps écoulé et l'identifiant de la coroutine """
  return f"elapsed: {time.time()-starttime:.4f}s, id: {i}"

async def tsleep(i):
    """ temporise avec time.sleep """
    print(f"{elapsed(i)}, launch time.sleep()")
    time.sleep(delay)
    print(f"{elapsed(i)}, resume after time.sleep()")

async def main():
    await asyncio.gather(tsleep(1),tsleep(2),tsleep(3))

asyncio.run(main())
'''
import sys, asyncio

#EXERCICE 3
'''
async def C(n,p):
    await asyncio.sleep(0)
    if (p==0 or n==p):
        return 1
    else:
        return await C(n-1,p)+ await C(n-1,p-1)

async def f():
    while True:
        await asyncio.sleep(0)
        for c in "\|/-":
            print(c*4, end="\r"*4,flush=True)

async def g():
    while True:
        await asyncio.sleep(0)
        for i in range(20):
            print("* ",end="",flush=True)
        for i in range(20):
            print("\b\b  \b\b",end="",flush=True)


async def main():
    n = 30
    p = 15
    await asyncio.gather(
        C(n, p),
        #f()
    )

asyncio.run(main())'''

#EXERCICE 4

'''
import subprocess

async def ping(host='example.com', count=1, wait_sec=1):
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

#host = "192.168.1.1"'''
'''
async def main():
    hosts=['192.168.1.', '192.168.2.', '192.168.3.', '192.168.4.', '192.168.5.']
    for host in hosts: 
        for i in range (256):
            #print(i)
            IP = host+ str(i)
            #print(IP)
            result = await ping(IP)
            #print (result)
            if result:
                print(f"{IP} is reachable")

asyncio.run(main())
''' '''
for i in range (0,256):
    host = "192.168.1." + str(i)
    if ping(host):
        print(f"{host} is reachable")
'''
'''
CORRECTION COMID
import asyncio
import sys


async def ping(host="example.com", count=1, wait_sec=1):
    try:
        p = await asyncio.create_subprocess_exec(
            "ping",
            "-c",
            str(count),
            "-W",
            str(wait_sec),
            host,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout_data, _ = await p.communicate()

        output = stdout_data.decode()
        lines = output.split("\n")
        lines = list(filter(lambda x: x != "", lines))
        total = lines[-2].split(",")[3].split()[1]
        loss = lines[-2].split(",")[2].split()[0]
        timing = lines[-1].split()[3].split("/")
        return {
            "type": "rtt",
            "min": timing[0],
            "avg": timing[1],
            "max": timing[2],
            "mdev": timing[3],
            "total": total,
            "loss": loss,
        }
    except Exception:
        return None


async def test_all_addresses(host):
    async def test_address(h):
        res = await ping(h)
        if res:
            return h

    res = await asyncio.gather(
        *[test_address(f"{host}.{i}") for i in range(256)]
    )

    return list(filter(lambda x: x is not None, res))


async def main():
    args = sys.argv
    hosts = args[1:]

    res = await asyncio.gather(*[test_all_addresses(h) for h in hosts])
    return [item for row in res for item in row]

if __name__ == "__main__":
    print(asyncio.run(main()))

v2

#!/bin/env python3
import os,sys,subprocess,re
import asyncio

def usage():
    print(f"usage: {os.path.basename(sys.argv[0])} x.y.z [x.y.z ...]")
    exit(0)

async def ping(host='example.com', count=1, wait_sec=1):
    # print(host, end="\r")
    await asyncio.sleep(0)
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

async def classC_ping(network):
  for i in range(1,255):
    ip  = f"{network}.{i}"
    result = await ping(ip)
    if result:
        print(f"{ip} is reachable")

async def main():
  async with asyncio.TaskGroup() as tg:
    for net in sys.argv[1::]:
      task = tg.create_task(classC_ping(net))

if __name__=="__main__":
    for net in sys.argv[1:]:
        if not re.match(r"\d{,3}\.\d{,3}\.\d{,3}",net):
            usage()

    asyncio.run(main())

'''

#APPLICATION 2 SERVEUR
#squelette serveur
import asyncio

addr = "127.0.0.1"
port = 1234

async def handle(reader, writer):
  data = await reader.read(100) 
  print(f"réception de : {data.decode()}") 

  response = "je suis le serveur et voici ma reponse"
  writer.write(response.encode()) 
  await writer.drain() 
  print(f"envoi de : {response}")

  writer.close()

async def main(addr,port):
  server = await asyncio.start_server(handle,addr,port) 

  async with server:
    await server.serve_forever() 

asyncio.run(main(addr,port))  


#squelette client
#!/bin/env python3
import asyncio

addr = "127.0.0.1"
port = 1234

async def send(message,addr,port):
    reader, writer = await asyncio.open_connection(addr,port)

    print(f'envoi de : {message}')
    writer.write(message.encode()) 

    data = await reader.read(100) 
    print(f'r<C3><A9>ception de : {data.decode()}') 

    writer.close()

async def main(addr,port):
  server = await send("mon message",addr,port) 

asncio.run(main(addr,port))   


#pour voir si le serveur tourne : netstat -ltnp
#kill ****



