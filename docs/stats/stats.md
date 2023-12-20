# Anki Stats

## Anki Deck Card Counts

### Tango N5 as of {{ get_current_date() }}

- **Young Cards**: {{ get_card_interval_stats('tango-n5')['young'] }}
- **Mature Cards**: {{ get_card_interval_stats('tango-n5')['mature'] }}
- **Total Cards Known**: {{ get_card_interval_stats('tango-n5')['total_cards'] }}

![Card Counts](../assets/anki-stats/n5-card-counts.png){ align=center }

### Tango N4 as of {{ get_current_date() }}

- **New Cards**: {{ get_card_interval_stats('tango-n4')['new'] }}
- **Young Cards**: {{ get_card_interval_stats('tango-n4')['young'] }}
- **Mature Cards**: {{ get_card_interval_stats('tango-n4')['mature'] }}

![Card Counts](../assets/anki-stats/n4-card-counts.png){ align=center }