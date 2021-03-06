"""RGG that is made for fun of class"""

# Import Statements----------------------------------------------------------------------------------------------------
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import List, Tuple
import random
import time
import sys
import copy


# Input Blocker--------------------------------------------------------------------------------------------------------
def blocking_input(acceptable_responses: [str]) -> str:
    """calls input('>') until an appropriate input is selected
    :param acceptable_responses: the inputs that will get a go-ahead"""
    while True:
        output = input('>')
        if output in acceptable_responses:
            break
    return output


def dialogue_input():
    text_input = None
    while text_input is None:
        text_input = blocking_input([''])
        if text_input == '':
            break
    return text_input


class Direction:
    def __init__(self, direction: str, directions_used: List):
        self.direction = direction
        self.directions_used = directions_used

    def choose_direction(self):
        direction = blocking_input(['n', 's', 'e', 'w'])
        self.directions_used.append(direction)
        if direction in self.directions_used:
            print('You already went that way')


class Item:
    def __init__(self,
                 name: str,
                 hp_restore: int):
        self.name = name
        self.hp_restore = hp_restore

    def use_item(self, player):
        player.hp += min(player.max_hp, self.hp_restore)

# Character class-------------------------------------------------------------------------------------------------------
class Character:
    """All the methods a character in the game can perform"""
    def __init__(self,
                 name: str,
                 hp: float,
                 max_hp: float,
                 attack: float,
                 speed: float,
                 exp: int,
                 level_exp: int,
                 team: int):

        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.speed = speed
        self.team = team
        self.exp = exp
        self.level_exp = level_exp
        self.level = 1

        """:param max_hp: hp of an unharmed player
        :param level: level of the player, 1-100 eventually
        :param exp: value of the current exp a player has
        :param target_exp: value of the exp needed for a player's level to increase"""

    def is_alive(self) -> bool:
        """Returns true if the player if they are alive"""
        return self.hp > 0

    def is_ally(self, other_player) -> bool:
        """returns true if the player is an ally"""
        return other_player.team == self.team

    def deal_damage(self, other_player: 'Character'):
        """The base method for dealing damage to an enemy player
        :param other_player: target of damage"""
        if other_player.is_alive():
            other_player.hp -= self.attack
            print(f'{self.name} attacked {other_player.name}')
        return other_player

    def get_all_enemies(self, players: List['Character']) -> List[int]:
        """returns the location of all enemy players in a list"""
        return [
            index for index, player in enumerate(players)
            if not self.is_ally(player) and player.is_alive()
        ]

    def act(self, players: List):
        item = Item
        all_enemy_locations = self.get_all_enemies(players)
        if self.is_alive():
            if item in inventory:
                for item in inventory:
                    Item.use_item(item, self)
            else:
                print('No items to use')
            if all_enemy_locations:
                targeted_index = all_enemy_locations[0]
                targeted_player = players[targeted_index]
                damaged_player = self.deal_damage(targeted_player)
                players[targeted_index] = damaged_player

        return players


class Ally(Character):
    def __init__(self,
                 name: str,
                 hp: float,
                 max_hp: float,
                 attack: float,
                 speed: float,
                 exp: int,
                 level_exp: int):
        super().__init__(name, hp, max_hp, attack, speed, exp, level_exp, team=1)

    def fight_input(self):
        item = Item
        print('What will you do?')
        print('[f]: fight, [r]: run, [i]: item')
        fight_output = None
        while fight_output is None:
            fight_output = blocking_input(['f', 'r', 'i'])
            if fight_output == 'f':
                pass
            elif fight_output == 'r':
                print('You can]\'t escape!')
                fight_output = None
            elif fight_output == 'i':
                if item in inventory:
                    for item in inventory:
                        print(f'Do you want to use {item}')
                        item_input = blocking_input(['y', 'n'])
                        if item_input == 'y':
                            Item.use_item(item, self)
                        elif item_input == 'n':
                            fight_output = None

                else:
                    print('Inventory is empty')
                    fight_output = None

    def act(self, players: List):
        all_enemy_locations = self.get_all_enemies(players)
        if self.is_alive():
            if all_enemy_locations:
                print('Who do you attack?')
                print('"0", "1", "2", or "3" for the corresponding enemy position')
                print([player.name for player in players if player.team == 2 and player.is_alive])
                target_input = None
                while target_input is None:
                    target_input = input('>')
                    try:
                        targeted_index = all_enemy_locations[int(target_input)]
                        targeted_player = players[targeted_index]
                        damaged_player = self.deal_damage(targeted_player)
                        players[targeted_index] = damaged_player
                    except ValueError:
                        print('That is not a valid target')
                        target_input = None
                    except IndexError:
                        print('That is not a valid target')
                        target_input = None

        return players


class Enemy(Character):
    def __init__(self,
                 name: str,
                 hp: float,
                 max_hp: float,
                 attack: float,
                 speed: float,
                 exp: int,
                 level_exp: int):
        super().__init__(name, hp, max_hp, attack, speed, exp, level_exp, team=2)

    def act(self, players: List):
        item = Item
        all_enemy_locations = self.get_all_enemies(players)
        if self.is_alive():
            if all_enemy_locations:
                targeted_index = random.choice(all_enemy_locations)
                targeted_player = players[targeted_index]
                damaged_player = self.deal_damage(targeted_player)
                players[targeted_index] = damaged_player

        return players


# How the battle runs--------------------------------------------------------------------------------------------------
@dataclass(order=True)
class Move:
    """Handles the priority Queue"""
    priority: float
    player: Character = field(compare=False)


class Battle:
    """list of characters, and order of moves"""

    def __init__(self, players: List['Character']):
        self.players = players
        self.battle_queue = PriorityQueue()

    def add_into_queue(self, player: Character, game_time: float) -> None:
        """adds a player back based on game time
        faster players go first"""
        move = Move(priority=game_time + 1/player.speed, player=player)
        self.battle_queue.put(move)

    def get_from_queue(self) -> Tuple[Character, int]:
        """removes the player from the queue to add back after cooldown"""
        move = self.battle_queue.get()
        return move.player, move.priority

    def is_over(self) -> bool:
        """true if the battle is over"""
        return self.battle_queue.empty()

    def level_up(self):
        exp_gain = 200
        for player in self.players:
            if player.team == 1:
                player.exp += exp_gain
                print(f'{player.name} received {exp_gain} experience points!')
                if player.exp == player.level_exp:
                    print(f'{player.name} leveled up!')
                    player.level += 1
                    player.max_hp += 2
                    player.hp = player.max_hp
                    player.attack += 1
                    player.speed += 1
                    player.exp = 0
                    player.level_exp *= 2
                    print(f'{player.name}: {player.level}')

    def run(self):
        """Makes the battle loop while it's not over"""
        print(f'{[player.name for player in self.players if player.team == 2]} appeared!')
        dialogue_input()
        # Empty print statements are to separate texts in the console
        # To improve readability during the program's running
        for player in self.players:
            self.add_into_queue(player=player, game_time=0)

        while not self.is_over():
            acting_player, current_game_time = self.get_from_queue()
            if acting_player.is_alive():
                print(f'{acting_player.name}\'s turn')
                if acting_player.team == 1:
                    acting_player.fight_input()
                    acting_player.act(self.players)
                    dialogue_input()
                    for player in self.players:
                        if player.is_alive():
                            print(f'{player.name} LV: {player.level}')
                            print(f'HP: {int(player.hp)}/{player.max_hp}')
                    if acting_player.is_alive and acting_player.get_all_enemies(self.players):
                        self.add_into_queue(acting_player, current_game_time)
            else:
                print(f'{acting_player.name} is dead')
            print()
        for player in self.players:
            if player.team == 1 and not player.is_alive():
                print('You Died')
            elif player.team == 1 and player.is_alive():
                pass
        print('You win!')
        self.level_up()


# Main Loop------------------------------------------------------------------------------------------------------------
if __name__ == '__main__':
    inventory = []
    debugger = False
    if debugger is True:
        names = {'1': 'Tyler', '2': 'Alex', '3': 'Robert'}
        print('Debugger mode...')
        print('Welcome debugger!')
        print('1: Tyler, 2: Alex, 3: Robert')
        print('Which debugger are you?')
        name = None
        while name is None:
            name_input = input('>')
            name = names.get(name_input)
        print(f'Welcome {name}')
    else:
        print('What is your name?')
        name = input('>')
    PC = Ally(name=name, hp=20, max_hp=20, attack=4, speed=5, exp=0, level_exp=200)
    print('press enter to move to the next line of text')
    print('You wake in your bed.')
    dialogue_input()
    print('You decide to get onto your computer.')
    dialogue_input()
    print('Suddenly, as you turn the computer on, you\'re transported to an unfamiliar world.')
    dialogue_input()
    print('"Welcome to the Algorithm." You hear a voice saying out of nowhere.')
    dialogue_input()
    print('Suddenly an apparition appears and attacks!')
    anime_male = Enemy(name='Anime Male', hp=20, max_hp=20, attack=3, speed=5, exp=0, level_exp=200)
    battle = Battle(players=[PC, anime_male])
    battle.run()
    potion = Item(name='potion', hp_restore=10)
    print('You found a potion.')
    inventory.append(potion)
    print('Thank you for playing the demo!')
    time.sleep(3)




