import copy
import cards

class Player:
  def __init__(self, name, score = 0, decks = {"hand": cards.CardDeck(name="Hand")}):
    self.name = name
    self._decks = decks
    self._score = score

  def __repr__(self):
    decks_string = '\n'.join(map(lambda x: str(x), self._decks.values()))
    return(f"Player: {self.name}\n{decks_string}")

  def draw_from(self, deck, draw_to_deck = "hand"):
    if not draw_to_deck in self._decks:
      self._decks[draw_to_deck] = cards.CardDeck(name = draw_to_deck)
    self._decks[draw_to_deck].add_card(deck.draw())

  def play_from_deck(self, index, deck = "hand"):
    return(self._decks[deck].play(index))

  def read_from_deck(self, index, deck = "hand"):
    return(self._decks[deck].read_card(index))

  def add_to_score(self, add):
    self._score += add

class PlayerGroup:
  def __init__(self, players, first_player = 0, default_decks = {"hand": cards.CardDeck(name="Hand")}):
    self._players = list(map(lambda x: Player(x, decks = copy.deepcopy(default_decks)), players))
    self._current_player = 0
    if 0 <= first_player and first_player < len(self._players):
      self._current_player = first_player
    else:
      raise PlayerGroup.OutOfRange(f"{first_player} is not a valid index for first player; must be between zero and {len(self._players) -1}.")
    self._index = -1
    self._direction = 1

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

  def __getitem__(self, item):
    return(self._players[item])

  def deal_cards_from(self, deck, hand_size, to_deck = "hand"):
    if deck.get_card_count() < (len(self._players) * hand_size):
      raise PlayerGroup.OutOfRange(f"Not enough cards in deck to deal {hand_size} cards to each player.")
    for i in range(hand_size):
      for player in self._players:
        player.draw_from(deck, draw_to_deck = to_deck)

  def get_player_count(self):
    return(len(self._players))

  def get_player_names(self):
    return(list(map(lambda x: x.name, self._players)))

  def pass_turn(self):
    if self._current_player < (len(self._players) - 1):
      self._current_player += self._direction
    else:
      self._current_player = 0

  def change_direction(self):
    self._direction *= -1

  def get_current_player(self):
    return(self._players[self._current_player])

  def get_player_by_name(self, name):
    for p in self._players:
      if p.name == name:
        return(p)

  def get_offset_player(self, offset):
    return(self._players[(self._current_player + offset) % len(self._players)])

  class OutOfRange(Exception):
    def __init__(self, message):
      self.message = message
  
    def __str__(self):
      return(self.message)