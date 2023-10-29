from .anki_stats.AnkiCards import AnkiCards
from datetime import date

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
    tango_n5_deck = AnkiCards('TheMoeWay_Tango_N5')

    return f'**{tango_n5_deck.get_total_known_cards()}** vocabulary words known with **{tango_n5_deck.get_new_cards()}** new cards remaining'
  
  @env.macro
  def n4_card_counts():
    tango_n4_deck = AnkiCards('TheMoeWay_Tango_N4')

    return f'**{tango_n4_deck.get_total_known_cards()}** vocabulary words known with **{tango_n4_deck.get_new_cards()}** new cards remaining'
  
  @env.macro
  def get_current_date():
    return date.today().strftime("%m/%d/%y")