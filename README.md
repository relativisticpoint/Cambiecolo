# Cambiecolo 
This is a multi-process multiplayer Python game, it runs on the terminal (no graphic interface).
Cambiecolo is the environmentalist cousin of the Cambio card game. Its goal is presenting a hand of 5
cards of the same transport means. The player who succeeds is awarded the points of the transport they
put together. The game deals as many different types of transports as there are players. Possible transport
means are: airplane, car, train, bike and shoes. Each player receives 5 random cards, face down, e.g. if there
are 3 players, 15 cards of 3 transport means are distributed, 5 cards per transport. A bell is placed in the
middle of the players. As soon as cards are distributed, players start exchanging by announcing the
number of cards they offer, from 1 to 3 identical cards, without showing them. They exchange the same
number of cards with the first player to accept the offer. This continues until one of the players rings the
bell and presents a hand of 5 identical cards, scoring the points of the transport they have grouped.
# How to run the game ?
to run the game you must run the game.py script on a terminal :


    $ python3 game.py

  
for each player open a terminal and run the player.py script :
  

    $ python3 playerX.py

(X refers to the id of the player for example if two players want to play one of them launches player.py on a terminal the other one runs player1.py etc..)
