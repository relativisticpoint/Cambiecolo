import multiprocessing
import telnetlib
import os
import sys
import time
import sysv_ipc
from multiprocessing import Process, Queue, shared_memory
import threading
import socket
import random

joueurs2 = []
num=0

class Player(object): #juste une classe pour 
    def __init__(self, name, number,hand):
        self.name = name
        self.number = number
        self.hand = hand
        
    def __str__(self) -> str:
        return f"Player {self.name} whose number {self.number} whose hand {self.hand}"

def worker(joueurs2):
    hani = Player('hani',0,[0,0])
    joueurs2.append(hani)


if __name__=="__main__":
    player_process = multiprocessing.Process(target=worker,args=(joueurs2,))
    player_process.start()
    player_process.join()
    print("la liste est ",joueurs2)
    joueurs2[0].hand.append(2345)
    print("la liste est ",joueurs2[0])
