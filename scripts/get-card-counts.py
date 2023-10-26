print('What is the value for new?')

new_cards_count = input()

print('What is the value for learning?')

learning_cards_count = input()

print('What is the value for re-learning?')

re_learing_cards_count = input()

print('What is the value for young?')

young_cards_amount = input()

print('What is the value for mature?')

mature_cards_amount = input()

print('What is the value for suspended?')

suspended_cards_amount = input()

print('What is the value for buried?')

buried_cards_amount = input()

total_learned_cards_amount = int(young_cards_amount) + int(mature_cards_amount)

print(f'**{total_learned_cards_amount}** Vocabulary words known with **{new_cards_count}** new cards remaining: On track to finish all new cards on **_November 28th_** doing 15 new cards a day. Then I\'ll start Tango N4 with the same new card amount.')
