from main.anki_stats.anki_cards import AnkiCards
from main.anki_stats.anki_util import invoke_anki_request
from datetime import date, datetime, timedelta

def define_env(env):
  """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    - filter: a function with one of more arguments,
        used to perform a transformation
  """
  
  @env.macro
  def get_card_interval_stats(deck_choice):
    tango_n5_deck = AnkiCards('TheMoeWay_Tango_N5')
    tango_n4_deck = AnkiCards('TheMoeWay_Tango_N4')

    deck = AnkiCards('')

    if deck_choice == 'tango-n5':
      deck = tango_n5_deck
    elif deck_choice == 'tango-n4':
      deck = tango_n4_deck

    card_stats = deck.get_card_statistics()

    new_cards = [int(card['interval']) for card in card_stats if card['interval'] == 0]
    young_cards = [int(card['interval']) for card in card_stats if card['interval'] < 21 and card['interval'] != 0]
    mature_cards = [int(card['interval']) for card in card_stats if card['interval'] >= 21]

    total_cards_known = 0
    if len(new_cards) == 0:
      stats = invoke_anki_request('getDeckStats', decks=[deck.get_deck_name()])
      deck_id = list(stats.keys())[0]
      total_cards_known = stats[str(deck_id)]['total_in_deck']
    else:
      total_cards_known = len(young_cards) + len(mature_cards)

    return {'new': len(new_cards), 'young': len(young_cards), 'mature': len(mature_cards), 'total_cards': total_cards_known }
  
  @env.macro
  def get_current_date():
    return date.today().strftime("%m/%d/%y")
  
  @env.macro
  def get_new_cards_finish_date() -> str:
    tango_n5_deck = AnkiCards('TheMoeWay_Tango_N5')
    new_cards = tango_n5_deck.get_new_cards()

    days_to_finish = 0
    while new_cards > 0:
      new_cards -= tango_n5_deck.get_new_cards_per_day_amount()
      days_to_finish += 1

    date_finished_with_new_cards = datetime.strftime(datetime.today() + timedelta(days=days_to_finish), "%m/%d/%y")

    return date_finished_with_new_cards

  @env.macro
  def get_cards_per_day() -> dict:
    tango_n5_deck = AnkiCards('TheMoeWay_Tango_N5')
    tango_n4_deck = AnkiCards('TheMoeWay_Tango_N4')

    return { 'N5_Cards_Per_Day': tango_n5_deck.get_new_cards_per_day_amount(), 'N4_Cards_Per_Day': tango_n4_deck.get_new_cards_per_day_amount()  }