import random
from functions import *
from globals import *

# wn = turtle.Screen()
# wn.title("Card Game")
# wn.bgcolor("white")
# wn.setup(width=800, height=600)
# wn.tracer(0)

# pen = turtle.Turtle()
# pen.speed(0)
# pen.hideturtle()







# print("Full deck:")
# print_deck(full_deck)
# print()

# Shuffle the deck
random.shuffle(full_deck)
# print("Shuffled deck:")
# print_deck(full_deck)
# print()



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


see_cards(current_player)
see_cards(current_player)

# players[current_player].draw_card(full_deck)
print()
# print_deck(players[current_player].hand)

card_drawn = full_deck.pop()
print("Card drawn:")
print_card_in_deck([card_drawn], 0)


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

# Move to the next player


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

    draw_and_discard(current_player)
    current_player = (current_player + 1)
    print(f"Current: {current_player}")

current_player -= current_player


play_round(current_player)




# # Render player one's hand
# render_cards(players[0])
# wn.update()

# wn.mainloop()


################################################

# shuffle open deck

# limit
# discart simmilar card
# if wrong get 1 more card

#sockets to play in lan
# player amount decided by the amount in lan
# min 2 players
# max 8 players
# change language option