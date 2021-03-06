# Blackjack
# Od 1 do 7 graczy współzawodniczy z rozdającym

# Ulepsz projekt Blackjack, umożliwiając graczom stawianie pieniędzy. Śledź budżety wszystkich graczy i usuwaj
# każdego gracza, któremu skończą się pieniądze.


class Card(object):
    """Karty do gry"""
    RANKS = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10",
             "J", "Q", "K"]
    SUITS = ["c", "d", "h", "s"]

    def __init__(self, rank, suit, face_up=True):
        self.rank = rank
        self.suit = suit
        self.is_face_up = face_up

    def __str__(self):
        if self.is_face_up:
            rep = self.rank + self.suit
        else:
            rep = "XX"
        return rep

    def flip(self):
        self.is_face_up = not self.is_face_up


class Hand(object):
    """Ręka - wszystkie karty trzymane przez gracza."""

    def __init__(self):
        self.cards = []

    def __str__(self):
        if self.cards:
            rep = ""
            for card in self.cards:
                rep += str(card) + "\t"
        else:
            rep = "<pusta>"
        return rep

    def clear(self):
        self.cards = []

    def add(self, card):
        self.cards.append(card)

    def give(self, card, other_hand):
        self.cards.remove(card)
        other_hand.add(card)


class Deck(Hand):
    """Talia kart."""

    def populate(self):
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                self.add(Card(rank, suit))

    def shuffle(self):
        import random
        random.shuffle(self.cards)

    def deal(self, hands, per_hand=1):
        for rounds in range(per_hand):
            for hand in hands:
                if self.cards:
                    top_card = self.cards[0]
                    self.give(top_card, hand)
                else:
                    print("Nie mogę dalej rozdawać. Zabrakło kart")


class Player(object):
    """Uczestnik gry."""

    def __init__(self, name, score=0):
        self.name = name
        self.score = score

    def __str__(self):
        rep = self.name + ":\t" + str(self.score)
        return rep


def ask_yes_no(question):
    """Zadaj pytanie, na które można odpowiedzieć tak lub nie."""
    response = None
    while response not in ("t", "n"):
        response = input(question).lower()
    return response


def ask_number(question, low, high):
    """Popros o podanie liczby z okreslonego zakresu."""
    response = None
    while response not in range(low, high):
        response = int(input(question))
    return response



class BJ_Card(Card):
    """ Karta do blackjacka. """
    ACE_VALUE = 1

    @property
    def value(self):
        if self.is_face_up:
            v = BJ_Card.RANKS.index(self.rank) + 1
            if v > 10:
                v = 10
        else:
            v = None
        return v


class BJ_Deck(Deck):
    """Talia kart do blackjacka."""

    def populate(self):
        for suit in BJ_Card.SUITS:
            for rank in BJ_Card.RANKS:
                self.cards.append(BJ_Card(rank, suit))


class BJ_Hand(Hand):
    """Ręka w blackjacku"""

    def __init__(self, name):
        super(BJ_Hand, self).__init__()
        self.name = name

    def __str__(self):
        rep = self.name + ":\t" + super(BJ_Hand, self).__str__()
        if self.total:
            rep += "(" + str(self.total) + ")"
        return rep

    @property
    def total(self):
        # jesli karta w ręce ma wartosc None, to i wartosc sumy wynosi None
        for card in self.cards:
            if not card.value:
                return None

        # zsumuj wartosci kart, traktuj każdego asa jako 1
        t = 0
        for card in self.cards:
            t += card.value

        # ustal, czy ręka zawiera asa
        contains_ace = False

        for card in self.cards:
            if card.value == BJ_Card.ACE_VALUE:
                contains_ace = True

        # jesli ręka zawiera asa, a suma jest wystarczajaco niska,
        # potraktuj asa jako 11
        if contains_ace and t <= 11:
            # dodaj tylko 10, ponieważ już dodalismy 1 za asa
            t += 10

        return t

    def is_busted(self):
        return self.total > 21


class BJ_Player(BJ_Hand):
    """Gracz w blackjacku."""

    def is_hitting(self):
        response = ask_yes_no("\n" + self.name + ", chcesz dobrać kartę? (T/N): ")
        return response == "t"

    def bust(self):
        print(self.name, "ma furę.")
        self.lose()

    def lose(self):
        print(self.name, "przegrywa.")

    def win(self):
        print(self.name, "wygrywa.")
        return self.name




    def push(self):
        print(self.name, "remisuje.")
        return self.name


class BJ_Dealer(BJ_Hand):
    """Rozdający w blackjacku."""

    def is_hitting(self):
        return self.total < 17

    def bust(self):
        print(self.name, "ma furę.")

    def flip_first_card(self):
        first_card = self.cards[0]
        first_card.flip()


class BJ_Game(object):
    """Gra w blackjacka."""

    def __init__(self, names):
        self.players = []

        for name in names:
            player = BJ_Player(name)
            self.players.append(player)

        self.dealer = BJ_Dealer("Rozdający")

        self.deck = BJ_Deck()
        self.deck.populate()
        self.deck.shuffle()

    @property
    def still_playing(self):
        sp = []
        for player in self.players:
            if not player.is_busted():
                sp.append(player)
        return sp

    def __additional_cards(self, player):
        while not player.is_busted() and player.is_hitting():
            self.deck.deal([player])
            print(player)
            if player.is_busted():
                player.bust()

    def play(self):

        # rozdaj każdemu początkowe dwie karty
        self.deck.deal(self.players + [self.dealer], per_hand=2)
        self.dealer.flip_first_card()  # ukryj pierwszą kartę rozdającego
        for player in self.players:
            print(player)
        print(self.dealer)

        # rozdaj graczom dodatkowe karty
        for player in self.players:
            self.__additional_cards(player)

        self.dealer.flip_first_card()  # odsłoń pierwszą kartę rozdającego

        if not self.still_playing:
            # ponieważ wszyscy gracze dostali furę, pokaż tylko rękę rozdającego
            print(self.dealer)
        else:
            # daj dodatkowe karty rozdającemu
            print(self.dealer)
            self.__additional_cards(self.dealer)



        # poszukiwanie najlepszego wyniku
        max_value = 0

        if self.dealer.total > max_value and self.dealer.total < 22:
            max_value = self.dealer.total

        for player in self.still_playing:
            if player.total > max_value and player.total < 22:
                max_value = player.total


        counter = 0
        if self.dealer.total == max_value:
            counter += 1
        for player in self.still_playing:
            if player.total == max_value:
                counter += 1

        print("Chcę znać counter " + str(counter))

        if self.dealer.total == max_value and counter == 1:
            print("Dealer wygrywa.")

        winners = []

        for player in self.still_playing:
            if player.total == max_value and counter == 1:
                winner_name = player.win()
                winners.append(winner_name)

            elif player.total < max_value:
                player.lose()
            else:
                draw_player = player.push()
                winners.append(draw_player)


        # usuń karty wszystkich graczy
        for player in self.players:
            player.clear()
        self.dealer.clear()




        return counter, winners





def main():
    print("\t\tWitaj w grze 'Blackjack'!\n")

    names = []
    banks = {}
    while True:
        try:
            number = ask_number("POdaj liczbę graczy (1 - 7): ", low = 1, high = 8)
            break
        except ValueError:
            print("Podaj liczbę od 1 do 7!")

    for i in range(number):
        name = input("Wprowadź nazwę gracza: ")
        while True:
            try:
                bank = int(input("Podaj ile gracz wpłaca pieniędzy: "))
                break
            except ValueError:
                print("Podaj liczbę!")

        banks.update({name: bank})
        names.append(name)
    print(banks)








    helper = False
    again = None
    remove_names = []
    pot = 0
    while again != "n":
        while True:
            try:
                stake =int(input("Wprowadź stawkę gry: "))
                break
            except ValueError:
                print("Wprowadź liczbę!!")

        for name in banks:
            while banks[name] < stake:
                print(str(name) + " masz za mało pieniędzy.")



                question = None
                while question != "n":
                    question = ask_yes_no("\n" + str(name) + " chcesz dopłacić? [t/n] ")
                    print(question)
                    if str(question) == "t" or str(question) == "T":
                        while True:
                            try:
                                payment = int(input("Podaj ile gracz wpłaca pieniędzy: "))
                                break
                            except ValueError:
                                print("Podaj liczbę!!")

                        banks[name] += payment
                        print(banks[name])

                    if question == "n" and banks[name] < stake:
                        print("Ochrona pokaże Ci gdzie są drzwi.\n")
                        remove_names.append(name)
                        helper = True

                if helper == True:
                    break

        if helper == True:
            for name in remove_names:
                banks.pop(name)

        for name in banks:
            banks[name] -= stake
            pot += stake
        #stake od rozdającego
        pot += stake

        print("Śledzenie aktualnych stanów kont: ")
        for name in banks:
            print(str(name) + ": " + str(banks[name]))
        print("Pot: " + str(pot))

        #usuwanie gracza z listy który ma za mało pieniędzy
        for name in remove_names:
            names.remove(name)
        remove_names = []

        game = BJ_Game(names)







        counter, winners = game.play()


        for name in banks:
            for position in winners:
                if name == position:
                    banks[name] += (pot / counter)
                    banks[name] = int(banks[name])



        pot = 0
        again = ask_yes_no("\nCzy chcesz zagrać ponownie?: ")
        if again == "n":
            print("Wypłacone zostanie: ")
            for name in banks:
                print(str(name) + ": " + str(banks[name]))




main()

input("\n\nAby zakończyć program, nacisnij klawisz Enter.")
