from __future__ import annotations
from abc import ABC, abstractmethod
import random
from typing import Union, List
from enum import Enum
from coord import Coord
from random import randint



class CharacterDeath(Exception):

    def __init__(self, msg, char: Character):
        self.message = msg


class InvalidAttack(Exception):
    pass


class Player(Enum):
    VILLAIN = 0
    HERO = 1


class Character(ABC):
    """
    This abstract class' purpose is to define what attributes and functions
    will be used for its child classes, Hero and Villain

    Attributes:
        player (Player): Enum holds possibility of child being hero or villain
    """
    @abstractmethod
    def __init__(self, player: Player):
        """
        Initializes player, health, temp_health, attack, defense, move, and range

        """
        self.__player = player
        self.__health = 5  # maximum amount of health points character can have
        self.__temp_health = 5
        self.__attack = 3
        self.__defense = 3
        self.__move = 3
        self.__range = 1

    @property
    def player(self):
        """
        This property returns self.__player

        Returns:
            player (Enum): current player
        """
        return self.__player

    @player.setter
    def player(self, p):
        """
        This property sets self player to type in parameter

        Parameters:
            p (Enum): The new player that self player will be set to

        Raises:
            TypeError: If p is not an instance of enum, Player
        """
        if not isinstance(p, Player):
            raise TypeError
        else:
            self.__player = p

    @property
    def health(self):
        """
        This property return self health

        Returns:
            health (int): currently held health
        """
        return self.__health

    @health.setter
    def health(self, h):
        """
        This property sets self health to new health, h

        Parameters:
            h (int): The new  health that self health will be set to

        Raises:
            ValueError: if h is less than 0
        """
        if h >= 0:
            self.__health = h
        else:
            raise ValueError

    @property
    def temp_health(self):
        """
        This property return self temp_health

        Returns:
             temp_health (int): currently held temp_health
        """
        return self.__temp_health

    @temp_health.setter
    def temp_health(self, th):
        """
        This property sets self temp_health to new temp_health, th

        Parameters:
            th (int): The new temp_health that self will be set to

        Raises:
            CharacterDeath: if th is less than 0
            TypeError: if th isn't an int
        """
        if isinstance(th, int):
            if th < 0:
                raise CharacterDeath("Character dead", self)
            else:
                self.__temp_health = th
        else:
            raise TypeError


    @property
    def combat(self):
        """
        This property returns self attack and defense in form
        of a list

        Returns:
            lst (list): current combat, holding attack and defense

        """
        lst = [self.__attack, self.__defense]

        return lst

    @combat.setter
    def combat(self, lst: list):
        """
        This property will make sure attack and defense are set by using list

        Parameters:
            lst (list): list that self list will be set to

        Raises:
            ValueError: If index 0 or index 1 are less than 0
            TypeError: If index 0 or index 1 are not integers

        """
        if isinstance(lst[0], int) and isinstance(lst[1], int):  # attack and defense must be integers
            if lst[0] >= 0 and lst[1] >= 0:
                self.__attack = lst[0]
                self.__defense = lst[1]
            else:
                raise ValueError
        else:
            raise TypeError

    @property
    def move(self):
        """
        This property returns current move value

        Returns:
            move (int): current move value
        """
        return self.__move

    @move.setter
    def move(self, mv: int):
        """
        This property sets current move to new move, mv

        Parameters:
            mv (int): the move that current move will be set to

        Raises:
            ValueError: if mv is less than or equal to 0
            TypeError: if mv isn't an int

        """
        if isinstance(mv, int):
            if mv > 0:
                self.__move = mv
            else:
                raise ValueError
        else:
            raise TypeError

    @property
    def range(self):
        """
        This property returns current range

        Returns:
             range (int): current range value
        """
        return self.__range

    @range.setter
    def range(self, r: int):
        """
        This property sets current range to new range, r

        Parameters:
            r (int): the new range that self will be set to

        Raises:
            ValueError: if r is less than or equal to 0
            TypeError: if r is not an int

        """
        if isinstance(r, int):
            if r > 0:
                self.__range = r
            else:
                raise ValueError
        else:
            raise TypeError

    @abstractmethod
    def is_valid_move(self, from_coord: Coord, to_coord: Coord, board: List[List[Union[None, Character]]]):
        '''
        Determines if a move is valid using coordinates from the board
        :param from_coord:
        :param to_coord:
        :param board:
        :return: False or True
        '''
        if not (0 <= from_coord.x < len(board)) or not (0 <= from_coord.y < len(board)):
            return False
        if not (0 <= to_coord.x < len(board)) or not (0 <= to_coord.y < len(board)):
            return False
        if (from_coord.x == to_coord.x) and (from_coord.y == to_coord.y):
            return False
        if board[from_coord.x][from_coord.y] != self:
            return False
        if board[to_coord.x][to_coord.y] is not None:
            return False
        else:
            return True

    @abstractmethod
    def is_valid_attack(self, from_coord: Coord, to_coord: Coord, board: List[List[Union[None, Character]]]):
        """
        This function checks if a move, given board and coordinates, makes a valid attack

        Parameters:
            from_coord (Coord): x and y starting coordinate
            to_coord (Coord): x and y ending coordinate
            board (list): 2d list that stores None or character

        Returns:
            True (Bool): if all conditions above face contradiction, else it returns False

        """
        if not (0 <= from_coord.x < len(board)) or not (0 <= from_coord.y < len(board)):
            return False

        if not (0 <= to_coord.x < len(board)) or not (0 <= to_coord.y < len(board)):
            return False
        # NEED TO CHECK IF START AND END COORDS ARE DIFFERENT
        if (from_coord.x == to_coord.x) and (from_coord.y == to_coord.y):  # or makes sure to catch either x or y coordinate being different
            return False  # checking directly in parentheses avoids from_x being compared to to_y
        if board[from_coord.x][from_coord.y] != self:
            return False
        if board[to_coord.x][to_coord.y] is None:
            return False

        return True

    @abstractmethod
    def calculate_dice(self, target: Character, attack=True, lst: list = None):  # There was a problem with how I put [] in parameters
        """
        This function computes from a list representing rolls and
        returns sum of successful rolls

        Parameters:
            target (Character): character that self is attacking or defending from
            attack (Bool): indicates if self is attacking
            lst (list): holds dice rolls

        Returns:
            succ_sum (int): successful rolls for attack
            s_sum (int): successful rolls for defense
        """

        if lst is not None:
            if attack:  # means self is attacking the target
                succ_sum = 0
                for r in range(len(lst)):
                    if lst[r] > 4:
                        succ_sum += 1
                return succ_sum

            else:  # if defending
                s_sum = 0
                for r in range(len(lst)):
                    if lst[r] > 3:
                        s_sum += 1
                return s_sum
        else:
            if attack:  # means self is attacking the target
                succ_sum = 0
                atk_lst = [randint(1, 6) for _ in range(self.__attack)]
                for i in range(len(atk_lst)):
                    if atk_lst[i] > 4:
                        succ_sum += 1
                return succ_sum

            else:  # if defending
                s_sum = 0
                def_lst = [randint(1, 6) for _ in range(self.__defense)]
                for d in range(len(def_lst)):
                    if def_lst[d] > 3:
                        s_sum += 1
                return s_sum

    @abstractmethod
    def deal_damage(self, target: Character, damage: int):
        '''
        Causes the target to lose temp health
        :param target:
        :param damage:
        :return: String showing how much damage is dealt
        '''
        target.temp_health -= damage
        print(f'{target} was dealt {damage} damage')


    def __str__(self):
        """
        Returns string representation of class and player

        """
        return f'{self.__class__.__name__}(Player:{self.__player})'



