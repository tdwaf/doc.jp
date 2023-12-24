from main.anki_stats.anki_util import invoke_anki_request

class AnkiCards:
  def __init__(self, deck_name):
    self.deck_name = deck_name

  def __get_cards(self) -> type:
    return invoke_anki_request('findCards', query=f'deck:{self.deck_name}')
  
  def get_deck_name(self) -> str:
    return self.deck_name.replace("_", " ")

  def get_card_statistics(self) -> type:
    anki_cards = self.__get_cards()
    return invoke_anki_request('cardsInfo', cards=anki_cards)
  
  def get_new_cards_per_day_amount(self) -> type:
    deck_name = self.deck_name.replace("_", " ")
    deck_info = invoke_anki_request('getDeckConfig', deck=deck_name)

    return deck_info['new']['perDay']