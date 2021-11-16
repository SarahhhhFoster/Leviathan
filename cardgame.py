#!/usr/bin/env python3
import cards
import players
from itertools import combinations
import random

random.seed()

# Welcome to Leviathan. A number of prominent occult figures have
# recently been invited to Leviathan House to oversee a divination of
# the fate of the accursed place.

# Divination cards are drawn at the start of the round to decide what
# the round's outcome should be. Each card has a front and back face,
# each of which is the inverse of the other. The goal is to try to
# predict which other players might be able to reverse that effect and
# try to force an outcome you desire. Or lie to change it yourself if
# you aren't naturally given the gift.

divination_repeats = 5

divination_deck_list = [
  ["The Scholar", "Give two times the power level in points to the terminal player.", "The Fool", "Take two times the power level in points from the terminal player."],
  ["The Baron", "Give the power level in points to adjacent players.", "The Pauper", "Take the power level in points from adjacent players."],
  [
    "Castor", "Give the power level in points to the player to the left from the terminal player, and take that number from the player to the right.",
    "Pollux", "Take the power level in points from the player to the left from the terminal player, and give that number to the player to the right."],
  [
    "The Gambler", "Flip a coin. If it's heads, give twice the power level in points to the terminal player. If tails, give the power level to each adjacent.",
    "Fate", "The terminating player must choose another player, then flip a coin. The total points change is double the power level, and the other player gains or loses points on heads or tails respectively."],
  ["Waxing Crescent", "All players but the terminal player gain a point.", "Waning Gibbous", "All players but the terminal player lose a point."]
]

divination_cards = []
for i in range(divination_repeats):
  for div_description in divination_deck_list:
    divination_cards.append(div_description)

divination_deck = cards.CardDeck(divination_cards, name = "Divination Deck")
divination_deck.shuffle()

# Players should be able to, as professional powers:
# * Add to power
# * Subtract from power
# * Reverse direction
# * Flip the divination
# * Set the divination countdown
# * Summon a spirit

# I've refactored the generation of the profession deck out a bit to
# avoid some repetition and make it a little more concise component by
# component, at the expense of it being a little harder to grok.

power_descriptions = {
  "powerup": {
    "name": "increase power",
    "long_desc": "add one point to the power of the current divination"
  },
  "powerdown": {
    "name": "decrease power",
    "long_desc": "remove one point from the power of the current divination"
  },
  "reverse": {
    "name": "reverse play",
    "long_desc": "reverse the direction of turn-passing play"
  },
  "flip": {
    "name": "reverse divination",
    "long_desc": "flip the divination card to reverse its nature"
  },
  "setcount": {
    "name": "set the countdown",
    "long_desc": "set the divination countdown to the current number of players"
  },
  "summon": {
    "name": "summon a spirit",
    "long_desc": "play a card from the spirit deck"
  }
}

# This generates a list of all combinations of powers taken two at a
# time, then I map each combination to a named profession below that. If
# I missed any combination this will error out, which is good and fine.

power_combinations = list(map(
  lambda y: "-".join(y), list(combinations(power_descriptions.keys(), 2))))

professions = {
  "powerup-powerdown": "numerologist",
  "powerup-reverse": "palmist",
  "powerup-flip": "clairvoyant",
  "powerup-setcount": "personage",
  "powerup-summon": "glossolalist",
  "powerdown-reverse": "Thelemite",
  "powerdown-flip": "haruspex",
  "powerdown-setcount": "exorcist",
  "powerdown-summon": "demonologist",
  "reverse-flip": "theosophist",
  "reverse-setcount": "thaumaturge",
  "reverse-summon": "Fortean",
  "flip-setcount": "Hermeticist",
  "flip-summon": "necromancer",
  "setcount-summon": "doomsayer"
}

# This takes the above descriptors and converts them into longer-form
# card descriptions

class_repeats = 2
profession_deck_list = []
for profession_powers in power_combinations:
  abilities = profession_powers.split("-")
  class_name = professions[profession_powers]
  prof_power_descs = list(map(lambda x: power_descriptions[x]["long_desc"], abilities))
  for i in range(class_repeats):
    profession_deck_list.append(
      [
        class_name.capitalize(),
        f"A {class_name} can {prof_power_descs[0]} or {prof_power_descs[1]}.",
        {"can": abilities}
      ]
    )
profession_deck = cards.CardDeck(profession_deck_list, name = "Profession Deck")
profession_deck.shuffle()

play_group = players.PlayerGroup(["Sarah", "Jaala", "Kirstin", "Jessica"], default_decks = {"profession": cards.CardDeck(name="Profession")})
play_group.deal_cards_from(profession_deck, 1, "profession")

current_card = divination_deck.draw()
if(random.randint(0,1)):
  current_card.flip()

for player in play_group:
  print(player)

current_player = play_group.get_current_player()
current_profession = current_player.read_from_deck(0, deck = "profession")
current_action = None

