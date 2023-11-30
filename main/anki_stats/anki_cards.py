from main.anki_stats.anki_util import invoke_anki_request

class AnkiCards:
  def __init__(self, deck_name):
    self.deck_name = deck_name

  def __get_cards(self):
    return invoke_anki_request('findCards', query=f'deck:{self.deck_name}')

  def __get_card_statistics(self):
    anki_cards = self.__get_cards()
    return invoke_anki_request('cardsInfo', cards=anki_cards)

  def get_total_known_cards(self):
    card_stats = self.__get_card_statistics()

    mature_cards = []
    young_cards = []

    for card in card_stats:
      card_interval = card['interval']

      if int(card_interval) >= 21:
        mature_cards.append(card_interval)
      elif int(card_interval) < 21 and int(card_interval) != 0:
        young_cards.append(card_interval)
    
    return int(len(mature_cards)) + int(len(young_cards))

  def get_new_cards(self):
    card_stats = self.__get_card_statistics()

    new_cards = []

    for card in card_stats:
      card_interval = card['interval']

      if int(card_interval) == 0:
        new_cards.append(card_interval)

    return int(len(new_cards))
  
  def get_new_cards_per_day_amount(self):
    deck_name = self.deck_name.replace("_", " ")
    deck_info = invoke_anki_request('getDeckConfig', deck=deck_name)

    return deck_info['new']['perDay']
  
  def get_deck_stats(self):
    deck_name = self.deck_name.replace("_", " ")
    return invoke_anki_request('getDeckStats', decks=deck_name)


