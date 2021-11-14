import cards

class Player:
  def __init__(self, name, score = 0):
    self.name = name
    self._hand = cards.CardDeck(name = f"{self.name}'s Hand")
    self._score = score

  def __repr__(self):
    return(f"Player: {self.name}\n{self._hand}")

  def draw_from(self, deck):
    self._hand.add_card(deck.draw())

  def play_from_hand(self, index):
    return(self._hand.play(index))

class PlayerGroup:
  def __init__(self, players, first_player = 0):
    self._players = list(map(lambda x: Player(x), players))
    self._first_player = 0
    if 0 <= first_player and first_player < len(self._players):
      self._first_player = first_player
    else:
      raise PlayerGroup.OutOfRange(f"{first_player} is not a valid index for first player; must be between zero and {len(self._players) -1}.")
    self._index = -1

  def __repr__(self):
    return_string = []
    for i in range(len(self._players)):
      return_string.append(f"{i}: {self._players[i].name}")
    return("\n".join(return_string))

  def __iter__(self):
    return self

  def __next__(self):
    self._index += 1
    if self._index >= len(self._players):
      self._index = -1
      raise StopIteration
    else:
      return self._players[self._index]

  def deal_cards_from(self, deck, hand_size):
    for i in range(hand_size):
      for player in self._players:
        player.draw_from(deck)

  class OutOfRange(Exception):
    def __init__(self, message):
      self.message = message
  
    def __str__(self):
      return(self.message)