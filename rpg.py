"""RGG that is made for fun of class"""

# Import Statements----------------------------------------------------------------------------------------------------
from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import List, Tuple, Dict
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
    """takes input to pass on the dialogue"""
    text_input = None
    while text_input is None:
        text_input = blocking_input([''])
        if text_input == '':
            break
    return text_input


def show_next_turn():
    """Returns who will move next in the battle queue"""
    battle_next_turn = Battle.battle_queue[0]
    print(str(battle_next_turn) + 'will move next!')


inventory: Dict = {}


# Item Class------------------------------------------------------------------------------------------------------------
class Item:
    def __init__(self,
                 name: str,
                 hp_restore: int):
        self.name = name
        self.hp_restore = hp_restore

    def use_item(self, player: Character) -> float:
        """Uses the item on a player, returning the new HP value for the player

        :param player: Player using the item
        :return: New HP value for player (Player object is NOT updated)
        """
        player.hp += min(float(self.hp_restore), player.max_hp)
        return player.hp


# Level Class-----------------------------------------------------------------------------------------------------------
class Level:
    level: int
    player: Character
    enemy: Enemy
    exp_earned: int

    def add_exp(self):
        exp_earned = enemy.exp_on_death
        for player in players:
            if player.team == 1:
                player.exp += exp_earned
            return player.exp

    def level_up(self):
        if player.exp >= player.level_exp:
            player.level += 1
            player.max_hp *= player.leveling_scale*1.0
            player.hp = player.max_hp
            player.base_mp *= player.leveling_scale*0.3
            player.mp = player.base_mp
            player.base_attack *= leveling_scale*0.45
            player.exp -= player.level_exp
            player.level_exp *= player.leveling_scale*2.0
        return player.level, player.max_hp, player.hp, player.base_mp, player.mp, player.base_attack, player.exp, \
            player.level_exp


# Character class-------------------------------------------------------------------------------------------------------
class Character:
    """All the methods a character in the game can perform"""
    def __init__(self,
                 name: str,
                 hp: float,
                 max_hp: float,
                 mp: float,
                 base_mp: float,
                 attack: float,
                 base_attack: float,
                 speed: float,
                 level: int,
                 exp: int,
                 level_exp: int,
                 leveling_scale: float,
                 exp_on_death: int,
                 team: int):

        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.mp = mp
        self.base_mp = base_mp
        self.attack = attack
        self.base_attack = base_attack
        self.speed = speed
        self.level = level
        self.team = team
        self.exp = exp
        self.level_exp = level_exp
        self.leveling_scale = leveling_scale
        self.exp_on_death = exp_on_death
        self.is_blocking = False

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

    def deal_damage(self, other_player: 'Character', multiplier: float):
        """The base method for dealing damage to an enemy player
        :param other_player: target of damage"""
        if other_player.is_alive():
            if other_player.is_blocking:
                other_player.hp -= self.base_attack * 0.5
                other_player.is_blocking = False
            else:
                other_player.hp -= self.base_attack * 1.0
            print(f'{self.name} attacked {other_player.name}')
        return other_player

    def show_next_turn(self):
        """Returns who will move next in the battle queue"""
        print(str(self.battle_queue[1]) + 'will move next!')

    def get_all_enemies(self, players: List['Character']) -> List[int]:
        return [
            index for index, player in enumerate(players)
            if player.is_alive() and not player.is_ally(self)
        ]

    def act(self, players: List):
        all_enemy_locations = self.get_all_enemies(players)
        if self.is_alive():
            if all_enemy_locations:
                targeted_index = all_enemy_locations[0]
                targeted_player = players[targeted_index]
                damaged_player = self.deal_damage(targeted_player, 1.0)
                players[targeted_index] = damaged_player

        return players


class Ally(Character):
    def __init__(self,
                 name: str,
                 hp: float,
                 max_hp: float,
                 mp: float,
                 base_mp: float,
                 attack: float,
                 base_attack: float,
                 speed: float,
                 level: int,
                 exp: int,
                 level_exp: int,
                 leveling_scale: float):
        super().__init__(name, hp, max_hp, mp, base_mp, attack, base_attack, speed, level, exp, level_exp,
                         leveling_scale, exp_on_death=0, team=1)

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
                        damaged_player = self.deal_damage(targeted_player, 1.0)
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
                 mp: float,
                 base_mp: float,
                 attack: float,
                 base_attack: float,
                 speed: float,
                 level: int,
                 exp: int,
                 exp_on_death: int,
                 level_exp: int):
        super().__init__(name,
                         hp,
                         max_hp,
                         mp,
                         base_mp,
                         attack,
                         base_attack,
                         speed,
                         level,
                         exp,
                         exp_on_death,
                         level_exp,
                         team=2)

    def act(self, players: List):
        all_enemy_locations = self.get_all_enemies(players)
        if self.is_alive():
            if all_enemy_locations:
                targeted_index = random.choice(all_enemy_locations)
                targeted_player = players[targeted_index]
                damaged_player = self.deal_damage(targeted_player, 1.0)
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
                acting_player.act(self.players)
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
    print('Anime RPG')
    print('[s]: start')
    print('[q]: quit')
    start_input = blocking_input(['s', 'q'])
    if start_input == 's':
        debugger = True
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
        PC = Ally(name=name, hp=20, max_hp=20, mp=10, base_mp=10, attack=4, base_attack=4, speed=5, level=1, exp=0,
                  level_exp=200, leveling_scale=2.0)
        anime_male = Enemy(name='Anime Male', hp=20, max_hp=20, mp=10, base_mp=10, attack=3, base_attack=3, speed=5,
                           level=1, exp=0, level_exp=200)
        battle = Battle(players=[PC, anime_male])
        battle.run()
        potion = Item(name='potion', hp_restore=10)
        print('You found a potion.')
        inventory[potion.name] = potion
        aqua = Ally(name='Aqua', hp=22, max_hp=22, mp=10, base_mp=10, attack=6, base_attack=6, speed=5, level=2, exp=0,
                    level_exp=400)
        krillin = Enemy(name='Krillin', hp=20, max_hp=20, mp=10, base_mp=10, attack=3, base_attack=3, speed=4,
                        level=2, exp=0, level_exp=200)
        yamcha = Enemy(name='Yamcha', hp=21, max_hp=21, mp=10, base_mp=10, attack=4, base_attack=4, speed=3,
                            level=2, exp=0, level_exp=200)
        battledbz = Battle(players=[PC, aqua, krillin, yamcha])
        battledbz.run()
        arimay = Ally(name='Arimay', hp=20, max_hp=20, attack=3, speed=6, exp=0, level_exp=200)

    elif start_input == 'q':
        print('Thank you for Playing!')
        time.sleep(3)
        sys.exit()





