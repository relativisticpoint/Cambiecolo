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
key = 667 #pour utiliser la message queue

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
        if request == "afficher_offres":
            print("Voici les offres")
            #réception du tableau des offres par mq
            m, _ = mq.receive()
            m = m.decode()
            print(m) #affichage offres
        if request == "cloche":
            print("cloche")
            #envoie de l'action sonner cloche à game par mq
