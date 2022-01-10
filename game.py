import telnetlib
import os
import sys
import time
import sysv_ipc
from multiprocessing import Process, Queue
import threading
import socket
import random

#*************************************************GAME************************************************
num_players = 2 #num des joueurs
cartes = {0:'airplane',1:'car',2:'train',3:'bike',4:'shoes'} #dictionnaire des cartes disponibles (associe a chaque carte un numero)
joueurs = []
mqs = []
list_player_processes = []
Bell = False #

keys = [] #pour pouvoir utiliser la message queue une key par joueur 
lock = threading.Lock()
class Player(object): #juste une classe pour 
    def __init__(self, name, number,hand):
        self.name = name
        self.number = number
        self.hand = hand
        
    def __str__(self) -> str:
        return f"Player{self.name} whose number {self.number} whose hand {self.hand}"
    
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

def initialize_game():
    initialize_key(num_players)
    print(keys)
    initialize_mq(num_players)
    i=0
    while not (len(joueurs)==num_players):
        message = ''
        message, t=mqs[i].receive()
        while not message == '':
            name=message.decode()
            print(name)
            message=''
            joueurs.append(Player(name,i,rand_hand()))
            i+=1
            print("hello")
    print('on a fini le while')
    for i in range(num_players):
        print(joueurs[i])
    
    
  
    
def player(num):
    #initialize_game()
    initialize_key(num_players)
    initialize_mq(num_players)
    while not Bell :
        requete = ''
        requete, t=mqs[num].receive()
        while not requete == '':
            requete=requete.decode()
            print(requete,num)
            requete=''
        
        
def clean():
	try:
		for i in range(num_players):
			q = sysv_ipc.MessageQueue(666+i)
			q.remove()
		print("on a vidé les queues") 
	except:
		print("AHA")  
      
		
                
if __name__=="__main__":
    clean()
    initialize_game()
    for i in range(num_players):
        random_hand = rand_hand()

        player_process = Process(target=player,args=(i,))
        list_player_processes.append(player_process)
    print(list_player_processes)
    for player_process in list_player_processes:
        player_process.start()
    # for player_process in list_player_processes:
    #     player_process.join()

