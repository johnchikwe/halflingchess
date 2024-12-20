import unittest
import copy
import character
from character import Character, Player
from coord import Coord
from creatures import Villain, Goblin, Skeleton, Necromancer, Player
from creatures import Hero, Warrior, Mage, Paladin, Ranger
from dungeon import Dungeon


class CharacterTest(unittest.TestCase):  # test character class

    def test_Villain(self):  # this is going to test if the character is appropriate player
        n = Necromancer()
        self.assertEqual(n.player, Player.VILLAIN)

    def test_wrongPlayer(self):
        g = Goblin()  # goblin is a villain, therefore cannot be hero
        self.assertNotEquals(g.player, Player.HERO)

    def test_combat_attrType(self):
        s = Skeleton()
        self.assertEqual(s.combat, list(s.combat))  # combat attribute must be a list

    def test_villain_combat(self):
        n = Necromancer()
        self.assertNotEqual(n.combat, [1, 4])  # testing for right attack and defense

    def test_attackDefense(self):
        m = Mage()
        self.assertEqual(m.combat[0], m.combat[1])

    def test_characterDeath(self):
        s = Skeleton()
        with self.assertRaises(character.CharacterDeath):
            s.temp_health = -1

    def test_combat_Int(self):  # check if integers in combat
        g = Goblin()
        self.assertIsInstance(g.combat[0], int)

    def test_moveGreater(self):  # testing if move is in bounds
        w = Warrior()
        with self.assertRaises(ValueError):
            w.move = 0


    # test villain is_valid_move
    def test_villain_wrongDirection(self):
        ch = Villain()
        board = [[None for _ in range(5)] for _ in range(5)]
        fromm = Coord(0, 4)
        board[0][4] = ch
        to = Coord(1, 3)
        valid = ch.is_valid_move(fromm, to, board)
        self.assertFalse(valid)

    def test_villain_Vertical(self):
        ch = Villain()
        board = [[None for _ in range(5)] for _ in range(5)]
        fromm = Coord(0, 4)
        board[0][4] = ch
        to = Coord(0, 3)
        valid = ch.is_valid_move(fromm, to, board)
        self.assertTrue(valid)

    def test_villain_Horizontal(self):
        ch = Villain()
        board = [[None for _ in range(5)] for _ in range(5)]
        fromm = Coord(1, 0)
        board[1][0] = ch
        to = Coord(4, 0)
        valid = ch.is_valid_move(fromm, to, board)
        self.assertTrue(valid)


    def test_villainWithBlockage(self):
        s = Skeleton()
        board = [[None for _ in range(5)] for _ in range(5)]
        fromm = Coord(0, 4)
        to = Coord(0, 3)
        board[0][4] = s
        board[0][3] = Goblin()
        valid = s.is_valid_move(fromm, to, board)
        self.assertFalse(valid)

    def test_villainExceedMove(self):
        n = Necromancer()
        board = [[None for _ in range(5)] for _ in range(5)]
        fromm = Coord(0, 0)
        to = Coord(0, 4)
        board[0][0] = n
        valid = n.is_valid_move(fromm, to, board)
        self.assertFalse(valid)

    def testOutRangeFromTo(self):
        ch = Villain()
        board = [[None for _ in range(5)] for _ in range(5)]
        fromm = Coord(0, 5)
        to = Coord(1, 9)
        valid = ch.is_valid_attack(fromm, to, board)
        self.assertFalse(valid)


    def testOutRangeFrom(self):
        ch = Hero()
        board = [[None for _ in range(5)] for _ in range(5)]
        fromm = Coord(0, 9)
        to = Coord(1, 3)
        valid = ch.is_valid_attack(fromm, to, board)
        self.assertFalse(valid)

    def testInRange(self):
        ch = Hero()
        board = [[None for _ in range(5)] for _ in range(5)]
        fromm = Coord(1, 3)
        board[fromm.x][fromm.y] = Mage()
        to = Coord(1, 4)
        board[1][4] = Goblin()
        valid = ch.is_valid_attack(fromm, to, board)
        self.assertEqual(True, valid)

    def test_calculateDiceZero(self):
        v1 = Necromancer()
        h = Mage()
        attack = True
        lst = [1, 3, 2]
        dice = v1.calculate_dice(h, attack, lst)
        self.assertEqual(dice, 0)

    def test_calculateDice(self):
        v1 = Necromancer()
        h = Mage()
        attack = True
        lst = [1, 5, 5]
        dice = v1.calculate_dice(h, attack, lst)
        self.assertEqual(dice, 2)

    def test_calculateDiceEmptyList(self):
        v1 = Goblin()
        h = Mage()
        attack = True
        lst = []
        dice = v1.calculate_dice(h, attack, lst)
        self.assertEqual(dice, 0)

    def test_calculateDiceDefending(self):
        h = Ranger()
        v = Goblin()
        attack = False
        lst = [1, 2, 4]
        dice = h.calculate_dice(v, attack, lst)
        self.assertEqual(dice, 1)

    def test_calculateDiceHeroVHero(self):
        h = Ranger()
        h2 = Paladin()
        attack = False
        lst = [1, 2, 4]
        dice = h.calculate_dice(h2, attack, lst)
        self.assertEqual(dice, 1)



    def testRaiseIfDead(self):
        board = [[None for _ in range(5)] for _ in range(5)]
        v1 = Necromancer()
        v2 = Skeleton()
        v2.temp_health = 0
        fromm = Coord(0, 0)
        board[0][0] = v1
        to = Coord(1, 1)
        board[1][1] = v2
        v1.raise_dead(v2, fromm, to, board)
        self.assertEqual(v2.temp_health, v2.health//2)

    def testRaiseOutRange(self):  # if it's out of range
        board = [[None for _ in range(6)] for _ in range(6)]
        v1 = Necromancer()
        v2 = Skeleton()
        v2.temp_health = 0
        fromm = Coord(0, 0)
        board[0][0] = v1
        to = Coord(1, 1)
        board[4][4] = v2
        v1.raise_dead(v2, fromm, to, board)
        self.assertNotEquals(v2.temp_health, v2.health // 2)

    def testRaiseDeadHero(self):   # this checks for hero being switched to villain
        board = [[None for _ in range(6)] for _ in range(6)]
        v1 = Necromancer()
        v2 = Mage()
        v2.temp_health = 0
        fromm = Coord(0, 0)
        board[0][0] = v1
        to = Coord(1, 1)
        board[4][4] = v2
        v1.raise_dead(v2, fromm, to, board)
        self.assertEqual(v2.player, Player.VILLAIN)


    def test_warrior_dice(self):
        g = Goblin()
        w = Warrior()
        attack = True
        lst = [1, 5, 4]
        gob = [5, 3, 2]
        self.assertEqual(w.calculate_dice(g, attack, lst, gob), 2)

    def test_warriorDiceGobNone(self):
        g = Goblin()
        w = Warrior()
        attack = True
        lst = [3, 5, 6]
        gob = []
        self.assertEqual(w.calculate_dice(g, attack, lst, gob), 2)

    def test_warriorDiceNotGob(self):
        n = Necromancer()
        w = Warrior()
        attack = True
        lst = [2, 5]
        gob = [5, 6, 2]
        self.assertEqual(w.calculate_dice(n, attack, lst, gob), 1)

    def test_warriorDiceFalseAttack(self):
        g = Goblin()
        w = Warrior()
        attack = False
        lst = [1, 4]
        gob = []
        self.assertEqual(w.calculate_dice(g, attack, lst, gob), 1)


    def test_character_at(self):
        board = [[None for _ in range(6)] for _ in range(6)]
        v1 = Necromancer()
        d1 = Dungeon(6, 6, [])
        fromm = Coord(0, 0)
        board[fromm.x][fromm.y] = v1
        self.assertEqual(d1.character_at(fromm.x, fromm.y), v1)

    def test_attack_damage(self):

        v1 = Necromancer()
        h1 = Mage()
        d1 = Dungeon(6, 6, [])
        fromm = Coord(0, 0)
        to = Coord(1, 1)
        d1.board[fromm.x][fromm.y] = v1
        d1.board[1][1] = h1
        initial_health = copy.deepcopy(h1.temp_health)
        d1.attack(fromm, to)
        self.assertLess(h1.temp_health, initial_health)

    def test_set_char_at(self):
        v1 = Necromancer()
        d1 = Dungeon(6, 6, [])
        d1.set_character_at(v1, 2, 2)
        self.assertEqual(d1.board[2][2], v1)

    def test_empty_generateVillains(self):  # testing if this function makes villain list not empty
        d = Dungeon(6, 6, [])
        d.generate_villains()
        self.assertNotEqual(len(d.villains), 0)

    def test_generateVillainsNec(self):  # testing that self.villains doesn't have 2 necromancers
        d = Dungeon(12, 11, [])
        d.generate_villains()
        necro_count = d.villains.count(Necromancer())
        self.assertEqual(necro_count, 1)

    def test_generateVillainsGobCount(self):  # check if there are more goblins than necromancers
        d = Dungeon(12, 11, [])
        gob_count = d.villains.count(Goblin())
        necro_count = d.villains.count(Necromancer())
        self.assertGreater(gob_count, necro_count)

    def test_move_fromNone(self):  # testing if move accurately makes from_coord none
        d = Dungeon(12, 11, [])
        d.set_character_at(Necromancer(), 0, 0)
        from_c = Coord(0, 0)
        to_c = Coord(1, 1)
        d.move(from_c, to_c)
        self.assertEqual(d.board[from_c.x][from_c.y], None)

    def test_outRangeMove(self):  # testing if move is out of range
        d = Dungeon(12, 11, [])
        d.set_character_at(Necromancer(), 0, 0)
        from_c = Coord(0, 0)
        to_c = Coord(1, 20)
        self.assertRaises(IndexError, d.board[to_c.x][to_c.y])

    def test_place_heroesOdd(self):  # checking where warrior is for odd length
        d = Dungeon(9, 8, [])
        d.board = [[None for _ in range(9)] for _ in range(8)]
        d.place_heroes()
        x = len(d.board)-2
        y = len(d.board) // 2  # len(d.board) // 2
        self.assertEqual(d.board[x][y], Warrior())

    def test_place_heroesEven(self):  # checking where warrior is for even length
        d = Dungeon(4, 6, [])
        d.board = [[None for _ in range(4)] for _ in range(6)]
        d.place_heroes()
        x = len(d.board)-2
        y = (len(d.board)//2)-1
        self.assertEqual(d.board[x][y], Warrior())

    def test_Hero(self):
        w = Warrior()
        self.assertEqual(w.player, Player.HERO)

    def test_wrongPlayer(self):
        m = Mage()
        self.assertNotEqual(m.player, Player.VILLAIN)

    def test_combat_attrType(self):
        r = Ranger()
        self.assertEqual(r.combat, list(r.combat))

    def test_is_valid_attack(self):
        board = [[None for _ in range(5)] for _ in range(5)]
        r = Ranger()
        m = Mage()
        fromm = Coord((0, 0))
        e = r.is_valid_attack()
        self.assertEqual()

    def test_revive(self):
        board = [[None for _ in range(5)] for _ in range(5)]
        v1 = Paladin()
        v2 = Mage()
        v2.temp_health = 0
        fromm = Coord(0, 0)
        board[0][0] = v1
        to = Coord(1, 1)
        board[1][1] = v2
        v1.revive(v2, fromm, to, board)
        self.assertEqual(v2.temp_health, v2.health // 2)

    def testReviveOutRange(self):
        board = [[None for _ in range(6)] for _ in range(6)]
        h1 = Paladin()
        h2 = Ranger()
        h2.temp_health = 0
        fromm = Coord(0, 0)
        board[0][0] = h1
        to = Coord(1, 1)
        board[4][4] = h2
        h1.revive(h2, fromm, to, board)
        self.assertNotEqual(h2.temp_health, h2.health // 2)

    def testRaiseDeadHero(self):
        board = [[None for _ in range(6)] for _ in range(6)]
        h1 = Paladin()
        v1 = Goblin()
        v1.temp_health = 0
        fromm = Coord(0, 0)
        board[0][0] = v1
        to = Coord(1, 1)
        board[4][4] = v1
        h1.revive(v1, fromm, to, board)
        self.assertEqual(v1.player, Player.HERO)

    def test_Ranger_damage(self):
        r = Ranger()
        s = Skeleton()
        r.deal_damage(s, 4)
        self.assertEqual(s.temp_health, s.health - 3)

    def test_mage_damage(self):
        m = Mage()
        g = Goblin()
        m.deal_damage(g, 1)
        self.assertEqual(g.temp_health, g.health - 2)

    def test_is_dungeon_clear(self):
        d = Dungeon(8, 8, [Necromancer()])
        self.assertEqual(d.is_dungeon_clear(), False)









