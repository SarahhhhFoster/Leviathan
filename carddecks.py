import cards
import gameactions
import gameconstants
from itertools import combinations

# Divination cards are drawn at the start of the round to decide what
# the round's outcome should be. Each card has a front and back face,
# each of which is the inverse of the other. The goal is to try to
# predict which other players might be able to reverse that effect and
# try to force an outcome you desire. Or lie to change it yourself if
# you aren't naturally given the gift.

divination_deck_list = [
  [
    "The Scholar", "Give two times the power level in points to the terminal player.",
    "The Fool", "Take two times the power level in points from the terminal player.",
    {"function": {
      "The Scholar": gameactions.scholar,
      "The Fool": gameactions.fool
      }
    }
  ],
  [
    "The Baron", "Give the power level in points to terminus-adjacent players.",
    "The Pauper", "Take the power level in points from terminus-adjacent players.",
    {"function": {
      "The Baron": gameactions.baron,
      "The Pauper": gameactions.pauper
      }
    }
  ],
  [
    "Castor", "Give the power level in points to the player to the left from the terminal player, and take that number from the player to the right.",
    "Pollux", "Take the power level in points from the player to the left from the terminal player, and give that number to the player to the right.",
    {"function": {
      "Castor": gameactions.castor,
      "Pollux": gameactions.pollux
      }
    }
  ],
  [
    "The Gambler", "Flip a coin. If it's heads, give twice the power level in points to the terminal player. If tails, give the power level to each adjacent.",
    "Fate", "The terminating player must choose another player, then flip a coin. The total point change is double the power level, and the other player gains or loses points on heads or tails respectively.",
    {"function": {
      "The Gambler": gameactions.gambler,
      "Fate": gameactions.fate
      }
    }
  ],
  [
    "Waxing Crescent", "All players but the terminal player gain a point.",
    "Waning Gibbous", "All players but the terminal player lose a point.",
    {"function": {
      "Waxing Crescent": gameactions.waxing,
      "Waning Crescent": gameactions.waning
      }
    }
  ]
]

divination_cards = []
for i in range(gameconstants.divination_repeats):
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

power_descriptions = {
  "powerup": {
    "name": "increase power",
    "long_desc": "add one point to the power of the current divination",
    "function": gameactions.powerup
  },
  "powerdown": {
    "name": "decrease power",
    "long_desc": "remove one point from the power of the current divination",
    "function": gameactions.powerdown
  },
  "reverse": {
    "name": "reverse play",
    "long_desc": "reverse the direction of turn-passing play",
    "function": gameactions.reverse
  },
  "flip": {
    "name": "reverse divination",
    "long_desc": "flip the divination card to reverse its nature",
    "function": gameactions.flip
  },
  "setcount": {
    "name": "set the countdown",
    "long_desc": "set the divination countdown to the current number of players if it is unset",
    "function": gameactions.setcount
  },
  "summon": {
    "name": "summon a spirit",
    "long_desc": "play a card from the spirit deck",
    "function": gameactions.summon
  }
}

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

# This generates a list of all combinations of powers taken two at a
# time, then I map each combination to a named profession below that. If
# I missed any combination this will error out, which is good and fine.

power_combinations = list(map(
  lambda y: "-".join(y), list(combinations(power_descriptions.keys(), 2))))

# This takes the above descriptors and converts them into longer-form
# card descriptions

profession_deck_list = []
for profession_powers in power_combinations:
  abilities = profession_powers.split("-")
  class_name = powers_professions[profession_powers]
  prof_power_descs = list(map(lambda x: power_descriptions[x]["long_desc"], abilities))
  for i in range(gameconstants.class_repeats):
    profession_deck_list.append(
      [
        class_name.capitalize(),
        f"A {class_name} can {prof_power_descs[0]} or {prof_power_descs[1]}.",
        {"can": abilities}
      ]
    )
profession_deck = cards.CardDeck(profession_deck_list, name = "Profession Deck")
profession_deck.shuffle()

# Spirits can be summoned by a player power with unexpected effects. The
# effects aren't dissimilar to other actions and will just refer to the
# functions defined at the top.

spirit_deck_list = {
  "Poultergeist": {
    "text": "If the divination countdown has started, decrease the count by one.",
    "function": gameactions.addcount
  },
  "Wandering Spirit": {
    "text": "If the divination countdown has started, increase the count by one.",
    "function": gameactions.subcount
  },
  "Cosmic Horror": {
    "text": "Immediately end the round.",
    "function": gameactions.endcount
  },
  "Terrifying Vision": {
    "text": "Reverse the direction of play.",
    "function": gameactions.reverse
  },
  "Familiar Figure": {
    "text": "Add one point to the divination strength.",
    "function": gameactions.powerup
  },
  "Will O' Wisp": {
    "text": "Remove one point from the divination strength.",
    "function": gameactions.powerdown
  }
}

spirit_cards = []
for i in range(gameconstants.spirit_repeats):
  for spirit_name in spirit_deck_list.keys():
    spirit_cards.append([spirit_name, spirit_deck_list[spirit_name]['text']])

spirit_deck = cards.CardDeck(spirit_cards, name = "Spirit Deck")
spirit_deck.shuffle()