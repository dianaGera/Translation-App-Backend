from random import randint
from try_output import dict, eng_words

def choice():
    print(' Tap 1 to receive new words', '\n'
          ' Tap 2 to check the word in our vocab')
    tap = int(input())
    if tap == 1:
        random_num()
    elif tap == 2:
        add_word()


def add_word():
    find_word = ''
    while find_word != '' or 'stop':
        find_word = input('Write a word: ')
        if find_word + ' ' in eng_words:
            print('That word exist in our vocab')
        else:
            print('You find a word that does not exist in our vocab. (Y/n)', '\n')
            ch = input('Want to add it? ')
            if ch == 'Yes' or 'YES' or 'yes' or 'Y' or 'y' or 'n':
                translation = input('Type the translation: ')
                #print(len(my_vocab) + 1, find_word, translation, file=writefile)
                #writefile.close()
                #if input('Back to the menu(1) or continue(2)?') == 1 or 'menu': ##


def random_num():
    rand_list = []
    c = len(dict)
    for i in range(int(input('Введите кол слов - '))):
        rand_list.append(randint(1, c + 1))
    print('\n', rand_list, '\n')
    conversion(rand_list)


def conversion(rand_list):
    c = 1
    for random_Num in rand_list:
        print(*(c, '-- ' + dict[random_Num][1] + '------ ' + dict[random_Num][2]) if c > 9 else
              (c, ' -- ' + dict[random_Num][1] + '------ ' + dict[random_Num][2]))
        c += 1
    print('\n', 'Start again? - ')

choice()