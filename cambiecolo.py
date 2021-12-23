import multiprocessing
import random
global switcher 
switcher = {0:'airplane',1:'car',2:'train',3:'bike',4:'shoes'}
class Player:
    def __init__(self,id,hand) :
        self.id = id
        self.hand = hand 
    def __str__(self) -> str:
        return f"the hand of the player {self.id} is {self.hand} "
def rand_hand():
    hand = []
    for i in range(5):
        aleatoire=random.randint(0,4)
        hand.append(switcher[aleatoire])
    print (hand)
    return hand
def init_game(num_players):
    p=[]
    for i in range(num_players):
        # p[i] = Process(target=Player, args=(i, rand_hand))
        break





def Game(num_players=2):
    init_game(num_players)







if __name__ == "__main__":
    hand = ['airplane','car','train','bike','shoes']
    armand = Player(5000,rand_hand())
    print(armand)

