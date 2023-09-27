#!/bin/env python3
'''import asyncio

addr = "127.0.0.1" 
port = 1234

async def send(message,addr,port):
    reader, writer = await asyncio.open_connection(addr,port)

    print(f'envoi de : {message}')
    writer.write(message.encode()) 

    data = await reader.read(100) 
    print(f'réception de : {data.decode()}') 

    writer.close()

async def main(addr,port):
    server = await send("où?",addr,port) 
    server = await send("quand?",addr,port) 
    server = await send("comment?",addr,port) 
    server = await send("qui?",addr,port) 
asyncio.run(main(addr,port))   '''

#####################
#######################
####################### TP3


from socket import *

host = "o"  #nom de la machine, on trouve les ip avec host o
port = 2074
buf = 1024                              # taille du buffer
s_addr = (host,port)

UDPsock = socket(AF_INET,SOCK_DGRAM)    # création du socket

while True:
    msg = input('>> ')
    if not msg: break

    data = bytes(msg,'utf-8')
    print(f"Envoi de {data}")
    UDPsock.sendto(data,s_addr)         # envoi vers le serveur

UDPsock.close()




