from __future__ import annotations
from creatures import Villain
from coord import Coord
from typing import Optional, Union, List
from coord import Coord
from character import Player
from character import Character

from creatures import Villain, Goblin, Skeleton, Necromancer
from creatures import Hero, Warrior, Mage, Paladin, Ranger
from random import randint


class Dungeon:
    def __init__(self, height: int, width: int, villains: List[Villain] = []):
        if not (4 <= height <= 12):
            raise ValueError
        if not (4 <= width <= 12):
            raise ValueError

        self.__height = height
        self.__width = width
        self.__heroes = [Warrior(), Mage(), Paladin(), Ranger()]
        self.__board = [[None for _ in range(width)] for _ in range(height)]
        self.__player = Player.HERO
        if len(villains) > 0:
            self.villains = villains
        else:
            self.generate_villains()

    @property
    def height(self):
        return self.__height

    @property
    def width(self):
        return self.__width

    @property
    def board(self):
        return self.__board

    @board.setter
    def board(self, board: List[List[Union[None, Character]]]):
        if not isinstance(board, list):
            if len(board) != self.__width or len(board) != self.__height:
                raise ValueError
        else:
            raise TypeError
        self.__board = board

    @property
    def player(self):
        return self.__player

    @property
    def heroes(self):
        return self.__heroes

    @heroes.setter
    def heroes(self, h):
        if not isinstance(h, list):
            for i in h:
                if not isinstance(i, Hero):
                    raise TypeError
            self.__heroes = h
        else:
            raise TypeError

    @property
    def villains(self):
        return self.__villains

    @villains.setter
    def villains(self, v):
        if isinstance(v, list):
            for i in v:
                if not isinstance(i, Villain):
                    raise TypeError
            if len(v) > 0:
                self.__villains = v
        else:
            raise TypeError

    def generate_villains(self):
        """
        This function generates villains for current list of villains if empty
        """
        villains = randint(1, max(self.height, self.width))
        v_lst = []
        necromancer = False

        for _ in range(villains):  # randomly generated number of villains
            val = randint(1, 10)
            if val in range(1, 6):  # 50% chance of selection
                v_lst.append(Goblin())
            elif val in range(6, 9):  # 30% chance of selection
                v_lst.append(Skeleton())
            elif val in range(9, 11) and necromancer is False:
                v_lst.append(Necromancer())  # 20% chance of selection
                necromancer = True
            elif val in range(9, 11) and necromancer is True:
                v_lst.append(Skeleton())
        self.villains = v_lst

    def is_valid_move(self, coords: List[Coord]) -> bool:
        '''
                Determines if the move the player is trying to make is valid
                :param coords:
                :return: True or False
                '''
        # if the length of coords is less than 2 returns false
        if len(coords) < 2:
            return False

        from_coord = coords[0]
        to_coord = coords[1]

        # prevents starting off the board
        if not (0 <= from_coord.x < self.height) or not (0 <= from_coord.y < self.width):
            return False
        # prevents landing off the board
        if not (0 <= to_coord.x < self.height) or not (0 <= to_coord.y < self.width):
            return False
        # prevents moving to the same spot you're already at
        if (from_coord.x == to_coord.x) and (from_coord.y == to_coord.y):
            return False
        # Prevents moving when your character is not at its spot
        if self.character_at(from_coord.x, from_coord.y) != self:
            return False
        # prevents moving through obstacles
        if self.character_at(to_coord.x, to_coord.y) is not None:
            return False
        else:
            return True

    def is_valid_attack(self, coords: List[Coord]) -> bool:
        """
        Determines if the attack is valid using coordinates
        :param coords:
        :return: True or False
        """
        # if length of coords is less than 2 returns false
        if len(coords) < 2:
            return False

        from_coord = coords[0]
        to_coord = coords[1]

        # prevents attacking from off the board
        if not (0 <= from_coord.x < self.height) or not (0 <= from_coord.y < self.width):
            return False
        # prevents attacking something off the board
        if not (0 <= to_coord.x < self.height) or not (0 <= to_coord.y < self.width):
            return False
        # Prevents attacking the same position your already in
        if (from_coord.x == to_coord.x) and (from_coord.y == to_coord.y):
            return False
        # prevents attacking when there is no character at the attackers position
        if self.character_at(from_coord.x, from_coord.y) is None:
            return False
        # prevents attacking when your character is
        if self.character_at(to_coord.x, to_coord.y) is None:
            return False
        else:
            return True

    def character_at(self, x: int, y: int):
        """
        if given valid coordinates, returns character at coordinates

        Returns:
            self.board[x][y] (Character or None): None if character isn't there

        Raises:
            ValueError: if x or y isn't within range between 0 and height/width
        """
        if not (0 <= x < self.height) or not (0 <= y < self.width):
            raise ValueError

        return self.board[x][y]


    def set_character_at(self, target: Character, x: int, y: int):
        """
        if given valid coordinates, this sets character at x and y coordinates
        on board

        Raises:
            ValueError: if x or y isn't within range between 0 and height/width
        """
        if not (0 <= x < self.height) or not (0 <= y < self.width):
            raise ValueError

        self.board[x][y] = target

    def move(self, from_coord: Coord, to_coord: Coord):
        """
        Moves value stored at beginning coordinate and places
        it at ending coordinate
       """

        if self.is_valid_move([from_coord, to_coord]):  # move must be valid
            self.board[to_coord.x][to_coord.y] = self.board[from_coord.x][from_coord.y]
            self.board[from_coord.x][from_coord.y] = None  # setting it to None symbolizes it being moved

    def set_next_player(self):
        """
        Sets current player to its opposite
        """
        if self.__player == Player.HERO:
            self.__player = Player.VILLAIN
        else:
            self.__player = Player.HERO

    def attack(self, from_coord: Coord, to_coord: Coord):
        """
        Checks to see the from_coords and to_coords produce a valid attack.
         If so, it calculates and deals damage to the Character at the location of the to_coords

        Parameters:
            from_coord (Coord): x and y starting coordinate
            to_coord (Coord): x and y ending coordinate

        Raises:
            TypeError: if value at from or to coordinate is not a character
        """
        if not self.is_valid_attack([from_coord, to_coord]):
            return
        else:
            atk = self.character_at(from_coord.x, from_coord.y)
            defd = self.character_at(to_coord.x, to_coord.y)
            if isinstance(atk, Character) and isinstance(defd, Character):
                atk_result = atk.calculate_dice(defd, True)
                defd_result = defd.calculate_dice(atk, False)
                damage = atk_result - defd_result
                if damage > 0:
                    atk.deal_damage(defd, damage)
                else:
                    print(f'{defd} to no damage from {atk}')
            else:
                raise TypeError

    def place_heroes(self):
        """
        This function places heroes on board in order and does so
        on board being even or odd length
        """
        if len(self.__board) % 2 == 0:  # checking if length of board is even
            length = len(self.__board)
            self.set_character_at(Warrior(), length-2, (length//2)-1)
            self.set_character_at(Mage(), length-1, (length//2)-1)
            self.set_character_at(Paladin(), length-2, (length//2))
            self.set_character_at(Ranger(), length-1, (length//2))
        else:
            length = len(self.__board)  # if length of board is odd
            self.set_character_at(Warrior(), length-2, length//2)
            self.set_character_at(Mage(), length-1, length//2)
            self.set_character_at(Paladin(), length-2, (length//2)+1)
            self.set_character_at(Ranger(), length-1, (length//2)+1)

    def place_villains(self):
        """
        Randomly places all the villains on the board without
        the exception of the bottom two rows.
        """
        for v in self.__villains:
            x = randint(1, len(self.__villains))
            y = randint(1, len(self.__villains))
            self.set_character_at(v, x, y)  # setting each villain, v, at random coordinates, x and y



    def print_board(self):
        st = ' \t'
        st += '_____' * len(self.board)
        st += '\n'
        for i in range(len(self.__board)):
            st += f'{i}\t'
            for j in range(len(self.__board[i])):
                if self.board[i][j] is None:
                    st += '|___|'
                else:
                    st += f'|{self.board[i][j].__class__.__name__[:3]}|'
            st += '\n'
        st += '\t'
        for i in range(len(self.board[0])):
            st += f'  {i}  '
        print(st)

    def is_dungeon_clear(self):
        '''
        Returns true if the dungeon is clear,  false if it is not.
        :return: True or False
        '''
        for i in self.__villains:
            if not i.temp_health <= 0:
                return False
        return True

    def generate_new_board(self, height: int = -1, width: int = -1):
        """
        Makes new board based on new height and width but dungeon
        must be clear in order to do so

        Parameters:
            height (int): new height that current height gets set to
            width (int): new width that current width gets set to
        """
        if not self.is_dungeon_clear():
            return

        if height is None and width is None:  # if no values for height and width are given
            height = randint(4, 12)
            width = randint(4, 12)
            self.board = [[None for _ in range(width)] for _ in range(height)]
            self.generate_villains()
            self.place_heroes()
            self.place_villains()

        else:
            self.board = [[None for _ in range(width)] for _ in range(height)]
            self.generate_villains()
            self.place_heroes()
            self.place_villains()

    def adventurer_defeat(self):
        """
        Returns true if the heroes are all dead, false if they are not
        :return: True or False
        """
        for hero in self.__heroes:
            if hero.temp_health <= 0:
                return True
            else:
                return False