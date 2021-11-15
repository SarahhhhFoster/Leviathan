import cards
import players
from itertools import repeat
import random
import urwid

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for c in choices:
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', item_chosen, c)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button, choice):
    response = urwid.Text([f"OK.\n"])
    done = urwid.Button(u'Ok')
    urwid.connect_signal(done, 'click', exit_program)
    main.original_widget = urwid.Filler(urwid.Pile([response,
        urwid.AttrMap(done, None, focus_map='reversed')]))

def exit_program(button):
    raise urwid.ExitMainLoop()

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

divination_deck = cards.CardDeck(
  list(repeat(["The Scholar", "Give two times the power level in points to the terminal player.", "The Fool", "Take two times the power level in points from the terminal player."], divination_repeats)) +
  list(repeat(["The Baron", "Give the power level in points to adjacent players.", "The Pauper", "Take the power level in points from adjacent players."], divination_repeats)) +
  list(repeat([
    "Castor", "Give the power level in points to the player to the left from the terminal player, and take that number from the player to the right.",
    "Pollux", "Take the power level in points from the player to the left from the terminal player, and give that number to the player to the right."], divination_repeats)) +
  list(repeat([
    "The Gambler", "Flip a coin. If it's heads, give twice the power level in points to the terminal player. If tails, give the power level to each adjacent.",
    "Fate", "The terminating player must choose another player, then flip a coin. The total points change is double the power level, and the other player gains or loses points on heads or tails respectively."], divination_repeats)) +
  list(repeat(["Waxing Crescent", "All players but the terminal player gain a point.", "Waning Gibbous", "All players but the terminal player lose a point."], divination_repeats)),
  name = "Divination Deck")
divination_deck.shuffle()

# Players should be able to, as professional powers:
# * Add to power
# * Subtract from power
# * Reverse direction
# * Flip the divination
# * End round

class_repeats = 2

class_deck = cards.CardDeck(
  list(repeat(["Numerologist", "The numerologist can increase or decrease the power of a divination by one point.", {"can": ["powerup", "powerdown"]}], class_repeats)) +
  list(repeat(["Palmist", "The palm reader can increase the power of a divination by one point or reverse the direction of play.", {"can": ["powerup", "reverse"]}], class_repeats)) +
  list(repeat(["Clairvoyant", "The clairvoyant can increase the power of a divination by one point or reverse the divination card.", {"can": ["powerup", "flip"]}], class_repeats)) +
  list(repeat(["Personage", "The personage can increase the power of a divination by one point or end the divination round.", {"can": ["powerup", "end"]}], class_repeats)) +
  list(repeat(["Thelemite", "The thelemite can decrease the power of a divination by one point or reverse the direction of play.", {"can": ["powerdown", "reverse"]}], class_repeats)) +
  list(repeat(["Haruspex", "The haruspex can decrease the power of a divination by one point or reverse the divination card.", {"can": ["powerdown", "flip"]}], class_repeats)) +
  list(repeat(["Exorcist", "The exorcist can decrease the power of a divination by one point or end the divination round.", {"can": ["powerdown", "end"]}], class_repeats)) +
  list(repeat(["Theosophist", "The theosophist can reverse the direction of play or reverse the divination card.", {"can": ["reverse", "flip"]}], class_repeats)) +
  list(repeat(["Thaumaturge", "The thaumaturge can reverse the direction of play or end the divination round.", {"can": ["reverse", "end"]}], class_repeats)) +
  list(repeat(["Demonologist", "The demonologist can reverse the divination card or end the divination round.", {"can": ["flip", "end"]}], class_repeats)),
  name = "Profession Deck")

power_descriptions = {
  "powerup": {
    "name": "Increase power",
    "long_desc": "Add one point to the power of the current divination."
  },
  "powerdown": {
    "name": "Decrease power",
    "long_desc": "Remove one point from the power of the current divination."
  },
  "reverse": {
    "name": "Reverse play",
    "long_desc": "Reverse the direction of turn-passing play."
  },
  "flip": {
    "name": "Reverse divination",
    "long_desc": "Flip the divination card to reverse its nature."
  },
  "end": {
    "name": "End round",
    "long_desc": "End the current divination round."
  }
}

class_deck.shuffle()

demo_group = players.PlayerGroup(["Sarah", "Jaala", "Kirstin", "Jessica"], default_decks = {"profession": cards.CardDeck(name="Profession")})
demo_group.deal_cards_from(class_deck, 1, "profession")

current_card = divination_deck.draw()
if(random.randint(0,1)):
  current_card.flip()

current_player = demo_group.get_current_player()
current_profession = current_player.read_from_deck(0, deck = "profession")
main = urwid.Padding(
  menu(f"Player {current_player.name}, {current_profession.name}, what would you like to do?",
  map(lambda x: ("* " if (x in current_profession.get_attr("can")) else "  ") + power_descriptions[x]['name'], power_descriptions.keys())),
  left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 60),
    valign='middle', height=('relative', 60),
    min_width=20, min_height=9)
urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
