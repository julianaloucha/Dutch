import turtle
import random
import time
from globals import *

# global players
# global face_cards
# global Card
# global full_deck
# global open_deck
# global num_players
# global wn
# global pen



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


def print_deck(deck):
    for card in deck:
        print(f"{card.value} of {card.suit}")

def print_card_in_deck(deck, index):
    card = deck[index]
    print(f"{card.value} of {card.suit}")


def see_cards(current_player):
    card_index = int(input("Enter the index of a card to see: ")) - 1
    print_card_in_deck(players[current_player].hand, card_index)


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

        draw_and_discard(current_player)

    print("Dutch claimed by: ", players[dutch_claimer].name)
    print("Sum of cards for each player:")
    for player in players:
        print(f"{player.name}: {sum([card.sum for card in player.hand])}")

    # Determine the winner
    winner = min(players, key=lambda player: sum([card.sum for card in player.hand]))
    print(f"The winner is {winner.name}!!!")
    print()
    print("End of the game")

def draw_and_discard(current_player):
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

    draw_and_discard(current_player)

    # next player
    play_round(current_player)


def discard_similar_cards(current_player):
    # Discard similar cards
    card_index = int(input("Discard similar card (if no, select 0): ")) - 1
    if card_index != -1:
        card = players[current_player].hand[card_index]
        if open_deck[-1].value == card.value:
            players[current_player].hand[card_index] = None
            open_deck.append(card)
            print(f"Discarded card: {card.value} of {card.suit}")
            print()
            print("Open deck:")
            print_card_in_deck(open_deck, -1)
            print()
            discard_similar_cards(current_player)
        else:
            print(f"Ops! {card.value} of {card.suit} is not a similar card.")
            print()
            players[current_player].draw_card(full_deck)
            return


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
