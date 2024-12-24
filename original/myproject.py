import turtle
import random
import time

# wn = turtle.Screen()
# wn.title("Card Game")
# wn.bgcolor("white")
# wn.setup(width=800, height=600)
# wn.tracer(0)

# pen = turtle.Turtle()
# pen.speed(0)
# pen.hideturtle()


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

# Function to generate a deck of cards
def generate_cards(values, suits):
    cards = []
    for value in values:
        for suit in suits:
            if (value == 13 and suit == 'Spades') or (value == 13 and suit == 'Clubs'):
                card_value = face_cards[value]
                cards.append(Card(card_value, suit, -1))
            elif value in face_cards:
                card_value = face_cards[value]
                cards.append(Card(card_value, suit, value))
            else:
                cards.append(Card(value, suit, value))
            
    return cards

full_deck = generate_cards(values, suits)
open_deck = []

def print_deck(deck):
    for card in deck:
        print(f"{card.value} of {card.suit}")

def print_card_in_deck(deck, index):
    card = deck[index]
    print(f"{card.value} of {card.suit}")

# print("Full deck:")
# print_deck(full_deck)
# print()

# Shuffle the deck
random.shuffle(full_deck)
# print("Shuffled deck:")
# print_deck(full_deck)
# print()

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

# Distribute 4 cards to each player
for _ in range(4):
    for player in players:
        player.draw_card(full_deck)

# Print each player's deck
for player in players:
    print(f"{player.name}'s deck:")
    print_deck(player.hand)
    print()

# Print the remaining deck
# print("Remaining deck:")
# print_deck(full_deck)

# print(len(players))

# Who's turn is it?
current_player = 0

######### FIRST ROUND #########

# Display two cards in the current player's hand
print(f"{players[current_player].name}'s turn:")

print()
# Inquire which card to play
print("Select two cards to see:")

def see_cards(current_player):
    card_index = int(input("Enter the index of a card to see: ")) - 1
    print_card_in_deck(players[current_player].hand, card_index)

see_cards(current_player)
see_cards(current_player)

players[current_player].draw_card(full_deck)
print()
# print_deck(players[current_player].hand)
print("Card drawn:")
print_card_in_deck(players[current_player].hand, -1)
print()

card_index = int(input("Select a card to discart: ")) - 1
discarded_card = players[current_player].hand.pop(card_index)
print(f"Discarded card: {discarded_card.value} of {discarded_card.suit}")
open_deck.append(discarded_card)
print()
# print_deck(open_deck)

def check_discarded_card(discarded_card, current_player):
    if discarded_card.value == face_cards[12]:
        print("You have discarded a Queen. You get to see a card of your own deck.")
        see_cards(current_player)
        print()
    elif discarded_card.value == face_cards[11]:
        print("You have discarded a Jack. You get to switch two cards of your choice.")
        player1 = int(input("Which player would you like to swich cards: ")) - 1
        player1_card = int(input("Which one of their cards would you like to swich: ")) - 1
        player2 = int(input("Which player would you like to swich cards with: ")) - 1
        player2_card = int(input("Which one of their cards would you like to swich: ")) - 1
        players[player1].hand[player1_card], players[player2].hand[player2_card] = players[player2].hand[player2_card], players[player1].hand[player1_card]
        print()
        # Print each player's deck
        for player in players:
            print(f"{player.name}'s deck:")
            print_deck(player.hand)
            print()

check_discarded_card(discarded_card, current_player)

# Move to the next player

def choose_deck():
    print("Choose a deck to draw a card from:")
    print("1. Open deck")
    print("2. Closed deck")
    choice = int(input("Enter your choice: "))
    if choice == 1:
        card = open_deck.pop()
    else:
        card = full_deck.pop()
    return card

# play first round
current_player = (current_player + 1)
while current_player < num_players:
    #Display two cards in the current player's hand
    print(f"{players[current_player].name}'s turn:")

    print()
    # Inquire which card to play
    print("Select two cards to see:")

    see_cards(current_player)
    see_cards(current_player)
    print()

    print("Open deck:")
    # print last card in open deck
    print_card_in_deck(open_deck, -1)
    print()

    players[current_player].hand.append(choose_deck())

    print("Card drawn:")
    print_card_in_deck(players[current_player].hand, -1)
    print()

    card_index = int(input("Select a card to discart: ")) - 1
    discarded_card = players[current_player].hand.pop(card_index)
    print(f"Discarded card: {discarded_card.value} of {discarded_card.suit}")
    open_deck.append(discarded_card)
    print()
    check_discarded_card(discarded_card, current_player)
    current_player = (current_player + 1)
    print(f"Current: {current_player}")

current_player -= current_player

def last_round(current_player):
    dutch_claimer = current_player
    while current_player != dutch_claimer:
        current_player = (current_player + 1) % num_players # Move to the next player in a circular fashion

        #Display two cards in the current player's hand
        print(f"{players[current_player].name}'s turn:")

        print()

        dutch = input("Do you want claim Dutch? (dutch/no): ")
        if dutch == "dutch":
            last_round()
        
        # Inquire which card to play
        
        print("Open deck:")
        # print last card in open deck
        print_card_in_deck(open_deck, -1)
        print()

        players[current_player].hand.append(choose_deck())

        print("Card drawn:")
        print_card_in_deck(players[current_player].hand, -1)
        print()

        card_index = int(input("Select a card to discart: ")) - 1
        discarded_card = players[current_player].hand.pop(card_index)
        print(f"Discarded card: {discarded_card.value} of {discarded_card.suit}")



        open_deck.append(discarded_card)
        print()
        check_discarded_card(discarded_card, current_player)
        print()
    print("Dutch claimed by: ", players[dutch_claimer].name)
    print("Sum of cards for each player:")
    for player in players:
        print(f"{player.name}: {sum([card.sum for card in player.hand])}")

    # Determine the winner
    winner = min(players, key=lambda player: sum([card.sum for card in player.hand]))
    print(f"The winner is {winner.name}!!!")
    print()
    print("End of the game")

def play_round(current_player):
    current_player = (current_player + 1) % num_players # Move to the next player in a circular fashion

    #Display two cards in the current player's hand
    print(f"{players[current_player].name}'s turn:")

    print()

    dutch = input("Do you want claim Dutch? (dutch/no): ")
    if dutch == "dutch":
        last_round()
    
    # Inquire which card to play
    
    print("Open deck:")
    # print last card in open deck
    print_card_in_deck(open_deck, -1)
    print()

    card_drawn = choose_deck()
    print("Card drawn:")
    print_card_in_deck([card_drawn], 0)


    # players[current_player].hand.append(choose_deck())

    # print("Card drawn:")
    # print_card_in_deck(players[current_player].hand, -1)
    print()

    card_index = int(input("Select a card to discart (for drawn card select 0): ")) - 1
    if card_index == -1:
        discarded_card = card_drawn
    else:
        discarded_card = players[current_player].hand[card_index]
        players[current_player].hand[card_index] = card_drawn


    print(f"Discarded card: {discarded_card.value} of {discarded_card.suit}")

    open_deck.append(discarded_card)
    print()
    check_discarded_card(discarded_card, current_player)
    print()

    # next player
    play_round(current_player)

play_round(current_player)





# shuffle open deck
# switch new card with discarted card ## copy 307
# limit
# discart simmilar card
# if wrong get 1 more card

#sockets to play in lan
# player amount decided by the amount in lan
# min 2 players
# max 8 players
# change language option




#####################################################################
###################### DISPLAY ######################################
#####################################################################

# def on_card_button_click(card, x, y):
#     pen.clear()
#     positions = [(-150, 100), (150, 100), (-150, -100), (150, -100)]
#     for i, c in enumerate(players[0].hand):
#         if c == card:
#             c.render(positions[i][0], positions[i][1], pen)
#         else:
#             render_blank_card(positions[i][0], positions[i][1])
#     wn.update()

# # render the cards
# def render_cards(player):
#     pen.clear()
#     positions = [(-150, 100), (150, 100), (-150, -100), (150, -100)]
#     for i, card in enumerate(player.hand):
#         render_blank_card(positions[i][0], positions[i][1])
#         create_card_button(card, positions[i][0], positions[i][1] + 100)  # Create button on top of each card

# def render_blank_card(x, y):
#     pen.penup()
#     pen.goto(x, y)
#     pen.color("black")
#     pen.goto(x-50, y+75)
#     pen.pendown()
#     # pen.goto(x+50, y+75)
#     # pen.goto(x+50, y-75)
#     # pen.goto(x-50, y-75)
#     # pen.goto(x-50, y+75)
    
#     # Fill the card with blue color
#     pen.fillcolor("blue")
#     pen.begin_fill()
#     pen.goto(x+50, y+75)
#     pen.goto(x+50, y-75)
#     pen.goto(x-50, y-75)
#     pen.goto(x-50, y+75)
#     pen.end_fill()

# def create_card_button(card, x, y):
#     button = turtle.Turtle()
#     button.speed(0)
#     button.shape("square")
#     button.color("black")
#     button.shapesize(stretch_wid=1, stretch_len=5)  # Adjust the size of the button
#     button.penup()
#     button.goto(x, y)
#     button.onclick(lambda x, y: on_card_button_click(card, x, y))

# def on_player_button_click(player_index):
#     render_cards(players[player_index])
#     wn.update()

# # # Render player one's hand
# # render_cards(players[0])
# # wn.update()

# # wn.mainloop()