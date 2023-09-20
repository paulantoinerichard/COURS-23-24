#!/bin/env python3
import asyncio

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
asyncio.run(main(addr,port))   