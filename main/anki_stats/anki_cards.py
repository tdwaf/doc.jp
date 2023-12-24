import json
import urllib.request

class AnkiCards:
  def __init__(self, deck_name):
    self.deck_name = deck_name

  def __anki_request(action, **params) -> dict:
    return {'action': action, 'params': params, 'version': 6}
  
  def request(self, action, **params):
    requestJson = json.dumps(self.__anki_request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

  def __get_cards(self) -> type:
    return self.request('findCards', query=f'deck:{self.deck_name}')
  
  def get_deck_name(self) -> str:
    return self.deck_name.replace("_", " ")

  def get_card_statistics(self) -> type:
    anki_cards = self.__get_cards()
    return self.request('cardsInfo', cards=anki_cards)
  
  def get_new_cards_per_day_amount(self) -> type:
    deck_name = self.deck_name.replace("_", " ")
    deck_info = self.request('getDeckConfig', deck=deck_name)

    return deck_info['new']['perDay']