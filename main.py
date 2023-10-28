from datetime import date
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

def getDecks():
    decks = invoke('deckNames')
    translate_table = str.maketrans({' ': '_', '_': ' '})
    new_decks_list = []

    for deck in decks:
        translate_table = str.maketrans({' ': '_', '_': ' '})
        new_decks_list.append(deck.translate(translate_table))
    
    return new_decks_list

def getCards():
    decks = getDecks()
    cards_list = []

    for deck_name in decks:
        deck_cards = invoke('findCards', query=f'deck:{deck_name}')
        deck_dict = { 'deck_name': deck_name, 'deck_cards' : deck_cards }
        
        cards_list.append(deck_dict)
    
    return cards_list

def getCardsInfo(deck_name):
    anki_cards = getCards()
    deck_cards = next((deck['deck_cards'] for deck in anki_cards if deck['deck_name'] == deck_name), None)

    return invoke('cardsInfo', cards=deck_cards)

def calculate_card_info():
    tango_n5_card_info = getCardsInfo("TheMoeWay_Tango_N5")
    tango_n4_card_info = getCardsInfo("TheMoeWay_Tango_N4")

    tango_n5_new_cards = []
    tango_n5_young_cards = []
    tango_n5_matured_cards = []

    tango_n4_new_cards = []
    tango_n4_young_cards = []
    tango_n4_matured_cards = []


    for n5_card in tango_n5_card_info:
        n5_card_interval = n5_card['interval']

        if int(n5_card_interval) >= 21:
            tango_n5_matured_cards.append(n5_card_interval)
        elif int(n5_card_interval) < 21 and int(n5_card_interval) != 0:
            tango_n5_young_cards.append(n5_card_interval)
        elif int(n5_card_interval) == 0:
            tango_n5_new_cards.append(n5_card_interval)
    
    for n4_card in tango_n4_card_info:
        n4_card_interval = n4_card['interval']

        if int(n4_card_interval) >= 21:
            tango_n4_matured_cards.append(n4_card_interval)
        elif int(n4_card_interval) < 21 and int(n4_card_interval) != 0:
            tango_n4_young_cards.append(n4_card_interval)
        elif int(n4_card_interval) == 0:
            tango_n4_new_cards.append(n4_card_interval)
    
    return {
        'tango_n5_new_cards': len(tango_n5_new_cards), 
        'tango_n5_young_cards':  len(tango_n5_young_cards), 
        'tango_n5_matured_cards': len(tango_n5_matured_cards), 
        'tango_n4_new_cards': len(tango_n4_new_cards), 
        'tango_n4_young_cards': len(tango_n4_young_cards),
        'tango_n4_matured_cards': len(tango_n4_matured_cards)
    }

def define_env(env):
  """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    - filter: a function with one of more arguments,
        used to perform a transformation
  """

  @env.macro
  def n5_card_counts():
    cards_info = calculate_card_info()

    new_cards = cards_info["tango_n5_new_cards"]
    young_cards = cards_info["tango_n5_young_cards"]
    matured_cards = cards_info["tango_n5_matured_cards"]
    cards_known_total = int(young_cards) + int(matured_cards)

    return f'**{cards_known_total}** vocabulary words known with **{new_cards}** new cards remaining'
  
  @env.macro
  def n4_card_counts():
    cards_info = calculate_card_info()

    new_cards = cards_info["tango_n4_new_cards"]
    young_cards = cards_info["tango_n4_young_cards"]
    matured_cards = cards_info["tango_n4_matured_cards"]
    cards_known_total = int(young_cards) + int(matured_cards)

    return f'**{cards_known_total}** vocabulary words known with **{new_cards}** new cards remaining'
  
  @env.macro
  def get_current_date():
    return date.today().strftime("%m/%d/%y")



  