import random

class Card:
  def __init__(self, name, description, back_name = "", back_description = ""):
    self.name = name
    self.description = description
    self.back_name = back_name
    self.back_description = back_description

  def __repr__(self):
    return(f"{self.name}: {self.description}")

  def get_name(self):
    return(self.name)

  def get_text(self):
    return(self.description)

  def flip(self):
    self.name, self.description = self.back_name, self.back_description

class CardDeck:
  def __init__(self, deck_in = [], name = None):
    self._cards = []
    self._index = -1
    self.name = name
    for card in deck_in:
      if len(card) == 2:
        self._cards.append(Card(card[0], card[1]))
      elif len(card) == 4:
        self._cards.append(Card(card[0], card[1], card[2], card[3]))

  def __repr__(self):
    return_string = []
    if type(self.name) != type(None):
      return_string.append(f"{self.name}:")
    for i in range(len(self._cards)):
      if type(self.name) != type(None):
        return_string.append(f"\t{i}: {self._cards[i]}")
      else:
        return_string.append(f"{i}: {self._cards[i]}")
    return("\n".join(return_string))

  def __iter__(self):
    return self

  def __next__(self):
    self._index += 1
    if self._index >= len(self._cards):
      self._index = -1
      raise StopIteration
    else:
      return self._cards[self._index]

  def shuffle(self):
    random.shuffle(self._cards)

  def draw(self):
    if len(self._cards) > 0:
      return(self._cards.pop())
    else:
      raise CardDeck.EmptyDeck("Can't draw from an empty card deck.")

  def play(self, index):
    if index < len(self._cards) and index > 0:
      return(self._cards.pop(index))
    elif index > 0:
      raise CardDeck.OutOfRange(f"Card not available to play. Trying to access {index} but maximum is {len(self._cards) - 1}.")
    else:
      raise CardDeck.OutOfRange(f"Card not available to play. Trying to access {index} but must be greater than zero.")

  def add_card(self, card):
    self._cards.append(card)

  class EmptyDeck(Exception):
    def __init__(self, message):
      self.message = message
  
    def __str__(self):
      return(self.message)

  class OutOfRange(Exception):
    def __init__(self, message):
      self.message = message
  
    def __str__(self):
      return(self.message)