import random

class Card:
    def __init__(self, number):
        if 3 <= number <= 50:
            self.number = number
        else:
            raise ValueError(f'Wrong number{number}')

    def __repr__(self):
        return f'{self.number}'

# print(repr(Card(30)))

class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for n in range(3, 51):
            self.cards.append(Card(n))

    def __repr__(self):
        all_numbers = [str(card) for card in self.cards]
        ten = [str(card) for card in self.cards[-10:]]
        remaining = [str(card) for card in self.cards[:-10]]
        random.shuffle(self.cards)
        return f'Все карты: {", ".join(all_numbers)}\nКарты,сложенные в виде пирамиды: {", ".join(ten)}\nОставшаяся колода: {", ".join(remaining)}'
# print(repr(Deck()))
