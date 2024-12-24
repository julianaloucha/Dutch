values = list(range(1,14))
suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
symbols = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'}

face_cards = {1: 'Ace', 11: 'Jack', 12: 'Queen', 13: 'King',
              'Ace': 1, 'Jack': 11, 'Queen': 12, 'King': 13}

# Class to represent a card
class Card:
    def __init__(self, value, suit, sum):
        self.value = value
        self.suit = suit
        self.sum = sum
        
    def render(self, x, y, pen):
        pen.penup()
        pen.goto(x, y)
        pen.color("black")
        pen.goto(x-50, y+75)
        pen.pendown()
        pen.goto(x+50, y+75)
        pen.goto(x+50, y-75)
        pen.goto(x-50, y-75)
        pen.goto(x-50, y+75)
        
        # Draw the card value and suit symbol
        pen.penup()
        pen.goto(x-40, y+50)
        if self.suit in ['Hearts', 'Diamonds']:
            pen.color("red")
        else:
            pen.color("black")
        pen.write(f"{self.value}", align="left", font=("Arial", 16, "normal"))
        pen.goto(x+30, y-60)
        pen.write(f"{symbols[self.suit]}", align="left", font=("Arial", 16, "normal"))

class Player:
    def __init__(self, name, hand):
        self.name = name
        self.hand = hand

    def __repr__(self):
        return f"{self.name} has {self.hand}"
    
    def draw_card(self, deck):
        card = deck.pop()
        self.hand.append(card)
        return card

# Inquire the number of players
# num_players = int(input("Enter the number of players: "))
num_players = 4

# Create 4 players
players = [Player(f"Player {i+1}", []) for i in range(num_players)]

open_deck = []

