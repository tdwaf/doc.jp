import json
import urllib.request

def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke_anki_request(action, **params):
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

def get_new_cards_per_day_amount(deck_name):
    deck = deck_name.replace("_", " ")

    deck_info = invoke_anki_request('getDeckConfig', deck=deck)

    print(deck_info['new']['perDay'])

get_new_cards_per_day_amount('TheMoeWay_Tango_N5')