import multiprocessing
import random
class Player:
    def __init__(self,id,hand) :
        self.id = id
        self.hand = hand 
    def __str__(self) -> str:
        return f"the hand of the player {self.id} is {self.hand} "

def rand_hand():
    hand = []
    switcher = {1:'airplane',2:'car',3:'train',4:'bike',5:'shoes'}
    for i in range(5):
        aleatoire=random.randint(1,5)
        hand.append(switcher[aleatoire])
    print (hand)
    return hand




def Game():
    def init_game(num_players):

        for i in range(num_players):
            # p[i] = Process(target=Player, args=(i, rand_hand))
            break






if __name__ == "__main__":
    hand = ['airplane','car','train','bike','shoes']
    arm = Player(5000,rand_hand())
    print(arm)

