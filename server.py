# Original code from CMU 15-112 Sockets Manuel by by Rohan Varma adapted by Kyle Chin
# Some changes have been made to the code
import socket
import threading
from queue import Queue

HOST = "127.0.0.1" #Enter IP address
PORT = 50001
BACKLOG = 2

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST,PORT))
server.listen(BACKLOG)
print("looking for connection")

#   Listening to clients to receice messages
def handleClient(client,serverChannel,cID,clientele):
    client.setblocking(1)
    msg = ""
    while True:
        try:
            msg += client.recv(10).decode("UTF-8")
            print(msg)
            command = msg.split("\n")
            print("command", command)
            while (len(command) > 1):
                readyMsg = command[0]
                msg = "\n".join(command[1:])
                serverChannel.put(str(cID) + " " + readyMsg)
                command = msg.split("\n")
        except:
            # we failed
            return
        

def serverThread(clientele,serverChannel):
    while True:
        msg = serverChannel.get(True,None)
        msgList = msg.split(" ")
        senderID = msgList[0]
        details = " ".join(msgList[1:])
        for cID in clientele:
            if cID != senderID:
                print(cID,senderID)
                sendMsg = details + "\n"
                clientele[cID].send(sendMsg.encode())
                print("> sent to %s:" % cID, sendMsg[:-1])
        print()
        serverChannel.task_done()
        
clientele = dict()
playerNum = 0

serverChannel = Queue(100)
threading.Thread(target = serverThread, args = (clientele, serverChannel)).start()

while True:
    client,address = server.accept()
    myID = str(playerNum)
    for cID in clientele:
        clientele[cID].send(("newPlayer %s\n" % myID).encode())
        client.send(("newPlayer %s\n" % cID).encode())
    clientele[myID] = client
    client.send(("myIDis %s \n" % myID).encode())
    print("connection recieved from %s" % myID)
    threading.Thread(target = handleClient, args = 
                            (client ,serverChannel, myID, clientele)).start()
    playerNum += 1

            
            