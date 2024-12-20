import random
from typing import Optional, Union, List
from character import Character, Player
from coord import Coord
from random import randint
class Villain(Character):
    """
    This class' purpose is to be the blueprint of villain pieces

    """

    def __init__(self):
        """
        Calls init from parent class and passes in enum and sets to villain
        """
        super().__init__(Player.VILLAIN)

    def is_valid_move(self, from_coord: Coord, to_coord: Coord, board: List[List[Union[None, Character]]]):
        """
        This function checks if a move from villain, given board and coordinates, produces a valid move

        Parameters:
            from_coord (Coord): x and y starting coordinate
            to_coord (Coord): x and y ending coordinate
            board (list): 2d list that stores None or character

        Returns:
            True (Bool): if all conditions above face contradiction, else it returns False
        """

        if abs(from_coord.x - to_coord.x) > self.move:  # move must be checked to, not only range
            return False
        if abs(from_coord.y - to_coord.y) > self.move:  # move checks x and y coordinate separately, not together
            return False

        if not (from_coord.x == to_coord.x or from_coord.y == to_coord.y):
            return False

        if board[to_coord.x][to_coord.y] is not None:
            return False
        '''
        loop breakdown:
        from + move makes sure it doesn't account for current coordinate
        the third parameter, step, moves coordinate down or up
        '''
        if from_coord.x == to_coord.x:
            move = 1 if to_coord.y > from_coord.y else -1
            for y in range(from_coord.y + move, to_coord.y, move):
                if board[from_coord.x][y] is not None:
                    return False
        if from_coord.y == to_coord.y:
            move = 1 if to_coord.x > from_coord.x else -1
            for x in range(from_coord.x + move, to_coord.x, move):
                if board[x][from_coord.y] is not None:
                    return False
        """
        I check at the end because if checked at beginning then the 
        strict horizontal and vertical movement wouldn't be accounted for
        """
        if not super().is_valid_move(from_coord, to_coord, board):
            return False
        else:
            return True


    def is_valid_attack(self, from_coord: Coord, to_coord: Coord, board: List[List[Union[None, Character]]]):
        """
        Utilizes parent's is_valid_attack() and checks if villain makes good attack

        Returns:
            True (Bool): if all conditions from parent face contradiction, else False
        """
        if not super().is_valid_attack(from_coord, to_coord, board):
            return False
        else:
            return True

    def calculate_dice(self, target, attack=True, lst: list = None):
        """
        Utilizes parent calculate_dice() and computes from a list representing rolls and
        returns sum of successful rolls

        Parameters:
            target (Character): character that self is attacking or defending from
            attack (Bool): Set to True by default indicating whether self attacks
            lst (list): holds dice rolls

        Returns:
            successful rolls from attack or defense
        """
        return super().calculate_dice(target, attack, lst)

    def deal_damage(self, target: Character, damage: int):
        super().deal_damage(target, damage)


class Goblin(Villain):
    """
    This utilizes parent init and adds piece to game and updates health, temp_health,
    and combat
    """
    def __init__(self):
        super().__init__()
        self.health = 3
        self.temp_health = 3
        self.combat = [2, 2]


class Skeleton(Villain):
    """
        This utilizes parent init and adds piece to game and updates health, temp_health,
        combat, and move
        """
    def __init__(self):
        super().__init__()
        self.health = 2
        self.temp_health = 2
        self.combat = [2, 1]   # attack is element 0 for self.combat
        self.move = 2


class Necromancer(Villain):  # not passing half health and raise_dead_valid
    """
    This villain is responsible for raising other villains from dead
    """
    def __init__(self):
        super().__init__()
        self.combat = [1, 2]  # attack is 1 and defense is 2
        self.range = 3

    def raise_dead(self, target: Character, from_coords: Coord, to_coords: Coord, board: List[List[Union[None, Character]]]):
        """
        This function chooses a target(Character) and raises them from dead given coordinates
         and board

         Parameters:
             target (Character): character that self will raise from dead
             from_coords (Coord): x and y starting coordinate
            to_coords (Coord): x and y ending coordinate
            board (list): 2d list that stores None or character

        Returns:
            Nothing if conditions aren't accurate for raising dead
        """
        if target.temp_health > 0:
            return
        '''
        not enough just to use target.range > 3 because that doesn't specify the mechanics
        calculating range is really like from(x1) and to(x2) and same for y
        '''

        if abs(from_coords.x - to_coords.x) + abs(from_coords.y - to_coords.y) > self.range:
            return  # this takes the actual range, and uses absolute value because negative range not allowed

        if target.player is not Villain:
            target.player = Player.VILLAIN  # below, if the 
        target.temp_health = target.health // 2  # floor division rounds down




class Hero(Character):
    """
    Uses the Character class to create Heroes
    """
    def __init__(self):
        '''
        initializes the Hero Class using the Player class
        '''
        super().__init__(Player.HERO)



class Warrior(Hero):
    """
    This hero is responsible for giving 2 more attack to a goblin
    """
    def __init__(self):
        super().__init__()
        self.health = 7
        self.temp_health = 7
        self.combat = [2, 4]

    def is_valid_move(self, from_coord: Coord, to_coord: Coord, board: List[List[Union[None, Character]]]) -> bool:
        '''
        Determines if the hero is making a valid move
        :param from_coord:
        :param to_coord:
        :param board:
        :return: True or False
        '''
        if super().is_valid_move(from_coord, to_coord, board):
            if (from_coord.x == to_coord.x) or (from_coord.y == to_coord.y):
                return True
        else:
            return False

    def is_valid_attack(self, from_coord: Coord, to_coord: Coord, board: List[List[Union[None, Character]]]) -> bool:
        '''
        Determines if the hero is making a valid attack
        :param from_coord:
        :param to_coord:
        :param board:
        :return: True or False
        '''
        if super().is_valid_attack(from_coord, to_coord, board):
            return True
        else:
            return False

    def calculate_dice(self, attack=True, lst: list = None, gob: list = None):
        '''
        Calls calculate dice for use in the Hero class
        :param attack:
        :param lst:
        :param gob:
        :return:  None
        '''
        super().calculate_dice(attack, lst)

    def deal_damage(self, target: Character, damage: int):
        '''
        Deals damage to a target
        :param target:
        :param damage:
        :return: None
        '''
        super().deal_damage(target, damage)
    def calculate_dice(self, target: Character, attack=True, lst: list = None, gob: list = None):
        """
        This function computes from 2 list representing rolls and
        returns sum of successful rolls. Gob is used only if target is Goblin

        Parameters:
            target (Character): character that self is attacking or defending from
            attack (Bool): indicates if self is attacking
            lst (list): holds dice rolls
            gob (list): holds dice rolls for goblin

        Returns:
            succ_sum (int): successful rolls for attack
        """

        if attack:  # means self is attacking the target
            succ_sum = 0
            if isinstance(target, Goblin):
                '''
                This adds 2 additional attack by adding it to the super().calculate_dice()
                first, check if gob list has dice rolls, succ_sum gets added a 1 when roll > 4
                if gob is none, then roll 2 additional dice by using random integers 1-6
                '''
                if gob is not None:  # checking if gob list has length greater than 0
                    for r in gob:
                        if r > 4:
                            succ_sum += 1
                else:
                    additional = [randint(1, 6) for _ in range(2)]  # generates length 2 list
                    for r in additional:
                        if r > 4:
                            succ_sum += 1

                return succ_sum + super().calculate_dice(target, attack, lst)
            else:
                return super().calculate_dice(target, attack, lst)  # this is just normal attack logic, without it being goblin

        else:  # it should call to parent function and go straight to the defend logic
            return super().calculate_dice(target, attack, lst)



class Mage(Hero):
    '''
    A Subclass of Hero with its unique stats
    '''
    def __init__(self):
        '''
        initializes the Mage Class and sets the stats
        '''
        super().__init__()
        self.attack = 2
        self.defense = 2
        self.range = 3
        self.move = 2

    def deal_damage(self, target: Character, damage: int):
        '''
        Deals damage increased by 1
        :param target:
        :param damage:
        :return: A string showing how much damage is dealt
        '''
        super().deal_damage(target, damage + 1)


class Paladin(Hero):
    '''
    A subclass of hero with unique stats
    '''
    def __init__(self):
        '''
        initializes the Paladin Class and sets the stats
        '''
        super().__init__()
        self.__heal = True
        self.health = 6
        self.temp_health = 6

    @property
    def heal(self):
        '''
        Returns self.heal
        :return:
        '''
        return self.__heal

    @heal.setter
    def heal(self, new_h):
        '''
        Sets self.heal or raises a type error
        :param new_h:
        :return:
        '''
        #raises type error if new_h is not a boolean
        if not isinstance(new_h, bool):
            raise TypeError
        else:
            self.__heal = new_h

    def revive(self, target: Character, from_coord: Coord, to_coord: Coord, board: List[List[Union[None, Character]]]):
        '''
        Revives a dead target that is an ally
        :param target:
        :param from_coord:
        :param to_coord:
        :param board:
        :return: None
        '''
        if self.__heal is False:
            return
        if board[to_coord.x][to_coord.y] != target:
            return
        if abs(from_coord.x - to_coord.x) + abs(from_coord.y - to_coord.y) > self.range:
            return
        else:
            target.temp_health = target.health // 2
            self.__heal = False

class Ranger(Hero):
    '''
    A subclass of Ranger with its unique stats
    '''

    def __init__(self):
        '''
        initializes the Ranger class and sets its stats
        '''
        super().__init__()
        self.range = 3

    def deal_damage(self, target: Character, damage: int):
        '''
        deals damage to enemies
        :param target:
        :param damage:
        :return: None
        '''
        # deals less damage to Skeletons
        if isinstance(target, Skeleton):
            target.temp_health -= (damage - 1)
            print(f'{target} was dealt {damage - 1} damage')
        else:
            target.temp_health -= damage
            print(f'{target} was dealt {damage} damage')
        # avoids negative temp healths
        if damage < 0:
            target.temp_health = 0
