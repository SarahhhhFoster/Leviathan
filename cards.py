import random

class Card:
  def __init__(self, name, description, back_name = "", back_description = "", attrs = {}):
    self.name = name
    self.description = description
    self.back_name = back_name
    self.back_description = back_description
    self._attrs = attrs

  def __repr__(self):
    return(f"{self.name}: {self.description}")

  def get_name(self):
    return(self.name)

  def get_text(self):
    return(self.description)

  def flip(self):
    temp_values = [self.name, self.description]
    self.name, self.description = self.back_name, self.back_description
    self.back_name, self.back_description = temp_values

  def get_attr(self, attr_name):
    return(self._attrs[attr_name])

  def set_attr(self, attr_name, attr_val):
    self._attrs[attr_name] = attr_val

class CardDeck:
  def __init__(self, deck_in = [], name = None):
    self._cards = []
    self._index = -1
    self.name = name
    for card in deck_in:
      if len(card) == 2:
        self._cards.append(Card(card[0], card[1]))
      elif len(card) == 3:
        self._cards.append(Card(card[0], card[1], attrs = card[2]))
      elif len(card) == 4:
        self._cards.append(Card(card[0], card[1], card[2], card[3]))
      elif len(card) == 5:
        self._cards.append(Card(card[0], card[1], card[2], card[3], attrs = card[4]))

  def __repr__(self):
    return_string = []
    if type(self.name) != type(None):
      return_string.append(f"{self.name}:")
    if len(self._cards) == 0:
      if type(self.name) != type(None):
        return_string.append("\tDeck empty")
      else:
        return_string.append("Deck empty")
    else:
      for i in range(len(self._cards)):
        if type(self.name) != type(None):
          return_string.append(f"\t{i}: {self._cards[i]}")
        else:
          return_string.append(f"{i}: {self._cards[i]}")
    return("\n".join(return_string))

  def __iter__(self):
    return CardDeckIter(deck = self)

  def shuffle(self):
    random.shuffle(self._cards)

  def draw(self):
    if len(self._cards) > 0:
      return(self._cards.pop())
    else:
      raise CardDeck.EmptyDeck("Can't draw from an empty card deck.")

  def play(self, index):
    if index < len(self._cards) and index >= 0:
      return(self._cards.pop(index))
    elif index > 0:
      raise CardDeck.OutOfRange(f"Card not available to play. Trying to access {index} but maximum is {len(self._cards) - 1}.")
    else:
      raise CardDeck.OutOfRange(f"Card not available to play. Trying to access {index} but must be greater than zero.")

  def read_card(self, index):
    if index < len(self._cards) and index >= 0:
      return(self._cards[index])
    elif index > 0:
      raise CardDeck.OutOfRange(f"Card not available to play. Trying to access {index} but maximum is {len(self._cards) - 1}.")
    else:
      raise CardDeck.OutOfRange(f"Card not available to play. Trying to access {index} but must be greater than zero.")

  def get_card_count(self):
    return(len(self._cards))

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

class CardDeckIter:
  def __init__(self, deck, start = 0):
    self._index = start
    self._card_deck = deck

  def __next__(self):
    index = self._index
    deck = self._card_deck
    self._index += 1
    if self._index > deck.get_card_count():
      self._index = 0
      raise StopIteration
    else:
      return deck.read_card(index)