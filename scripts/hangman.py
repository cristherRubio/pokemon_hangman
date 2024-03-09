import random
import re

'''
Basic hangman python logic
- Has a dynamic life system which divides (floored) all letters of the str by 2 and -1 the result to calculate life
- Dynamic regex replacement for correct letters
'''

#TODO: Display incorrect but already used letters

WORDS = ['Hola', 'Pikachu', 'Bulbasur']

sucess = False
pokemon = random.choice(WORDS).upper()
guessed_chars = []
attempts = (len(pokemon) // 2) - 1 
while True:
    if attempts < 0:
        print('LOST')
        break   

    print('Attempts', attempts)
    print('Guess the pokémon!')
    regex = r'[^ '+ "".join(guessed_chars) + r']'
    regex_sub = re.sub(regex, '_', pokemon)

    if regex_sub == pokemon:
        print('WON!')
        break
    
    print(regex_sub)
    letter_guess = input('enter a letter: ').upper()

    if letter_guess in pokemon:
        guessed_chars.append(letter_guess) 
    else:
        attempts -= 1