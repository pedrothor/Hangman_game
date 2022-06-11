def add_words():
    requested_word = input('Add one word for our database (0 to exit): ')
    words_list = []  # This list just in case of the user type the same word in the same round.
    if requested_word == '0':
        print('See you later!')
    else:
        with open("secret_words.txt", "r") as words_hang:
            if f'{requested_word}\n' in words_hang.readlines():
                print('Ops! This word already exists in the database. Try another one.')
                words_hang.close()
                add_words()
            else:
                with open("secret_words.txt", "a") as words_hang2:
                    if f'{requested_word}\n' in words_list:
                        print('You have already typed this word! Try another one.')
                        add_words()
                    else:
                        words_list.append(f'{requested_word}\n')
                        words_hang2.write(f'{requested_word.lower()}\n')
                        print(f'The word "{requested_word.title()}" was add!')
                        words_hang2.close()
                        add_words()


def secret_word():  # Choosing the secret word
    """This function returns a random word of a created file called as 'Palavras_forca'"""
    import random

    objective = int(input('What do you want?\n1 - Random secret word\n2 - Type a secret word\n3 - Add a word to the list\nChoose one: '))

    if objective == 1:

        with open('secret_words.txt', 'r') as choosing_word:
            lista = choosing_word.readlines()
            num = random.randint(0, len(lista)-1)

            chosen_word = lista[num].rstrip('\n')
        return chosen_word.lower()

    elif objective == 2:
        word = input('Type the secret word: ')
        return word.lower()

    elif objective == 3:
        add_words()

    else:
        print('Invalid command, try again.')
        secret_word()


def hangman():
    """This function is resposible for doing all mecanic of the game"""

    frase = 'WELCOME TO THE HANGMAN GAME!'

    print(len(frase) * '=')
    print(frase)
    print(len(frase) * '=')
    try:
        amount_players = int(input('How many players will participate? '))
        players = []
        players_points = dict()
        x = 1
        while x <= amount_players:
            name = input(f'Insert the name of the {x}º player: ')
            players.append(name)
            players_points[name] = 0
            x += 1

        word = secret_word()
        print(word)
        for i in range(50):
            print()
        print('Here we go!\n')
        print('| - - -\n|\n|\n|' + ' ' + '_ ' * len(word))
        typed = []  # Here will be stored the letters typed during the game.

        round_game = 0  # round is only to take over control about what player will play.
        errors = 0
        letters_of_chosen_word = set(list(word))  # storing the letters in a set to do not have duplicated items.
        while True:

            print(f'Already typed letters : {typed}\n')

            if errors == 6 or len(letters_of_chosen_word) == 0:  # 6 because the body has 6 members (1 head, 2 arms, chest, 2 lengs)
                print('Finish!\n')
                print(f'Correct word: {word.title()}')
                print('-'*len(word))
                print('Ranking')
                print('-'*len(word))

                pontos_ranking = sorted(players_points.values())[::-1]
                final_raking = dict()
                for i in pontos_ranking:
                    for k in players_points.keys():
                        if players_points[k] == i:
                            final_raking[k] = players_points[k]

                for keys, values in final_raking.items():
                    print(f'{keys.title()}: {values} point(s)')

                break

            else:
                typed_letter = input(f'{players[round_game].title()}, type a letter: ')

                if len(typed_letter) == 1:

                    if typed_letter in typed:

                        print(f'Letter "{typed_letter}" already typed! Try again.')
                        drawn(errors)
                        change_letters(word, typed)

                    elif typed_letter in letters_of_chosen_word:
                        typed.append(typed_letter)
                        drawn(errors)
                        change_letters(word, typed)

                        while typed_letter in letters_of_chosen_word:  # removing the typed letter from the secret word
                            letters_of_chosen_word.remove(typed_letter)

                        print(f'{players[round_game].title()}, you have earned 1 point!')

                        players_points[players[round_game]] += 1  # giving + 1 point to the player
                        # Here we don't add nothing to the round due to will be the same player, cause he had choose a correct letter.

                    else:
                        print(f'unfortunately the letter "{typed_letter}" does not belong to the secret word :(')
                        typed.append(typed_letter)  # add the does not belong to the typed_letter list.
                        errors += 1  # add 1 error
                        round_game += 1  # skiping to the next player
                        drawn(errors)
                        change_letters(word, typed)

                        if round_game > len(players) - 1:  # In case of the round is higher than last player index in the list, we return to the first player.
                            round_game = 0
                else:
                    print('You must type one letter by time!')
                    drawn(errors)
                    change_letters(word, typed)
    except ValueError:
        print('Error: You have typed something diferent of an integer number. Try again.')
        hangman()


def drawn(errors):
    """This function is responsible for printing the drawn of the hangman's game according to the errors"""
    if errors == 0:
        print('| - - -\n|\n|\n|')
    elif errors == 1:
        print('| - - -\n|     O\n|\n|')
    elif errors == 2:
        print('| - - -\n|     O\n|     |\n|')
    elif errors == 3:
        print('| - - -\n|     O\n|    /|\n|')
    elif errors == 4:
        print('| - - -\n|     O\n|    /|\ ')
    elif errors == 5:
        print('| - - -\n|     O\n|    /|\ \n|    /')
    else:
        print('| - - -\n|     O\n|    /|\ \n|    / \ ')
        print('GAME OVER')


def change_letters(word, typed):
    """Essa função é responsável por trocar os underlines '_' pela letra da palavra secreta"""
    show_letters = ''
    for secret_letter in word:
        if secret_letter in typed:
            show_letters += secret_letter
        else:
            show_letters += '_'

    print('  ' + f'{show_letters}')


hangman()
