from dataclasses import dataclass, field
from queue import PriorityQueue
from typing import List, Tuple, Dict
import random
import time
import sys
import copy


def blocking_input(acceptable_responses: [str]):
    """Returns input('>') until an acceptable response is inputted
    :param acceptable_responses: a list of strings that when inputted will get the go-ahead"""
    while True:
        output = input('>')
        if output in acceptable_responses:
            break
    return output


def dialogue_input():
    """Returns blocking_input(['']) until only the enter key is pressed"""
    text_input = None
    while text_input is None:
        text_input = blocking_input([''])
        if text_input == '':
            break


class Character:
    """The character class as a base"""
    def __init__(self,
                 name: str,
                 hp: float,
                 base_hp: float,
                 mp: float,
                 base_mp: float,
                 attack: float,
                 base_attack: float,
                 speed: float,
                 element: str,
                 level: int,
                 exp: int,
                 base_exp: int,
                 team: int):
        """:param name: The name of the character
        :param: hp: The health points of the character
        :param base_hp: The maximum hp a character can have at the current level
        :param mp: The magic points of the character
        :param base_mp: The maximum magic points a character can have at the current level
        :param attack: The attack value of the player, (affects the damage output
        :param base_attack: default non-buffed, non-nerfed attack value
        :param speed: The speed of the character
        :param element: The type of character
        :param level: the value of the character's level, (Eventually 1-100)
        :param exp: the value of experience points taken towards the next level
        :param base_exp: The value of the experience points needed to reach the next level
        :param team: The value that determines if a character is an ally or an enemy"""
        self.name = name
        self.hp = hp
        self.base_hp = base_hp
        self.mp = mp
        self.base_mp = base_mp
        self.attack = attack
        self.base_attack = base_attack
        self.speed = speed
        self.element = element
        self.level = level
        self.exp = exp
        self.base_exp = base_exp
        self.team = team

    def is_alive(self) -> bool:
        """Returns true if the player is alive
        player is alive if it has more than 0 hp"""
        return self.hp > 0

    def is_ally(self, other_player) -> bool:
        """Returns true if the other player is an ally to oneself
        :param other_player: the Character that is_ally is comparing to"""
        return other_player.team == self.team

    def deal_damage(self, other_player):
        """Deals damage to an other player (will eventually be healing as well)
        :param other_player: The character receiving the damage"""
        if other_player.is_alive:
            other_player.hp -= self.attack
            return other_player

    def get_all_enemy_indices(self, players: List['Character']) -> List[int]:
        """Returns the locations of all the enemy characters in a list
        :param players: The Characters within the list of enemies"""
        return [
            index for index, player in enumerate(players)
            if player.is_alive and not player.is_ally(self)]

    def act(self, players: List):
        """The method of doing something, IE. an attack"""
        all_enemy_locations = self.get_all_enemy_indices(players)
        if all_enemy_locations:
            targeted_index = all_enemy_locations[0]
            targeted_player = players[targeted_index]
            damaged_player = self.deal_damage(targeted_player)
            players[targeted_index] = damaged_player
        return players


class Move:
    """Handles the priority queue and prevents players from getting confused about who goes first"""
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






























































