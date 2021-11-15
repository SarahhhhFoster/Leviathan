import cards
import players
from itertools import repeat
import random

random.seed()

# Welcome to Leviathan. A number of prominent occult figures have
# recently been invited to Leviathan House to oversee a divination of
# the fate of the accursed place.

# Divination cards are drawn at the start of the round to decide what
# the round's outcome should be.

divination_deck = cards.CardDeck(
  list(repeat(["The Scholar", "Give two times the power level in points to the terminal player.", "The Fool", "Take two times the power level in points from the terminal player."], 5)) +
  list(repeat(["The Baron", "Give the power level in points to adjacent players.", "The Pauper", "Take the power level in points from adjacent players."], 5)) +
  list(repeat([
    "Castor", "Give the power level in points to the player to the left from the terminal player, and take that number from the player to the right.",
    "Pollux", "Take the power level in points from the player to the left from the terminal player, and give that number to the player to the right."], 5)) +
  list(repeat([
    "The Gambler", "Flip a coin. If it's heads, give twice the power level in points to the terminal player. If tails, give the power level to each adjacent.",
    "Fate", "The terminating player must choose another player, then flip a coin. The total points change is double the power level, and the other player gains or loses points on heads or tails respectively."], 5)) +
  list(repeat(["Waxing Crescent", "All players but the terminal player gain a point.", "Waning Gibbous", "All players but the terminal player lose a point."], 5)),
  name = "Divination Deck")
divination_deck.shuffle()

# Players should be able to, as professional powers:
# * Add to power
# * Subtract from power
# * Reverse direction
# * Flip the divination
# * End round

class_deck = cards.CardDeck(
  list(repeat(["The Numerologist", "The numerologist can increase or decrease the power of a divination by one point.", {"can": ["powerup", "powerdown"]}], 5)) +
  list(repeat(["The Palmist", "The palm reader can increase the power of a divination by one point or reverse the direction of play.", {"can": ["powerup", "reverse"]}], 5)) +
  list(repeat(["The Clairvoyant", "The clairvoyant can increase the power of a divination by one point or reverse the divination card.", {"can": ["powerup", "flip"]}], 5)) +
  list(repeat(["The Personage", "The personage can increase the power of a divination by one point or end the divination round.", {"can": ["powerup", "end"]}], 5)) +
  list(repeat(["The Thelemite", "The thelemite can decrease the power of a divination by one point or reverse the direction of play.", {"can": ["powerdown", "reverse"]}], 5)) +
  list(repeat(["The Haruspex", "The haruspex can decrease the power of a divination by one point or reverse the divination card.", {"can": ["powerdown", "flip"]}], 5)) +
  list(repeat(["The Exorcist", "The exorcist can decrease the power of a divination by one point or end the divination round.", {"can": ["powerdown", "end"]}], 5)) +
  list(repeat(["The Theosophist", "The theosophist can reverse the direction of play or reverse the divination card.", {"can": ["reverse", "flip"]}], 5)) +
  list(repeat(["The Thaumaturge", "The thaumaturge can reverse the direction of play or end the divination round.", {"can": ["reverse", "end"]}], 5)) +
  list(repeat(["The Demonologist", "The demonologist can reverse the divination card or end the divination round.", {"can": ["flip", "end"]}], 5)),
  name = "Profession Deck")
class_deck.shuffle()

demo_group = players.PlayerGroup(["Sarah", "Jaala", "Kirstin", "Jessica"], default_decks = {"profession": cards.CardDeck(name="Profession")})
demo_group.deal_cards_from(class_deck, 1, "profession")

current_card = divination_deck.draw()
if(random.randint(0,1)):
  current_card.flip()

print(demo_group, "\n")
for person in demo_group:
  print(person)
print(current_card)
