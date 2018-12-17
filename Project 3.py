#Project 3
#Main Program

#randomization module for shuffling deck
import random

#function gathers user information with validation
#initializes game parameters
#controls game loop
#calls game-related functions
def main():
    name = input("Name? ")
    while name.isalpha() == False:
        name = input("Name? ")

    bank = 1000
    playing = True
    first_round = True

    while playing:
        #quits game if bank is empty
        if bank == 0:
            print("Sorry, you're out of money!")
            break

        #create and reorder Deck object
        deck = Deck()
        deck.shuffle()

        #create and load attributes for dealer Player object
        dealer_hand = []
        dealer_hand.append(deck.draw())
        dealer = Player(dealer_hand)

        #create and load attributes for user Player object
        hand = []
        for card in range(2):
                hand.append(deck.draw())
        user = Player(hand, bank)

        #display current bank amount
        print("\n{} has ${:,}".format(name, bank))

        #first round bet is $25 and $100 after that
        wager = 100
        if first_round == True:
            wager = 25

        #input validation for bet input
        bet = input("Bet? (0 to quit, Enter to stay at ${}) ".format(wager))
        if bet == "0":
            break
        elif bet == "":
            bet = wager
            first_round = False
        else:
            continue

        #call function to display current bet, hands, and values
        game_status(bet, dealer, name, user)

        #run game sequence
        #return bank amount for next round depending on outcome
        bank = game(bank, deck, user, bet, dealer, name)

#function formats and displays current stats
def game_status(bet, dealer, name, user):
    print("\nBet: ${}".format(bet))
    print("Dealer's Hand: ", end=' ')
    dealer.get_hand()
    print("\nValue: ", end=' ')
    print(dealer.get_value())
    print("{}'s Hand: ".format(name), end=' ')
    user.get_hand()
    print("\nValue: ", end=' ')
    print(user.get_value())

#function prompts user to move
#calls game status function to update display
#controls dealer Player object behavior
#determines win and loss conditions
#returns bank amount
def game(bank, deck, user, bet, dealer, name):
    move = input("\nMove? (hit/stay) ")
    while move.lower() not in ['h', 's']:
        print("Please select h to hit or s to stay")
        move = input("Move? (hit/stay) ")

    game_over = False

    #user sequence
    while user.bust == False and move == 'h':
        card = deck.draw()
        user.add_card(card)

        #display game status
        game_status(bet, dealer, name, user)

        #check win/loss conditions
        user.check_bust()
        
        if user.get_value() > 21:
            print("{} bust".format(name))
            game_over = True
            bank -= 100
            return bank
        move = input("\nMove? (hit/stay) ")
        while move.lower() not in ['h', 's']:
            print("Please select h to hit or s to stay")
            move = input("Move? (hit/stay) ")

    #dealer sequence
    while dealer.bust == False and game_over == False:
        card = deck.draw()
        dealer.add_card(card)

        #display game status
        game_status(bet, dealer, name, user)

        #check win/loss conditions
        dealer.check_bust()
        
        if dealer.get_value() > 21:
            print("Dealer Bust")
            bank += 100
            return bank
        elif dealer.get_value() >= 17:
            if dealer.get_value() > user.get_value():
                print("Dealer wins")
                bank -= 100
                return bank
            elif dealer.get_value() < user.get_value():
                print("{} wins".format(name))
                bank += 100
                return bank
            else:
                print("Push")
                return bank

#initializes with suit and rank
#return suit and/or rank
#print card information
class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def __str__(self):
        return '{} ({})'.format(self.get_rank(), self.get_suit())

#defines suits and ranks
#iterates through suits and ranks to create 52 object list using Card class
class Deck:
    def __init__(self):
        suits = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        
        self.cards = []
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit, rank))

    #calls random module to reorder deck list
    def shuffle(self):
        random.shuffle(self.cards)

    #removes and return first object from deck list
    def draw(self):
        return self.cards.pop(0)

#defines player
#assigns bank, hand, and status
class Player:
    def __init__(self, hand, bank=None):
        self.hand = hand
        self.bank = bank
        self.bust = False
        self.value = 0

    #appends Card object to hand list
    def add_card(self, card):
        self.hand.append(card)

    #iterates through hand list, formats, and displays Card objects
    def get_hand(self):
        for card in self.hand:
            print(card, sep=' ', end=' ')

    #returns bank attribute
    def get_bank(self):
        return self.bank
        
    #iterates through hand and totals value based on Card object
    #returns processed value
    def get_value(self):
        self.value = 0
        aces = 0
        
        for card in self.hand:
            if card.rank == 'A':
                self.value += 11
                aces += 1
            elif card.rank in ['J', 'Q', 'K']:
                self.value += 10
            else:
                self.value += int(card.rank)

        #control flow for variable ace value (11 or 1)
        #based on bust criteria, number of aces, and total value
        if self.value >= 54 and aces == 4:
            self.value -= 40
        elif self.value >= 43 and aces >= 3:
            self.value -= 30
        elif self.value >= 32 and aces >= 2:
            self.value -= 20
        elif self.value > 21 and aces >= 1:
            self.value -= 10 
                
        return self.value

    #calls value method and updates bust status if value > 21
    def check_bust(self):
        if self.value > 21:
            self.bust = True
        return self.bust

#call main function and begin the program
main()
