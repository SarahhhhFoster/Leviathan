import cards
import players

demo_cards = cards.CardDeck([
  ["test one", "the first card to test"],
  ["test two", "the second card to test"],
  ["test three", "you see where this is going"]
], name = "Deck")
demo_cards.shuffle()

demo_group = players.PlayerGroup(["John Doe", "Jane Doe"])
demo_group.deal_cards_from(demo_cards, 1)

print(demo_group)
for player in demo_group:
  print(player)
print(demo_cards)