from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room, leave_room
import random
from globals import Card, Player, values, suits, face_cards
from functions import generate_cards, print_deck

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Game state
rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/')
# def home():
#     return render_template('connect.html')

# @app.route('/room')
# def room():
#     return render_template('room.html')

@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    if room not in rooms:
        rooms[room] = {
            'players': [],
            'deck': generate_cards(values, suits),
            'open_deck': []
        }
        random.shuffle(rooms[room]['deck'])
    
    if len(rooms[room]['players']) >= 8:
        emit('update', {'msg': "The room is full. Maximum 8 players allowed."}, to=request.sid)
        leave_room(room)
        return

    player = Player(username, [])
    rooms[room]['players'].append(player)
    emit('update', {'msg': f"{username} has joined the game."}, room=room)
    emit('player_count_update', {'playerCount': len(rooms[room]['players'])}, room=room)

@socketio.on('start_game')
def start_game(data):
    room = data['room']
    if room in rooms:
        if len(rooms[room]['players']) < 2:
            emit('update', {'msg': "Not enough players to start the game. Minimum 2 players required."}, room=room)
            return

        for _ in range(4):
            for player in rooms[room]['players']:
                player.draw_card(rooms[room]['deck'])

        random.shuffle(rooms[room]['players'])
        player_order = [player.name for player in rooms[room]['players']]
        emit('update', {'msg': f"Player order: {', '.join(player_order)}"}, room=room)

        players_hands = {player.name: [(card.value, card.suit) for card in player.hand] for player in rooms[room]['players']}
        emit('game_started', {
            'hands': players_hands,
            'first_player': player_order[0]
        }, room=room)

        # Notify the first player to start
        emit('player_turn', {
            'current_player': player_order[0]
        }, room=room)

@socketio.on('draw_card')
def draw_card(data):
    room = data['room']
    player_name = data['player']
    if room in rooms:
        player = next((p for p in rooms[room]['players'] if p.name == player_name), None)
        if player:
            card = rooms[room]['deck'].pop()
            player.hand.append(card)
            emit('card_drawn', {'player': player_name, 'card': (card.value, card.suit)}, room=room)

@socketio.on('discard_card')
def discard_card(data):
    room = data['room']
    player_name = data['player']
    card_index = data['card_index']
    if room in rooms:
        player = next((p for p in rooms[room]['players'] if p.name == player_name), None)
        if player:
            discarded_card = player.hand.pop(card_index)
            rooms[room]['open_deck'].append(discarded_card)
            emit('card_discarded', {
                'player': player_name,
                'discarded_card': (discarded_card.value, discarded_card.suit)
            }, room=room)

            # Notify the next player
            current_player_index = rooms[room]['players'].index(player)
            next_player_index = (current_player_index + 1) % len(rooms[room]['players'])
            next_player = rooms[room]['players'][next_player_index]
            emit('player_turn', {
                'current_player': next_player.name
            }, room=room)

if __name__ == '__main__':
    socketio.run(app, debug=True)
