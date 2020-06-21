# Write a one-card version of the "WAR" - game in which everyone receives one card and the player with the highest card wins.

# c - club
# d - diamond
# h - heard
# s - spade

# 1 to 7 players with dealer.

import operator
from collections import Counter
from itertools import takewhile

class Card(object):

    RANKS=["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    SUITS=["c", "d", "h", "s"]

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def __str__(self):
        rep = self.rank + self.suit
        return rep
class Hand(object):
    def __init__(self):
        self.cards = []

    def __str__(self):
        if self.cards:
            rep = ""

            for card in self.cards:
                rep += str(card) + "\t"
        else:
            rep = "<empty>"
        return rep

    def clear(self):
        self.cards =[]

    def add(self, card):
        self.cards.append(card)

    def give(self, card, other_hand):
        self.cards.remove(card)
        other_hand.add(card)

class Deck(Hand):
    def populate(self):
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.add(Card(rank, suit))

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def deal(self, hands, per_hand = 1):
        for rounds in range(per_hand):
            for hand in hands:
                if self.cards:
                    top_card = self.cards[0]
                    self.give(top_card, hand)
                else:
                    print("I can't deal the cards. Run out of cards")

class Player(object):
    def __init__(self, name, score = 0):
        self.name = name
        self.score = score

    def __str__(self):
        rep =self.name + ":\t" + str(self.score)
        return rep

def ask_yes_no(question):
    response = None
    while response not in ("y", "n"):
        response = input(question).lower()
    return response

def ask_number(question, low, high):
    response = None
    while response not in range(low, high):
        response = int(input(question))
    return response

class WAR_Value_Card(Card):
    @property
    def value(self):
        if WAR_Value_Card.RANKS.index(self.rank)  == 0:
            return 13
        else:
            return WAR_Value_Card.RANKS.index(self.rank) + 1

class WAR_Deck(Deck):
    def populate(self):
        for suit in WAR_Value_Card.SUITS:
            for rank in WAR_Value_Card.RANKS:
                self.cards.append(WAR_Value_Card(rank, suit))

class WAR_Hand(Hand):
    def __init__(self, name):
        super(WAR_Hand, self).__init__()
        self.name = name
    
    def __str__(self):
        rep = self.name + ":\t" + super(WAR_Hand, self).__str__()
        if self.total:
            rep += "(" + str(self.total) + ")"
        return rep

    @property
    def total(self):
        for card in self.cards:
            if not card.value:
                return None

        total_v = 0
        for card in self.cards:
            total_v += card.value
            return total_v

class WAR_Player(WAR_Hand):

    def lose(self):
        print(self.name, " lose.")

    def win(self):
        print(self.name, " won.")

    def push(self):
        print(self.name, "push.")



class WAR_Game():
    def __init__(self, names):
        self.players = []

        for name in names:
            player = WAR_Player(name)

            self.players.append(player)

        self.dealer = WAR_Player("Dealer")

        self.deck = WAR_Deck()
        self.deck.populate()
        self.deck.shuffle()

    def play(self):

        if len(self.deck.cards) < 52:
            self.deck = WAR_Deck()
            self.deck.populate()
            self.deck.shuffle()



        score = 0
        dictionary_player_value = {}
        self.deck.deal(self.players + [self.dealer])
        for player in self.players:
            print(player)
            score += player.total
            dictionary_player_value.update({player: player.total})
        print(self.dealer)
        score += self.dealer.total
        dictionary_player_value.update({self.dealer: self.dealer.total})

        print(dictionary_player_value)


        player_name_max_value = max(dictionary_player_value.items(), key = operator.itemgetter(1))[0]
        max_value = max(dictionary_player_value.items(), key = operator.itemgetter(1))[1]

        counter = 0
        self.active_players = []
        for i in dictionary_player_value:
            if dictionary_player_value[i] == max_value:
                counter += 1
                self.active_players.append(i)
        for player in self.active_players:
            print("Aktywni: " + str(player))


        if counter == 1:
            print("\n\n\tThe Winner is: " + str(player_name_max_value.name) + ".")
            print("\tMax_value: " + str(max_value))
            print("\tOther players lost! The Winner won: " +str(score) + " points.")


        else:

            helper = False
            while helper == False:
                dictionary_player_value_second = {}


                for player in self.active_players:
                    player.clear()
                    print("Aktywni gracze po wyczyszczeniu kart: " + str(player))

                self.deck.deal(self.active_players)
                for active_players in self.active_players:
                    score += active_players.total
                    dictionary_player_value_second.update({active_players: active_players.total})

                for player in self.active_players:
                    print("Aktywni gracze po rozdaniu ponownie kart: " + str(player))







                player_max_value = max(dictionary_player_value_second.items(), key=operator.itemgetter(1))[0]
                max_value = max(dictionary_player_value_second.items(), key=operator.itemgetter(1))[1]

                # print("\n" + str(player_max_value))
                # print("\n" + str(max_value))

                counter = 0
                for i in dictionary_player_value_second:
                    if dictionary_player_value_second[i] == max_value:
                        counter += 1

                if counter == 1:
                    print("\n\n\tThe Winner is: " + str(player_max_value) + ".")
                    print("\tMax_value: " + str(max_value))
                    print("\tOther players lost! The Winner won: " + str(score) + " points.")
                    helper = True
                else:
                    helper = False















        for player in self.players:
            player.clear()
        self.dealer.clear()





def main():
    print("\t\tWelcome in game: WAR")
    names = []
    score = 0
    number = ask_number("Enter the number of players (1-7): ", low = 1, high = 8)
    for i in range(number):
        name = input("Enter the player's name: ")
        names.append(name)

    game = WAR_Game(names)


    again = None
    while again != "n":
        game.play()
        again = ask_yes_no("\n Do you want to play again?: [y/n]")

main()
input("\n\nTo end the program, press enter.")
