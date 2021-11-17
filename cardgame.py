#!/usr/bin/env python3
import cards
import players
from itertools import combinations
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import radiolist_dialog
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
divination_power = 0
divination_count = -1

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

def powerup(divination_power, play_group, current_card, divination_count, spirit_deck):
  divination_power += 1

def powerdown(divination_power, play_group, current_card, divination_count, spirit_deck):
  divination_power -= 1

def reverse(divination_power, play_group, current_card, divination_count, spirit_deck):
  play_group.change_direction()

def flip(divination_power, play_group, current_card, divination_count, spirit_deck):
  current_card.flip()

def setcount(divination_power, play_group, current_card, divination_count, spirit_deck):
  if divination_count < 0:
    divination_count = play_group.get_player_count()

def addcount(divination_power, play_group, current_card, divination_count, spirit_deck):
  if divination_count > 0:
    divination_count += 1

def subcount(divination_power, play_group, current_card, divination_count, spirit_deck):
  if divination_count > 0:
    divination_count -= 1

def summon(divination_power, play_group, current_card, divination_count, spirit_deck):
  drawn_spirit = spirit_deck.draw()
  print(drawn_spirit)
  spirit_deck_list[drawn_spirit.name]['function'](divination_power, play_group, current_card, divination_count, spirit_deck)

power_descriptions = {
  "powerup": {
    "name": "increase power",
    "long_desc": "add one point to the power of the current divination",
    "function": powerup
  },
  "powerdown": {
    "name": "decrease power",
    "long_desc": "remove one point from the power of the current divination",
    "function": powerdown
  },
  "reverse": {
    "name": "reverse play",
    "long_desc": "reverse the direction of turn-passing play",
    "function": reverse
  },
  "flip": {
    "name": "reverse divination",
    "long_desc": "flip the divination card to reverse its nature",
    "function": flip
  },
  "setcount": {
    "name": "set the countdown",
    "long_desc": "set the divination countdown to the current number of players",
    "function": setcount
  },
  "summon": {
    "name": "summon a spirit",
    "long_desc": "play a card from the spirit deck",
    "function": summon
  }
}

# This generates a list of all combinations of powers taken two at a
# time, then I map each combination to a named profession below that. If
# I missed any combination this will error out, which is good and fine.

power_combinations = list(map(
  lambda y: "-".join(y), list(combinations(power_descriptions.keys(), 2))))

powers_professions = {
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

professions_powers = {}
for k, v in powers_professions.items():
  professions_powers[v.lower()] = list(k.split("-"))

# This takes the above descriptors and converts them into longer-form
# card descriptions

class_repeats = 2
profession_deck_list = []
for profession_powers in power_combinations:
  abilities = profession_powers.split("-")
  class_name = powers_professions[profession_powers]
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

spirit_repeats = 5

spirit_deck_list = {
  "Lesser Demon": {
    "text": "If the divination countdown has started, decrease the count by one.",
    "function": addcount
  },
  "Wandering Spirit": {
    "text": "If the divination countdown has started, increase the count by one.",
    "function": subcount
  }
}

spirit_cards = []
for i in range(spirit_repeats):
  for spirit_name in spirit_deck_list.keys():
    spirit_cards.append([spirit_name, spirit_deck_list[spirit_name]['text']])

spirit_deck = cards.CardDeck(spirit_cards, name = "Spirit Deck")
spirit_deck.shuffle()

winning_score = 10

play_group = players.PlayerGroup(["Sarah", "Jaala", "Kirstin", "Jessica"], default_decks = {"profession": cards.CardDeck(name="Profession")})
play_group.deal_cards_from(profession_deck, 1, "profession")

current_card = divination_deck.draw()
if(random.randint(0,1)):
  current_card.flip()

current_player = play_group.get_current_player()
current_profession = current_player.read_from_deck(0, deck = "profession")
current_action = None
play_strings = []
for m in power_descriptions.keys():
  power_string = ""
  if m in professions_powers[current_profession.name.lower()]:
    power_string = str("\U0001F70F " + power_descriptions[m]["name"])
    play_strings.insert(0, (m, power_string))
  else:
    power_string = str("  " + power_descriptions[m]["name"])
    play_strings.append((m, power_string))

result = radiolist_dialog(
    title = f"{current_player.name} the {current_profession.name}'s Turn",
    text = "What action would you like to perform?",
    values = play_strings
).run()
print(result)
power_descriptions[result]['function'](divination_power, play_group, current_card, divination_count, spirit_deck)