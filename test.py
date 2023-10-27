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

# deck:TheMoeWay_Tango_N5

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
        deck_dict = { deck_name : deck_cards }
        
        cards_list.append(deck_dict)
    
    return cards_list

def calculate(thing):
    for thing in cardLIst:
        print(thing[0])

def test():
    decks = getDecks()
    cardLIst = getCards()

    for thing in cardLIst:
        print(thing[0])

test()