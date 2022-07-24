import cards
import players
import random
from prompt_toolkit.shortcuts import message_dialog, radiolist_dialog

def powerup(this_divination, play_group, current_card, spirit_deck, spirit_deck_list):
  this_divination.change_power(1)

def powerdown(this_divination, play_group, current_card, spirit_deck, spirit_deck_list):
  this_divination.change_power(-1)

def reverse(this_divination, play_group, current_card, spirit_deck, spirit_deck_list):
  play_group.change_direction()

def flip(this_divination, play_group, current_card, spirit_deck, spirit_deck_list):
  current_card.flip()
  message_dialog(
    title=current_card.get_name(),
    text=f"The divination is now {current_card.get_name()}. {current_card.get_text()}"
  ).run()

def setcount(this_divination, play_group, current_card, spirit_deck, spirit_deck_list):
  if this_divination.divination_count < 0:
    this_divination.set_count(play_group.get_player_count())

def addcount(this_divination, play_group, current_card, spirit_deck, spirit_deck_list):
  if this_divination.divination_count > 0:
    this_divination.change_count(1)

def subcount(this_divination, play_group, current_card, spirit_deck, spirit_deck_list):
  if this_divination.divination_count > 0:
    this_divination.change_count(-1)

def endcount(this_divination, play_group, current_card, spirit_deck, spirit_deck_list):
  if this_divination.divination_count < 0:
    this_divination.set_count(0)

def summon(this_divination, play_group, current_card, spirit_deck, spirit_deck_list):
  drawn_spirit = spirit_deck.draw()
  message_dialog(
    title=f"Summoned a {drawn_spirit.get_name()}",
    text=f"{play_group.get_current_player().name} has summoned a a {drawn_spirit.get_name()}. {drawn_spirit.get_text()}"
  ).run()
  spirit_deck_list[drawn_spirit.name]['function'](this_divination, play_group, current_card, spirit_deck, spirit_deck_list)

# "The Scholar", "Give two times the power level in points to the terminal player."
def scholar(play_group, power_level):
  # print("scholar")
  play_group.get_current_player().add_to_score(2 * power_level)

# "The Fool", "Take two times the power level in points from the terminal player."
def fool(play_group, power_level):
  # print("fool")
  play_group.get_current_player().add_to_score(-2 * power_level)

# "The Baron", "Give the power level in points to terminus-adjacent players."
def baron(play_group, power_level):
  # print("baron")
  play_group.get_offset_player(1).add_to_score(power_level)
  play_group.get_offset_player(-1).add_to_score(power_level)

# "The Pauper", "Take the power level in points from terminus-adjacent players."
def pauper(play_group, power_level):
  # print("pauper")
  play_group.get_offset_player(1).add_to_score(power_level * -1)
  play_group.get_offset_player(-1).add_to_score(power_level * -1)

# "Castor", "Give the power level in points to the player to the left from the terminal player, and take that number from the player to the right."
def castor(play_group, power_level):
  # print("castor")
  play_group.get_offset_player(1).add_to_score(power_level * 1)
  play_group.get_offset_player(-1).add_to_score(power_level * -1)

# "Pollux", "Take the power level in points from the player to the left from the terminal player, and give that number to the player to the right."
def pollux(play_group, power_level):
  # print("pollux")
  play_group.get_offset_player(1).add_to_score(power_level * -1)
  play_group.get_offset_player(-1).add_to_score(power_level * 1)

# "The Gambler", "Flip a coin. If it's heads, give twice the power level in points to the terminal player. If tails, give the power level to each adjacent."
def gambler(play_group, power_level):
  # print("gambler")
  if(random.randint(0,1)):
    play_group.get_current_player().add_to_score(2 * power_level)
  else:
    play_group.get_offset_player(1).add_to_score(power_level)
    play_group.get_offset_player(-1).add_to_score(power_level)

# "Fate", "The terminating player must choose another player, then flip a coin. The total point change is double the power level, and the other player gains or loses points on heads or tails respectively."
def fate(play_group, power_level):
  # print("fate")
  fate_targets = []
  for p in play_group.get_player_names():
    if p != play_group.get_current_player().name:
      fate_targets.append((p, p))

  target_player_name = radiolist_dialog(
      title = "Fate",
      text = "The terminating player must choose another player, then flip a coin.\nThe total point change is double the power level.\nThe other player gains or loses points on heads or tails respectively.",
      values = fate_targets
  ).run()

  target_player = play_group.get_player_by_name(target_player_name)
  if(random.randint(0,1)):
    target_player.add_to_score(2 * power_level)
  else:
    target_player.add_to_score(-2 * power_level)

# "Waxing Crescent", "All players but the terminal player gain a point."
def waxing(play_group, power_level):
  # print("waxing")
  terminal = play_group.get_current_player().name
  for p in play_group:
    if p.name != terminal:
      p.add_to_score(1)

# "Waning Gibbous", "All players but the terminal player lose a point."
def waning(play_group, power_level):
  # print("waning")
  terminal = play_group.get_current_player().name
  for p in play_group:
    if p.name != terminal:
      p.add_to_score(-1)


def bluff_battle(winner, loser):
  score_delta = 2
  message_dialog(
    title="Bluff Battle",
    text=f"{winner.name} has won the bluffing battle and will get {score_delta} points.\n{loser.name} has lost and will lose {score_delta} points."
  ).run()
  winner.add_to_score(score_delta)
  loser.add_to_score(score_delta * -1)

def draw_new_profession(player, prof_deck):
  old_prof = player.play_from_deck(0, deck = "profession")
  player.draw_from(prof_deck, draw_to_deck = "profession")
  new_prof = player.read_from_deck(0, deck = "profession")
  message_dialog(
    title="Draw New Profession",
    text=f"{player.name} is drawing a new profession. They were the {old_prof.get_name()}; now they are the {new_prof.get_name()}."
  ).run()

dispatch_table = {
  "powerup": powerup,
  "powerdown": powerdown,
  "reverse": reverse,
  "flip": flip,
  "setcount": setcount,
  "addcount": addcount,
  "subcount": subcount,
  "endcount": endcount,
  "summon": summon,
  "scholar": scholar,
  "fool": fool,
  "baron": baron,
  "pauper": pauper,
  "castor": castor,
  "pollux": pollux,
  "gambler": gambler,
  "fate": fate,
  "waxing": waxing,
  "waning": waning,
}