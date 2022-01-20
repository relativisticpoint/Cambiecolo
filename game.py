import telnetlib
import os
import sys
import time
import sysv_ipc
from multiprocessing import Process, Queue, shared_memory
import threading
import socket
import random
import signal


#*************************************************GAME************************************************
num_players = 3 #num des joueurs
cartes = {0:'plane',1:'car',2:'train',3:'bike',4:'shoes'} #dictionnaire des cartes disponibles (associe a chaque carte un numero)
joueurs = [] #tableau de joueurs
mqs = [] #tableau qui contient les message queues 
list_player_processes = []
offers = shared_memory.ShareableList([""*32,""*32,""*32,""*32,""*32]) #variable ou seront stockees les offres au fur et a mesure du jeu, chaque case correspond a un joueur
Bell = False #boolean qui indique l'etat de la cloche
handP1 = shared_memory.ShareableList(["","","","",""])#la main de chaque player est stockee ici
handP2 = shared_memory.ShareableList(["","","","",""])
handP3 = shared_memory.ShareableList(["","","","",""])
handP4 = shared_memory.ShareableList(["","","","",""])
handP5 = shared_memory.ShareableList(["","","","",""])
all_hands= [handP1,handP2,handP3,handP4,handP5]#liste regroupant la main de chaque joueur 
list_pid = []

lock = shared_memory.ShareableList(["lose"])
winner = shared_memory.ShareableList([""])

keys = [] #pour pouvoir utiliser la message queue une key par joueur 


class Player(object): #juste une classe Player pour rassembler les informations de tous les players
    def __init__(self, name, number,hand):
        self.name = name
        self.number = number
        self.hand = hand
        
    def __str__(self) -> str:
        return f"Player {self.name} has number {self.number} has hand {self.hand}"
    

#Methode qui permet la distribution des cartes en respectant les règles du jeu
def create_hands(num_players):
    list_rand = [] #liste qui contiendra les 
    check=0
    aleatoire = 0
    for i in range(num_players):
        check = aleatoire
        #on tire aleatoirement un nombre entre 0 et 4 et on veut eviter de tirer deux fois de suite le meme
        while check==aleatoire:
            aleatoire=random.randint(0,4)
        for j in range(5):
            list_rand.append(cartes[aleatoire])
    for i in range(num_players):
        #on shuffle la liste 
        random.shuffle(list_rand)
    k=0
    for i in range(num_players):
        for j in range(5):
            all_hands[i][j] = list_rand[k] #remplir la hand de chaque joueur par des cartes identiques 
            k+=1


#Methode qui cree une key par joueur qui permettra plus tard de lui attribuer une message queue qui lui servira de canal avec game
def initialize_key(num_players):
  for i in range(num_players):
    new_key=666+i
    keys.append(new_key)


#Methode qui permet de creer et de stocker les message queues dans une liste 'mqs' 
def initialize_mq(num_players):
    for i in range(num_players):
        mq = sysv_ipc.MessageQueue(keys[i], sysv_ipc.IPC_CREAT) 
        mqs.append(mq)


#Methode qui permet de initialiser le jeu
def initialize_game(joueurs):
    initialize_key(num_players)
    print(keys)
    initialize_mq(num_players)
    create_hands(num_players)
    i=0
    while not (len(joueurs)==num_players):
        message = ''
        message, t=mqs[i].receive()
        while not message == '':
            receive=message.decode()
            name = receive[4:]
            pid = receive[:4]
            pid = int(pid)
            list_pid.append(pid)
            message=''
            joueurs.append(Player(name,i,all_hands[i]))
            print(name," has joined the game as player",i)
            i+=1
    print("All the players are here")
    for i in range(num_players):
        print(joueurs[i])
    

#methode qui ne renvoie true que si le joueur a la carte qu'il se propose d'echanger
def haveCard(offre, num,joueurs):
    isValid = False
    cardName = offre[1:]
    for card in joueurs[num].hand:
        if cardName == card:
            isValid = True
    return isValid


#méthode qui vérifie que les joueurs qui échangent ont bien le même nombre de cartes à échanger
def haveGoodNumber(offre, num,joueurs):
    isValid = False
    cardNumber = int(float(offre[0]))
    cardName = offre[1:]
    counter = 0
    for card in joueurs[num].hand:
        if cardName == card:
            counter += 1
    if cardNumber <= counter:
        isValid = True
    return isValid
        

#methode qui permet de verifier si une offre est valide cad si le joueur qui propose l offre a reelement ces cartes et le bon nombre  
def isOfferValid(offre, num,joueurs):
    isValid = False
    #print("offre:",offre," du joueur: ",num)
    if haveCard(offre, num,joueurs):
    #print("haveCard")
        if haveGoodNumber(offre, num,joueurs):
        #print("haveGoodNumber")
            isValid = True
    return isValid
    
    
#méthode qui vérifie si l'échange est valide (bon nombre de cartes)
def isExchangeValid(numeroEchange, carteEchange):
    isValid = False
    #have same number of card
    if int(carteEchange[0]) == int(offers[int(numeroEchange)][0]):
        isValid = True
        #print("Bon nombre de cartes")
    return isValid
            

#Methode qui permet d'assurer l'echange entre deux joueurs
def do_exchange(numPlayer1, offer1, numPlayer2, offer2):

    for cardIndex1 in range(len(joueurs[numPlayer1].hand)):
        if joueurs[numPlayer1].hand[cardIndex1] == offer1[1:]:
            cardIndex2 = 0
            while not joueurs[int(numPlayer2)].hand[int(cardIndex2)] == offer2[1:]:
                cardIndex2 += 1
            tmp = joueurs[int(numPlayer1)].hand[int(cardIndex1)]
            joueurs[int(numPlayer1)].hand[int(cardIndex1)] = joueurs[int(numPlayer2)].hand[int(cardIndex2)]
            joueurs[int(numPlayer2)].hand[int(cardIndex2)] = tmp

    offers[int(numPlayer2)] = ""*32
                    
    
#méthode qui permet de masquer le nom des cartes lors de l'affichage des offres par les joueurs. Ainsi le joueurs ont seulement connaissance du nombre de carte à échanger.
def maskedOffer(offers):
    tabMaskedOffer = []
    for i in range(len(offers)):
        tmp = str(offers[i])
        if tmp == "":
            tabMaskedOffer.append("")
        else:
            tabMaskedOffer.append(tmp[0])
    return tabMaskedOffer
    
    
# methode qui calcule le nombre max de cartes identiques qu'un joueur a
def countCardInHand(numPlayer):
    maxIdenticalCards = 0
    for i in range(len(cartes)):
        counter = 0
        for j in range(len(joueurs[int(numPlayer)].hand)):
            if cartes[i] == joueurs[int(numPlayer)].hand[j]:
                counter +=1
        if maxIdenticalCards < counter :
            maxIdenticalCards = counter
    return maxIdenticalCards


#methode qui verifie si un joueur a 5 cartes identiques, elle est appelee quand un joueur fait sonner la cloche  
def isFullHand(numPlayer):
    isValid = False
    if countCardInHand(numPlayer) == 5:
        isValid = True
    return isValid
        
              
#Methode centrale monstrueuse qui sera lancee dans des process séparés
def player(num,joueurs):
    global offers


    while lock[0] == "lose" :
        requete = ''
        requete, t=mqs[num].receive()
        print(requete)
        requete=requete.decode()
        
        if requete[:5] == "offre":
            requete = requete[5:]
            if isOfferValid(requete,num,joueurs):
                #si l'offre est valide on la print dans game
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
            message = str(maskedOffer(offers)).encode()
            mqs[num].send(message)
            requete=""
        if requete == "askHand": #si le player demande a voir sa main on lui envoie
            message = str(all_hands[num]).encode()
            mqs[num].send(message)
            requete=""
        if requete == "badInput":
            errorMessage = "error:bad input"
            message = str(errorMessage).encode()
            mqs[num].send(message)
        if requete[:7] == "echange": 
            numeroEchange = requete[7:8]
            carteEchange = requete[8:]
            print("log: numEchange ",numeroEchange," et carte: ",carteEchange)
            if isOfferValid(carteEchange,num,joueurs) and isExchangeValid(numeroEchange, carteEchange):
                print("log: Exchange is valid")
                do_exchange(num, carteEchange, numeroEchange, offers[int(numeroEchange)]) #si toutes les conditions pour faire l echange sont satisfaites on lance do_exchange
                print("Exchange done")
                
                ack = "ack:Echange reussi"
                message = str(ack).encode()
                mqs[num].send(message)
                
                for i in range(num_players):
                    print(joueurs[i])
            else:
                errorMessage = "error:Offre non valide"
                message = str(errorMessage).encode()
                mqs[num].send(message)
            requete=''
        if requete == "cloche":
            if lock[0][:3] == "win":
                message = str("END").encode()
                mqs[num].send(message)
                message = str("END").encode()
                mqs[num].send(message)
            if isFullHand(num) and lock[0] == "lose":
                ack = "ack:Le gagnant est "
                #print("valeur du lock: ",lock[0])
                lock[0] = "win"+str(num)
                #print("valeur du lock après : ",lock[0])
                winnerName = str(joueurs[num].name)
                winner[0] = winnerName
                message = str(ack+winnerName).encode()
                mqs[num].send(message)


            else:
                errorMessage = "error:you don't have five identical cards or a player has already won: "
                numberOfIdenticalCard = str(countCardInHand(num))
                message = str(errorMessage+numberOfIdenticalCard).encode()
                mqs[num].send(message)
            requete = ""
			
                  
#methode qui permet de 'clean' la memoire des message queues qui pourraient exister d'une ancienne partie 
def clean():
	try:
		for i in range(num_players):
			q = sysv_ipc.MessageQueue(666+i)
			q.remove()
		print("cleaned all the queues successfully") 
	except:
		print("Memory is already clean.")  
      
		

if __name__=="__main__":
    clean()
    initialize_game(joueurs)
    for i in range(num_players):
        player_process = Process(target=player,args=(i,joueurs,)) #on lance autant de process qu'il y a de joueurs
        list_player_processes.append(player_process)
    print(list_player_processes)
    for player_process in list_player_processes:
        player_process.start()
    for player_process in list_player_processes:
        player_process.join()
        
    for pid in list_pid:
        os.kill(pid, signal.SIGKILL)
    print("Game is over! The winner is", winner[0])

