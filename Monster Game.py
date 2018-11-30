import random
import sys
import time

inventory = []

def blocking_input(acceptable_responses: [str]):
    while True:
        output = input('>')
        if output in acceptable_responses:
            break
    return output

def start_screen():
    print('Will you survive?')
    print('[s]tart')
    print('[q]uit')


def start_options():
    start_screen()
    start_input = blocking_input(['s', 'q'])
    if start_input == 's':
        main_loop()
    if start_input == 'q':
        print('Are you sure you want to quit? y or n')
        quit_input = blocking_input(['y', 'n'])
        if quit_input == 'y':
            print('Thank You for Playing!')
            time.sleep(3)
        if quit_input == 'n':
            start_options()


rooms = {'living room': {
              'north': 'kitchen',
              'south': 'basement',
              'west': 'upstairs',
              'east': 'hallway'
              },
         'upstairs': {
             'north': 'attic',
             'south': 'bedroom',
             'east': 'living room',
             'west': 'kids bedroom'
             },
         'attic': {
             'south': 'upstairs',
             'item': 'monster'
             },
         'basement': {
             'north': 'living room',
             'item': 'monster'
             },
         'kitchen': {
             'south': 'living room',
             'west': 'outside'
             },
         'hallway': {
             'west': 'living room',
             'east': 'master bedroom'
             },
         'master bedroom': {
             'west': 'hallway',
             'item': 'key'
             },
         'bedroom': {
             'north': 'upstairs',
             'item': 'flashlight'
             },
         'kids bedroom': {
             'east': 'upstairs',
             'item': 'shield'
             }
         }





def main_loop():
    current_room = 'living room'
    print('You are trapped in a house in the woods!')
    print('You can\'t see a thing.')
    print('Try to escape')
    print('Controls:')
    print('go [direction]')
    print('get [item]')
    while True:
        print(f'You are in the ' + current_room)
        print('inventory: ' + str(inventory))
        if 'item' in rooms[current_room]:
            print(f'You see a ' + rooms[current_room]['item'])
        move = input('>').split()
        if move[0] == 'go':
            if move[1] in rooms[current_room]:
                current_room = rooms[current_room][move[1]]
            else:
                print('You can\'t go that way!')
        if move[0] == 'get':
            if 'item' in rooms[current_room] and move[1] in rooms[current_room]['item']:
                inventory.append(rooms[current_room]['item'])
                print(f'you got ' + rooms[current_room]['item'])
                del rooms[current_room]['item']
            else:
                print(f'can\'t get {move[1]}!')
        if 'item' in rooms[current_room] and rooms[current_room]['item'] == 'monster':
            if 'shield' in inventory:
                print('The shield stopped the monster.')
                print('but the shield breaks in the process.')
                inventory.remove('shield')
            else:
                print('The monster got you!')
                print('Game Over!')
                start_options()
        if current_room == 'outside':
            if 'key' in inventory and 'flashlight' in inventory:
                print('You escaped!')
                start_options()
            elif 'key' in inventory and 'flashlight' not in inventory:
                print('The door has been unlocked.')
                print('but it\'s too dark to see.')
                current_room = 'kitchen'
            elif 'key' not in inventory:
                print('The door is locked')
                current_room = 'kitchen'



start_options()
