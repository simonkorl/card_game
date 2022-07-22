import copy
import random


DECORS = ["C", "D", "H", "S"]

class Card:
    '''
    Card abstraction
    '''

    def __init__(self):
        self.cid = -1
        self.decor = None
        self.point = 0
        self.attack = 0
        self.attack_shield = 0
        self.defend_block = 0
        self.defend_shield = 0
        self.is_spell = False

def generate_basic_card_list():
    '''
    generate basic cards with unmodified attack and defense
    '''
    cardlist = []
    cid = 0
    for decor in DECORS:
        for point in range(1, 14):
            card = Card()
            card.cid = cid
            card.decor = decor
            card.point = point
            card.attack = point
            card.attack_shield = 14 - point
            card.defend_block = (16 - point) // 2
            card.defend_shield = point % 2
            cardlist.append(card)
            cid += 1
    return cardlist

class Deck:
    '''
    A set of cards
    '''
    def __init__(self, cardlist: list = None):
        if cardlist is None:
            cardlist = generate_basic_card_list()
        self.cardlist = cardlist
        self.cards = copy.deepcopy(cardlist)
        random.shuffle(self.cards)
        self.ss = {} # search struct

        self._build_basic_search_struct(cardlist)

    def _build_basic_search_struct(self, deck: list):
        assert len(deck) == 52
        ss = {} # search struct
        for decor in DECORS:
            decor_ss = {}
            for i in range(1, 14):
                decor_ss[i] = None
            ss[decor] = decor_ss
        # validate cardlist
        try:
            for card in deck:
                if ss[card.decor][card.point] is None:
                    ss[card.decor][card.point] = card
        except Exception:
            print("Error cardlist")
            return
        self.ss = ss
        return

    def shuffle(self, discard_pile: list = []):
        self.cards.extend(discard_pile)
        random.shuffle(self.cards)

    def add_cards(self, cards):
        self.cards.append(cards)

    def draw(self):
        return self.cards.pop()

    def find(self):
        pass

class Table:
    '''
    Handle the states of game
    '''

    def __init__(self):
        self.characters = []
        self.host = 0

class Solver:
    '''
    The Solver of battle
    '''
    def __init__(self):
        pass

    def solve(self, table):
        pass

    def solve_once(self, status: dict) -> dict:
        # status: {
        #    "display_cards": [card1, card2, card3, card4] 
        #    "card_status": [1: attacking, 2: defending, 1, 1]
        #    "alive": 4
        #    "host": 0
        # }
        damages = [0 for _ in range(4)]
        attacks = [0 for _ in range(4)]
        blocks = [0 for _ in range(4)]
        shields = [0 for _ in range(4)]
        display_cards = status["display_cards"]
        card_status = status["card_status"]
        n = status["alive"]
        def find_next(turn, status):
            n = status["alive"]
            host = status["host"]
            return (turn + host) % n
        # display phase
        for turn in range(n):
            num = find_next(turn, status)
            # display(status, num)
            # before getting attributes
            pass
            # getting attributes
            if card_status[num] == 1:
                # attacking
                attacks[num] += display_cards[num].attack
                shields[num] += display_cards[num].attack_shield
            elif card_status[num] == 2:
                # defending
                shields[num] += display_cards[num].defend_shield
                blocks[num] += display_cards[num].defend_block
            else:
                pass
            # after getting attributes
            pass
        # battle phase
        for turn in range(n):
            num = find_next(turn, status)
            if card_status[num] == 1:
                # attacking
                # attack(num, status)
                for t in range(1, n):
                    target = (t + num) % n
                    # skill check
                    # damage section
                    # physical damage
                    damage = attacks[num]
                    # attacking modify
                    if card_status[target] == 1:
                        # if both player are attacking
                        # the larget number gets higher damage
                        if attacks[num] > attacks[target]:
                            damage += 1
                        elif attacks[num] < attacks[target]:
                            damage -= 1
                    # block
                    damage -= blocks[target]
                    # shield
                    shield_damage = min(damage, shields[target])
                    damage -= shield_damage
                    shields[target] -= shield_damage
                    # life damage
                    damages[target] += damage
            elif card_status[num] == 2:
                # defending
                pass
            else:
                pass

        result = {
            "damages": damages,
            "attacks": attacks,
            "shields": shields,
            "blocks": blocks
        }
        return result

if __name__ == "__main__":
    deck = Deck()
    deck.shuffle()
    solver = Solver()
    f = open("result.txt", "w")
    for i in range(10):
        cards = [deck.draw() for _ in range(4)]
        card_status = [1 if random.random() < 0.5 else 2 for _ in range(4)]
        host = random.randint(0, 3)
        result = solver.solve_once({
            "display_cards": cards,
            "card_status": card_status,
            "host": host,
            "alive": 4
        })
        f.write(f"=======T {i}=======\n")
        f.write("player: card\tstatus\tattack\tshield\tblock\tdamage\n")
        for j in range(4):
            f.write(f"{'*' if host == j else '-'} {j}: {cards[j].decor} {cards[j].point}\t{'Atk' if card_status[j] == 1 else 'Dfs'}\t{result['attacks'][j]}\t{cards[j].attack_shield if card_status[j] == 1 else cards[j].defend_shield}\t{result['blocks'][j]}\t{result['damages'][j]}\n")
    f.close()
