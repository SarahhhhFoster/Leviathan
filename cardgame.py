#!/usr/bin/env python3
import cards
import players
import gameactions
import gameconstants
import carddecks
from prompt_toolkit import prompt
from prompt_toolkit.shortcuts import radiolist_dialog, message_dialog
import random

random.seed()

# This is where the meat of the gameplay begins.

class Divination_Props:
  def __init__(self):
    self.divination_power = 0
    self.divination_count = -1

  def change_power(self, amt):
    self.divination_power += amt

  def set_power(self, amt):
    self.divination_power = amt

  def change_count(self, amt):
    self.divination_count += amt

  def set_count(self, amt):
    self.divination_count = amt

this_divination = Divination_Props()

play_group = players.PlayerGroup(["Sarah", "Jaala", "Kirstin", "Jessica"], default_decks = {"profession": cards.CardDeck(name = "Profession")})
play_group.set_random_starting_player()
play_group.deal_cards_from(carddecks.profession_deck, 1, "profession")

current_card = carddecks.divination_deck.draw()
if(random.randint(0,1)):
  current_card.flip()

message_dialog(
  title = current_card.get_name(),
  text = f"The first divination is {current_card.get_name()}. {current_card.get_text()}"
).run()

def win_condition_met():
  for player in play_group:
    if player.get_score() >= gameconstants.winning_score:
      return(True)
    else:
      return(False)

while not win_condition_met():
  current_player = play_group.get_current_player()
  current_profession = current_player.read_from_deck(0, deck = "profession")
  current_action = None
  play_strings = []
  for m in carddecks.power_descriptions.keys():
    power_string = ""
    if m in map(lambda x: x.lower(), current_profession.get_attr("can")):
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
    carddecks.power_descriptions[choice_result]['function'](this_divination, play_group, current_card, carddecks.spirit_deck, carddecks.spirit_deck_list)
  else:
    failed_call = None
    opponent = play_group.get_player_by_name(doubt_result)
    if choice_result in carddecks.professions_powers[current_profession.name.lower()]:
      gameactions.bluff_battle(current_player, opponent)
    else:
      winner = play_group.get_player_by_name(doubt_result)
      gameactions.bluff_battle(opponent, current_player)
    gameactions.draw_new_profession(current_player, carddecks.profession_deck)

  if this_divination.divination_count == 0:
    current_card.get_attr("function")[current_card.get_name()](play_group, this_divination.divination_power)
    message_dialog(
      title = f"{current_card.get_name()} @ Power {this_divination.divination_power}",
      text = current_card.get_text()
    ).run()
    score_string_list = []
    for p in play_group:
      score_string_list.append(f"{p.name}: {p.get_score()}")
    message_dialog(
      title = "Scores",
      text = "\n".join(score_string_list)
    ).run()
    current_card = carddecks.divination_deck.draw()
    message_dialog(
      title = current_card.get_name(),
      text = f"The new divination is {current_card.get_name()}. {current_card.get_text()}"
    ).run()
    this_divination = Divination_Props()
  elif this_divination.divination_count > 0:
    this_divination.change_count(-1)
  play_group.pass_turn()