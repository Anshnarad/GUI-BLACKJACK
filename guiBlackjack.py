# Mini-project #6 - GUI Blackjack Vegas
# Coursera(ITIPIP) Final Project December 2017
# Created and submitted by Ansh Narad-User43
# http://www.codeskulptor.org/#user43_xW9zA57kI8_0.py (original Version)
# Modified a Little Bit
import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")
CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = "HIT OR STAND?"
player_score = 0
dealer_score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank
    def __str__(self):
        return self.suit + self.rank
    def get_suit(self):
        return self.suit
    def get_rank(self):
        return self.rank
    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] +CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards=[]
    def __str__(self):
        result=""
        for card in self.cards:
            result += " " + card.__str__()
        return " YOUR HAND CONTAINS " + result
    def add_card(self, card):
        self.cards.append(card)
    def get_value(self):
        value = 0 
        contains_ace = False
        for card in self.cards:
            rank= card.get_rank()
            value += VALUES[rank]
            if (rank=='A'):
                contains_ace = True
        if (value<11 and contains_ace):
                value+=10       
        return value
    def draw(self, canvas, pos):
        for card in self.cards:
            card.draw(canvas,pos)
            pos[0]+= 85
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards=[]
        for suit in SUITS:
            for rank in RANKS:
                self.cards.append(Card(suit,rank))
    def shuffle(self):
        random.shuffle(self.cards)
    def deal_card(self):
        return self.cards.pop(0)
    def __str__(self):
        result=""
        for card in self.cards:
            result="" + card.__str__()  
        return "THE DECK CONTAINS" + result



#define event handlers for buttons
def deal():
    global outcome, in_play,player_hand,dealer_hand,deck,dealer_score
    if(in_play==True):
        outcome= "PLAYER WINS. WANT NEW DEAL??"
        dealer_score+=1
        in_play=False  
    else:
        deck = Deck()
        outcome
        # your code goes here
        deck.shuffle()
        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        in_play = True

def hit():
    global outcome, in_play

    if in_play:
        if player_hand.get_value() <= 21:
            player_hand.add_card(deck.deal_card())
            print " PLAYER HAND IS: " , player_hand
        if player_hand.get_value() > 21:
            outcome = "YOU ARE BUSTED. WANT NEW DEAL?"
            in_play = False
            print "YOU ARE BUSTED, BETTER LUCK NEXT TIME!"
    
       
def stand():
    global outcome, player_score, dealer_score, in_play
    in_play = False
    while dealer_hand.get_value() < 17:
        dealer_hand.add_card(deck.deal_card())
    print "Dealer hand contains" , dealer_hand
    if dealer_hand.get_value() > 21:
        outcome = "DEALER BUSTED. Congratulations! PLAYER WINS."
        print "Dealer is busted. Player wins."
        player_score += 1
    else:
        if dealer_hand.get_value() >= player_hand.get_value() or player_hand.get_value() > 21:
            print "DEALER WINS"
            outcome = "DEALER WINS. WANT NEW DEAL?"
            dealer_score += 1
        else:
            print "PLAYER WINS. NEW DEAL?"
            outcome = "PLAYER WINS. NEW DEAL?"
            player_score += 1

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    global outcome, in_play, card_back, card_loc, player_score, dealer_score
    canvas.draw_text("BLACKJACK VEGAS 21+", [230, 50], 50 ,"gold")
    canvas.draw_text("*********************************************************", [230, 70], 20 ,"WHITE")
    player_hand.draw(canvas, [100, 400])
    dealer_hand.draw(canvas, [100, 250])
    canvas.draw_text(" %s " % outcome, [10, 150], 40,"Gold")
    canvas.draw_text("DEALER SCORE: %s " % dealer_score, [600, 220], 30 ,"RED")
    canvas.draw_text("PLAYER SCORE: %s " % player_score, [600, 370], 30 ,"CYAN")
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (136,293), CARD_BACK_SIZE)



# initialization frame
frame = simplegui.create_frame("Blackjack", 1000, 600)
frame.set_canvas_background("black")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
