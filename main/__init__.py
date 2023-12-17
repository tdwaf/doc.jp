from main.anki_stats.anki_cards import AnkiCards
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
  def tango_n5_card_stats() -> dict:
    tango_n5_deck = AnkiCards('TheMoeWay_Tango_N5')

    new_cards = tango_n5_deck.get_new_cards()
    young_cards = tango_n5_deck.card_interval_stats()["young_cards"]
    mature_cards = tango_n5_deck.card_interval_stats()["mature_cards"]
    total_cards_known = tango_n5_deck.card_interval_stats()["total_cards_known"]

    return {'new_cards': new_cards, 'young_cards': young_cards, 'mature_cards': mature_cards, 'total_cards_known': total_cards_known}
  
  @env.macro
  def tango_n4_card_stats() -> dict:
    tango_n4_deck = AnkiCards('TheMoeWay_Tango_N4')

    new_cards = tango_n4_deck.get_new_cards()
    young_cards = tango_n4_deck.card_interval_stats()["young_cards"]
    mature_cards = tango_n4_deck.card_interval_stats()["mature_cards"]
    total_cards_known = tango_n4_deck.card_interval_stats()["total_cards_known"]

    return {'new_cards': new_cards, 'young_cards': young_cards, 'mature_cards': mature_cards, 'total_cards_known': total_cards_known}
  
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
  