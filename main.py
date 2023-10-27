import json
import urllib.request

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
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

def getCards():
    return invoke('findCards', query='deck:current')

def getCardsInfo():
    anki_cards = getCards()
    cards_info = invoke('cardsInfo', cards=anki_cards)

    new_cards = []
    young_cards = []
    matured_cards = []
    
    for card in cards_info:
        card_interval = card['interval']

        if int(card_interval) >= 21:
            matured_cards.append(card_interval)
        elif int(card_interval) < 21 and int(card_interval) != 0:
            young_cards.append(card_interval)
        elif int(card_interval) == 0:
            new_cards.append(card_interval)
    
    return { 'new_cards': len(new_cards), 'young_cards': len(young_cards), 'mature_cards': len(matured_cards)}

def define_env(env):
  """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    - filter: a function with one of more arguments,
        used to perform a transformation
  """

  @env.macro
  def card_counts_message():
    cards_info = getCardsInfo()

    new_cards = cards_info["new_cards"]
    young_cards = cards_info["young_cards"]
    matured_cards = cards_info["mature_cards"]
    cards_known_total = int(young_cards) + int(matured_cards)

    return f'**{cards_known_total}** vocabulary words known with {new_cards} new cards remaining'


  