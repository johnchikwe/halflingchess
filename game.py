from __future__ import annotations
import os
from typing import List, Optional
from dungeon import *
from creatures import *
from coord import *


class Game:

    def __init__(self):
        self.dungeon = Dungeon(8, 8, [])
        self.rooms_cleared = 0
        self.moves = 0
        self.atk = 0
        self.selected = None

    def setup(self):
        self.dungeon.place_heroes()
        self.dungeon.place_villains()

    def play(self):
        while not self.dungeon.is_dungeon_clear() or not self.dungeon.adventurer_defeat():
            clear()
            self.print_display()
            self.select()

            while self.atk <= 1 and self.moves < 2:
                x = self.action()
                print(x)
                if x is None:
                    clear()
                    self.print_display()
                    continue
                elif x:
                    print('Next Turn')
                    break
                else:
                    print('Try again!')
                clear()
                self.print_display()
            self.selected = None
            self.end_turn()

    def attack(self):
        l = input('Please enter the coordinate you wish to attack: ')
        loc = [int(i) for i in l.split()]
        to = Coord(loc[0], loc[1])
        s = self.find_character(self.selected)
        start = Coord(s[0], s[1])
        self.dungeon.attack(start, to)
        self.atk += 1

    def move(self):
        print('in move')
        co = self.find_character(self.selected)
        mv = [Coord(co[0], co[1])]
        q = ''
        if isinstance(self.selected, Hero):

            while len(mv) < self.selected.move or q != 'q':
                try:
                    q = input('Select a coordinate (x, y): ')

                    if q == 'q':
                        break
                    l = [int(i) for i in q.split()]
                    print(l)
                    if 0 <= l[0] < self.dungeon.height and 0 <= l[0] < self.dungeon.width:
                        mv.append(Coord(l[0], l[1]))
                    else:
                        raise ValueError
                except ValueError:
                    print('Invalid coordinate, try again.')
                    continue
                except:
                    print('Something went wrong, try again')
            if self.dungeon.is_valid_move(mv):
                self.dungeon.move(mv[0], mv[-1])
                self.moves += 1
                return
        else:
            while len(mv) <= 1:
                try:
                    q = input('Select a coordinate (x, y): ')

                    if q == 'q':
                        break
                    l = [int(i) for i in q.split()]
                    print(l)
                    if 0 <= l[0] < self.dungeon.height and 0 <= l[0] < self.dungeon.width:
                        mv.append(Coord(l[0], l[1]))
                    else:
                        raise ValueError
                except ValueError:
                    print('Invalid coordinate, try again.')
                    continue
                except:
                    print('Something went wrong, try again')
                    continue
            if self.dungeon.is_valid_move(mv):
                self.dungeon.move(mv[0], mv[-1])
                self.moves += 1

    def raise_dead(self):
        co = self.find_character(self.selected)
        coords = [Coord(co[0], co[1])]
        loc = input('Please enter the coordinates you wish to attack: ')
        end = [int(i) for i in loc.split()]
        coords.append(Coord(end[0], end[1]))
        if isinstance(self.dungeon.board[coords[0].x][coords[0].y], Necromancer):
            if self.dungeon.is_valid_attack(coords):
                self.dungeon.board[coords[0].x][coords[0].y].raise_dead(
                    self.board[coords[1].x][coords[1].y])
                self.attack += 1

    def heal(self):
        co = self.find_character(self.selected)
        coords = [Coord(co[0], co[1])]
        loc = input('Please enter the coordinates you wish to attack: ')
        end = [int(i) for i in loc.split()]
        coords.append(Coord(end[0], end[1]))
        if isinstance(self.dungeon.board[coords[0].x][coords[0].y], Paladin):
            if self.dungeon.is_valid_attack(coords):
                self.dungeon.board[coords[0].x][coords[0].y].heal(
                    self.board[coords[1].x][coords[1].y])
                self.attack += 1

    def find_character(self, char: Character):
        for i in range(len(self.dungeon.board)):
            if char in self.dungeon.board[i]:
                return (i, self.dungeon.board[i].index(char))

    def select(self):
        coords = input(
            f'Please select two numbers 0-{self.dungeon.height-1} and 0-{self.dungeon.width-1} to select your piece: ')
        coords = coords.split()
        x, y = [int(i) for i in coords]
        self.selected = self.dungeon.board[x][y]
        while self.selected == None:
            coords = input(
                f'Please select two numbers 0-{self.dungeon.height-1} and 0-{self.dungeon.width-1} to select your piece: ')
            coords = coords.split()
            x, y = [int(i) for i in coords]
            self.selected = self.dungeon.board[x][y]
        print(f'{self.selected.__class__.__name__} has been selected')

    def action(self):
        print('Please select one of the following actions:')
        lst = ['attack', 'move']
        print('\t1. Move\n\t2. Attack', end='')
        if isinstance(self.selected, Necromancer):
            print('\n\t3. Raise Dead\n\t4. End Turn')
            lst.append('raise dead')
        elif isinstance(self.selected, Paladin):
            print('\n\t3. Heal\n\t4. End Turn')
            lst.append('heal')
        else:
            print('\n\t3. End Turn')

        lst.append('end turn')
        selection = input()
        return self.choices(selection, lst)

    def end_turn(self):
        self.moves = 0
        self.attack = 0
        self.dungeon.set_next_player()

    def choices(self, st, lst):
        if st.lower() in lst:
            if st == 'move' and self.moves <= 1:
                self.move()
                return None
            elif st.lower() == 'attack' and self.atk < 1:
                self.attack()
                return None
            elif st.lower() == 'end turn':
                return True
            elif st.lower() == 'heal' and self.atk < 1:
                self.heal()
                return None
            elif st.lower() == 'raise dead' and self.atk < 1:
                self.raise_dead()
                return None
            else:
                return False

    def print_display(self):
        print('=====================Villains======================')

        for v in self.dungeon.villains:
            print(
                f'{v.__class__.__name__:<12}{v.temp_health}/{v.health} HP\tLOC -> {self.find_character(v)}')
        print('---------------------------------------------------')
        self.dungeon.print_board()
        print('===================Heroes==========================')
        for h in self.dungeon.heroes:
            print(
                f'{h.__class__.__name__:<12}{h.temp_health}/{h.health} HP\tLOC -> {self.find_character(h)}')
        print('---------------------------------------------------')
        print(f'{self.dungeon.player.name}\'s turn')


def clear():
    command = ('cls' if os.name == 'nt' else 'clear')
    os.system(command)


if __name__ == "__main__":

    g = Game()
    g.setup()
    g.play()
