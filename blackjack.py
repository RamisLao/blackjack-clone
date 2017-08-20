# Mini-project #6 - Blackjack

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
outcome = "Hit or Stand?"
score = 0
title = "BLACKJACK"

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
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.cards = []

    def __str__(self):
        text = "Hand contains "
        for card in self.cards:
            text += card.__str__() + " "
        return text

    def add_card(self, card):
        return self.cards.append(card)

    def get_value(self):
        hand_value = 0
        aces = False
        for card in self.cards:
            if card.get_rank() == 'A':
                aces = True
        if not aces:
            for card in self.cards:
                hand_value += VALUES[card.get_rank()]
            return hand_value
        else:
            for card in self.cards:
                hand_value += VALUES[card.get_rank()]
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
        
    def draw(self, canvas, pos):
        position = list(pos)
        for card in self.cards:
            card.draw(canvas, position)
            position[0] += CARD_SIZE[0]
            
 
        
# define deck class 
class Deck:
    def __init__(self):
        self.cards = []
        [self.cards.append(Card(i, j)) for i in SUITS for j in RANKS]

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.cards)

    def deal_card(self):
        return self.cards.pop(0)
    
    def __str__(self):
        text = "Deck contains "
        for card in self.cards:
            text += card.__str__() + " "
        return text

# Variables

deck = Deck()
player = Hand()
dealer = Hand()
    
#define event handlers for buttons
def deal():
    global outcome, in_play, deck, player, dealer, score
    
    if in_play:
        outcome = "You lost. Now, Hit or Stand?"
        score -= 1
    else:
        outcome = "Hit or Stand?"
        
    in_play = True
        
    deck = Deck()
    player = Hand()
    dealer = Hand()

    deck.shuffle()
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
    player.add_card(deck.deal_card())
    dealer.add_card(deck.deal_card())
 

def hit():
    global outcome, score, in_play
    if in_play:
        outcome = 'Hit or Stand?'
        if player.get_value() <= 21:
            player.add_card(deck.deal_card())
            if player.get_value() > 21:
                outcome = "You have busted! New deal?"
                in_play = False
                score -= 1
    else:
        outcome = "The game's over. New deal?"
        
       
def stand():
    global outcome, in_play, score
    outcome = ''
    if in_play:
        in_play = False
        if outcome == "You have busted! New deal?":
            outcome = "You are busted! Deal again!"
        else:
            while dealer.get_value() < 17:
                dealer.add_card(deck.deal_card())
            if dealer.get_value() > 21:
                outcome = "The dealer has busted! New deal?"
                score += 1
            elif player.get_value() <= dealer.get_value():
                outcome = "The dealer has won! New deal?"
                score -= 1
            else:
                outcome = "You have won! New deal?"
                score += 1
    else:
        outcome = "The game's over. New deal?"
  

# draw handler    
def draw(canvas):
    global title, in_play
    canvas.draw_polygon([(110, 30), (490, 30), (490, 110), (110, 110)], 2, "Black", "White")
    pos = [120, 90]
    color = "Red"
    for letter in title:
        canvas.draw_text(letter, pos, 60, color)
        if color == "Red":
            color = "Black"
        else:
            color = "Red"
        pos[0] += 40
    canvas.draw_polygon([(0, 160), (600, 160), (600, 200), (0, 200)], 2, "Black", "White")
    canvas.draw_line((300, 159), (300, 201), 2, "Black")
    canvas.draw_text("Dealer's Hand", (80, 190), 30, "Black")
    canvas.draw_text("Score: " + str(score), (400, 190), 30, "Black")
    dealer.draw(canvas, (110, 230))
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, (110 + CARD_CENTER[0], 230 + CARD_CENTER[1]), CARD_SIZE)
    canvas.draw_polygon([(0, 360), (600, 360), (600, 400), (0, 400)], 2, "Black", "White")
    canvas.draw_text("Player: ", (80, 390), 30, "Black")
    canvas.draw_text(outcome, (175, 390), 30, "Black")
    player.draw(canvas, (110, 430))


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


# remember to review the gradic rubric
