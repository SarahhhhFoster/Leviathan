#!/usr/bin/env python3
import cards
import players
import gameactions
import gameconstants
import carddecks
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import radiolist_dialog
import random

random.seed()

# Welcome to Leviathan. A number of prominent occult figures have
# recently been invited to Leviathan House to oversee a divination of
# the fate of the accursed place.

# This is where the meat of the gameplay begins.

divination_power = 0
divination_count = -1

play_group = players.PlayerGroup(["Sarah", "Jaala", "Kirstin", "Jessica"], default_decks = {"profession": cards.CardDeck(name="Profession")})
play_group.deal_cards_from(carddecks.profession_deck, 1, "profession")

current_card = carddecks.divination_deck.draw()
if(random.randint(0,1)):
  current_card.flip()

current_player = play_group.get_current_player()
current_profession = current_player.read_from_deck(0, deck = "profession")
current_action = None
play_strings = []
for m in carddecks.power_descriptions.keys():
  power_string = ""
  if m in carddecks.professions_powers[current_profession.name.lower()]:
    power_string = str("\U0001F70F " + carddecks.power_descriptions[m]["name"])
    play_strings.insert(0, (m, power_string))
  else:
    power_string = str("  " + carddecks.power_descriptions[m]["name"])
    play_strings.append((m, power_string))

choice_result = radiolist_dialog(
    title = f"{current_player.name} the {current_profession.name}'s Turn",
    text = "What action would you like to perform?",
    values = play_strings
).run()

possible_doubters = []
for p in play_group.get_player_names():
  if p != current_player.name:
    possible_doubters.append((p, p))
possible_doubters.insert(0, (None, "Nobody"))

doubt_result = radiolist_dialog(
    title = "Disbelief",
    text = f"Do any players disbelieve that {current_player.name} can {carddecks.power_descriptions[choice_result]['name']}?",
    values = possible_doubters
).run()

if doubt_result == None:
  carddecks.power_descriptions[choice_result]['function'](divination_power, play_group, current_card, divination_count, carddecks.spirit_deck, carddecks.spirit_deck_list)
else:
  failed_call = None
  opponent = play_group.get_player_by_name(doubt_result)
  if choice_result in carddecks.professions_powers[current_profession.name.lower()]:
    gameactions.bluff_battle(current_player, opponent)
  else:
    winner = play_group.get_player_by_name(doubt_result)
    gameactions.bluff_battle(opponent, current_player)

play_group.pass_turn()