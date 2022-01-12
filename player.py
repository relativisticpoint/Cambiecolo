import telnetlib
import os
import sys
import time
import sysv_ipc
from multiprocessing import Process, Queue
import threading
import socket
import random

#*************************************************Joueurn************************************************
key = 666 #pour utiliser la message queue

class Player(object): #juste une classe pour 
    def __init__(self, name, number,hand):
        self.name = name
        self.number = number
        self.hand = hand
    
    
if __name__=="__main__":
    print("bienvenue dans le jeu")
    name=input("Entrez votre nom: ")
    try:
        mq = sysv_ipc.MessageQueue(key)
    except ExistentialError:
        print("Cannot connect to message queue", key, ", terminating.")
        sys.exit(1)
    #send le nom 
    message = str(name).encode()
    mq.send(message)
    while True:
        request = input("Que voulez vous faire ? ")
        if request == "faire_offre":
            offre = input("Quelle est votre offre ? ")
            
            print("Votre offre est: ", offre)
            #envoie de l'offre par mq
            message = str(offre).encode()
            mq.send(message)
            
        elif request == "afficher_offres":
            ask = "askOffer"
            message = str(ask).encode()
            mq.send(message)
            
            print("Voici les offres ")
            #réception du tableau des offres par mq
            #m, _ = mq.receive()
            #m = m.decode()
            #print(m) #affichage offres
        elif request == "cloche":
            print("cloche")
            #envoie de l'action sonner cloche à game par mq
        else :
            badInp = "badInput"
            message = str(badInp).encode()
            mq.send(message)
           
        #réception des messages d'erreurs et d'acquittement
        received, _ = mq.receive()
        if not received == "":
            received = received.decode()
            print(received)
            #if received[:5] == "error" or received[:3] == "ack":
            #   print(received)
        
        
        
        
        
        
        
        
