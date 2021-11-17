import cards
import players
from prompt_toolkit.shortcuts import message_dialog

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

def bluff_battle(winner, loser):
  score_delta = 2
  message_dialog(
    title="Bluff Battle",
    text=f"{winner.name} has won the bluffing battle and will get {score_delta} points.\n{loser.name} has lost and will lose {score_delta} points.").run()
  winner.add_to_score(score_delta)
  loser.add_to_score(score_delta * -1)