#!/bin/env python3

import asyncio

############## QUESTION 2
"""
import asyncio

addr = "0.0.0.0" #pour la réception
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

asyncio.run(main(addr,port))  """

############## QUESTION 3

'''import socket, os

addr = "127.0.0.1"
port = 1234

async def handle(reader, writer):
    data = await reader.read(100) 
    print(f"réception de : {data.decode()}") 

    if data.decode() == "où?":
        response = socket.getfqdn
    elif data.decode() == "qui?":
        response = os.getlogin
    elif data.decode() == "quand?":
        response = "pas encore fait"
    elif data.decode() == "comment?":
        response = "pas encore fait"
    else:
        print('pas compris !')
    writer.write(response.encode()) 
    await writer.drain() 
    print(f"envoi de : {response}")

    writer.close()

async def main(addr,port):
    server = await asyncio.start_server(handle,addr,port) 

    async with server:
        await server.serve_forever() 

asyncio.run(main(addr,port))  '''

#####################
#######################
####################### TP3
# pour kill un serveur : netstat -lntup puis kill -9 *****
from socket import *
import re, time

host = "0.0.0.0"  #sinon localhost pr moi
port = 2074
buf = 1024                            # taille du buffer
s_addr = (host,port)

UDPsock = socket(AF_INET,SOCK_DGRAM)  # création du socket
UDPsock.bind(s_addr)                  # activation

while True:
    data,c_addr = UDPsock.recvfrom(buf)  # écoute
    print(f"\nReçu {data} de {c_addr}")
    pattern = r'(\d+) "([^"]+)" "([^"]+)"'
    if data:
        resultats = re.search(pattern, data.decode('utf-8'))
        if resultats:
            print(f"\n{resultats.group(2)} de {c_addr}")
            time.sleep(int(resultats.group(1)))
            print(f"\n{resultats.group(3)} de {c_addr}")
        else:
            print(f"\nrequête incompréhensible de {c_addr}")
    else:
        print(f"\nrequête incompréhensible de {c_addr}")        

UDPsock.close()


#####Q4
'''
from socket import socket, AF_INET, SOCK_DGRAM
import re
import time
import threading


def receive_msg(data, c_addr):
    regex = re.compile(r"(\d+)\s([A-Za-z0-9]+)\s([A-Za-z0-9]+)")
    
    if re.fullmatch(regex, data.decode()):
        groups = re.search(regex, data.decode())
        print(f"\n{groups.group(2)} envoyé par {c_addr}")
        
        t = int(groups.group(1))
        time.sleep(t)
        
        print(f"\n{groups.group(3)} envoyé par {c_addr} il y  a {t} secondes")
    else:
        print(f"requête incompréhensible de {c_addr}")


if __name__ == "__main__":
    host = "0.0.0.0"
    port = 2074
    buf = 1024  # taille du buffer
    s_addr = (host, port)

    UDPsock = socket(AF_INET, SOCK_DGRAM)  # création du socket
    UDPsock.bind(s_addr)  # activation
    try:
        while True:
            data, c_addr = UDPsock.recvfrom(buf)  # écoute
            if len(data) > 0:
                t = threading.Thread(target=receive_msg, args=(data, c_addr))
                t.start()
    except KeyboardInterrupt:
        print("Interruption du serveur")
    finally:
        UDPsock.close()'''