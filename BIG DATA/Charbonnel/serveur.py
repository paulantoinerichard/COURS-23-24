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

import socket, os

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

asyncio.run(main(addr,port))  
