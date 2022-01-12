import telnetlib
import os
import sys
import time
import sysv_ipc
from multiprocessing import Process, Queue, shared_memory
import threading
import socket
import random


#*************************************************GAME************************************************
num_players = 2 #num des joueurs
cartes = {0:'plane',1:'car',2:'train',3:'bike',4:'shoes'} #dictionnaire des cartes disponibles (associe a chaque carte un numero)
joueurs = []
mqs = []
list_player_processes = []
offers = shared_memory.ShareableList([""*32,""*32,""*32,""*32,""*32])
Bell = False #

keys = [] #pour pouvoir utiliser la message queue une key par joueur 
lock = threading.Lock()
class Player(object): #juste une classe pour 
    def __init__(self, name, number,hand):
        self.name = name
        self.number = number
        self.hand = hand
        
    def __str__(self) -> str:
        return f"Player {self.name} whose number {self.number} whose hand {self.hand}"
    
def rand_hand(): #return un deck aleatoire de 5 cartes 
    hand = []
    for i in range(5):
        aleatoire=random.randint(0,4)
        hand.append(cartes[aleatoire])
    # print (hand)
    return hand
  
def initialize_key(num_players):
  for i in range(num_players):
    new_key=666+i
    keys.append(new_key)
def initialize_mq(num_players):
    for i in range(num_players):
        mq = sysv_ipc.MessageQueue(keys[i], sysv_ipc.IPC_CREAT) 
        mqs.append(mq)

def initialize_game(joueurs):
    initialize_key(num_players)
    print(keys)
    initialize_mq(num_players)
    i=0
    while not (len(joueurs)==num_players):
        message = ''
        message, t=mqs[i].receive()
        while not message == '':
            name=message.decode()
            message=''
            joueurs.append(Player(name,i,rand_hand()))
            print(name," has joined the game as player",i)
            i+=1
    print("All the players are here")
    for i in range(num_players):
        print(joueurs[i])
    

def haveCard(offre, num,joueurs):
    isValid = False
    cardName = offre[1:]
    for card in joueurs[num].hand:
        if cardName == card:
            isValid = True
    return isValid

def haveGoodNumber(offre, num,joueurs):
    isValid = False
    print("offre:",offre)
    cardNumber = int(float(offre[0]))
    cardName = offre[1:]
    counter = 0
    for card in joueurs[num].hand:
        if cardName == card:
            counter += 1
    print("counter: ",counter,"et cardNumber: ",cardNumber)
    if cardNumber <= counter:
        isValid = True
    return isValid
        
def isOfferValid(offre, num,joueurs):
    isValid = False
    print("offre:",offre," du joueur: ",num)
    if haveCard(offre, num,joueurs):
        print("haveCard")
    if haveGoodNumber(offre, num,joueurs):
        print("haveGoodNumber")
        isValid = True
    		
    return isValid

def player(num,joueurs):
    #initialize_game()
    global offers
    initialize_key(num_players)
    initialize_mq(num_players)
    # print("la liste des joueurs mais dans la methode player",joueurs)
    while not Bell :
        requete = ''
        requete, t=mqs[num].receive()
        print(requete)
        requete=requete.decode()
        if not requete == '' and not requete == "askOffer" and not requete == "badInput" and not requete[0]=="S" and not requete[0]=="e" and not requete[0]=="a":
            if isOfferValid(requete,num,joueurs):
                print("Player ",num," :",requete)
                offers[num] = str(requete)
                ack = "ack:Offre valide"
                message = str(ack).encode()
                mqs[num].send(message)
            else:
                errorMessage = "error:Offre non valide"
                message = str(errorMessage).encode()
                mqs[num].send(message)
            requete=''
        if requete == "askOffer":
            print(offers)
            print(requete)
            message = str(offers).encode()
            mqs[num].send(message)
            requete=""
        if requete == "badInput":
            errorMessage = "error:bad input"
            message = str(errorMessage).encode()
            mqs[num].send(message)

			

        
        
def clean():
	try:
		for i in range(num_players):
			q = sysv_ipc.MessageQueue(666+i)
			q.remove()
		print("clean all the queues successfully") 
	except:
		print("Memory is already clean.")  
      
		
                
if __name__=="__main__":
    clean()
    initialize_game(joueurs)
    for i in range(num_players):
        random_hand = rand_hand()

        player_process = Process(target=player,args=(i,joueurs,))
        list_player_processes.append(player_process)
    print(list_player_processes)
    for player_process in list_player_processes:
        player_process.start()
    # for player_process in list_player_processes:
    #     player_process.join()

