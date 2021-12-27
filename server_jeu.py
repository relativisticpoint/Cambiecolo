# test du serveur : 
import telnetlib
import os
import sys
import time
import sysv_ipc
from multiprocessing import Process, Queue
import threading
import socket
import client
import random
#*******************************************
num_players = 0
switcher = {0:'airplane',1:'car',2:'train',3:'bike',4:'shoes'} #dictionnaire des cartes disponibles (associe a chaque carte un numero)
clients = []
player_processes = []
Bell = False
lock = threading.Lock()
#*******************************************************
class Player(object):
    def __init__(self, addr, sock, number,hand):
        self.sock = sock
        self.name = '<{}> '.format(addr)
        self.number = number
        self.hand = hand
        # self.lock = threading.Lock()
        # self.thread = threading.Thread(target=self.serve)
        # self.thread.start()
    def __str__(self) -> str:
        return f"Player{self.name} whose number {self.number} welcome whose hand {self.hand}"
#*******************************************************
def rand_hand(): #return un deck aleatoire de 5 cartes 
    hand = []
    for i in range(5):
        aleatoire=random.randint(0,4)
        hand.append(switcher[aleatoire])
    # print (hand)
    return hand
#*******************************************************
def player(sock,hand,port):
    lock = threading.Lock()
    sock.bind(('',port)) #initialise la socket sur le port 65432
    sock.listen()

    while True:
        sock,addr = sock.accept()
        i=0
        with lock:
            clients.append(Player(addr,sock,len(clients),hand))#ici on cree l objet Player et on le rajoute a la liste des joueurs 
            print('*'*10,"le numéro",i,clients[i]) #le pb c est que ca nous print le client que sur ce port 
            i+=1
#*******************************************************
def game(num_players):
    #create player processes
    port = 65432
    for i in range(num_players):
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #on initialise le socket en fonction de son type dans ce cas tcp ipv4
        random_hand = rand_hand() #on cree une 'main' aleatoire 
        player_process = Process(target=player,args=(sock,random_hand,port,))#??should the player processes listen on the same port ? NON ref : port already used 
        port+=1
        player_process.start()

if __name__=="__main__":
    game(2)
    #check the Bell 

