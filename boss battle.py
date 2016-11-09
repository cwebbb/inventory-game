import random, os


def guess_number(tries):
    
    def show_boss():
        boss = ['                                |                              ',            
 '                               ||                              ',           
'       -==-____        _--_   ___||___   _--_        ____-==-   ',             
'          ---__----___/ __ \--  || |  --/ __ \___----__---      ',            
'               ---__ / /  \ \   \\ /   / /  \ \ __---           ',           
'                    -\|    \ \  _\/_  / /    |/-                ',          
'                   __/ \_()/\ \//  \\/ /\()_/ \__               ',         
'                  /_ \ / ~~  `-'    '-  ~~ \ / _\              ',        
'                 |/_\ |(~/   /\  /\  /\   \~)| /_\|             ',       
'                  /_  | /   (O ` \/   O)   \ |  _\              ',      
'                  _\ \_\/\___--~~~~--___/\/_/ /_               ',     
'                  /    _/\^\ V~~V/~V~~V /^/\_    \              ',    
'                  \/\ / \ \^\  |( /    /^/ / \ /\/              ',   
'                     \\   /\^\  \\\   /^/\   //                 ',  
'                     \ | /\^\  \/  /^/\ | /                     ',
'                         |( /\_\^__^/_/\ )|                     ', 
'                         | \\__--__--__// |                     ',
'                        /~~~~~~~~~~~~~~~~~~\                    ',
'                       |/|  /\  /\/\  /\  |\|                   ',
'                       ||| | | ( () ) | | |||                   ',
'                       |\|  \/  \/\/  \/  |/|                   ',
'                        \__________________/                    ',
'                        | (____------____) |                    ',
                                                                  ] 
        os.system('clear')                                                            
        for e in boss:
            print(e)

    def choose_number():
        numbers = '0123456789'
        chosen_number = ''
        range_start = 1
        while len(chosen_number) < 3:
            digit = random.randrange(range_start, 10)
            digit = str(digit)
            if digit not in chosen_number:
                chosen_number += digit
                range_start = 0
                numbers = numbers.replace(digit, '')
        return chosen_number            

    number = choose_number()
    show_boss()
    print('\n\nWelcome human! You did well so far. It\'s a shame it\'s all for naught!!!')
    print("I have thought up a 3 digit number. Each digit is unique.\nYou have %s guesses to get it or YOU WILL DIE!!!" % tries )
    print(number)
    while True:
        answer = []
        guess = input('Enter your guess: ')
        if guess == number:
            print('YOU GOT LUCKY THIS TIME BASTARD!!!\n')
            break
        elif len(guess) == 3 and guess.isdigit() == True and guess[0] != '0' and guess[0] != guess[1] != guess[2]:
            tries -= 1
            if tries == 0:
                print('YOU DIED!!!\n')
                break
            count = 0
            while count < len(number):
                if guess[count] == number[count]:
                    answer.append('Hot')
                elif guess[count] in number:
                    answer.append('Warm')
                count += 1
            if answer:
                print(' '.join(sorted(answer)))
            else:
                print('Cold')
            print('You have %s tries left.' % tries )
        else:
            print("You are one of those strong but stupid heroes aren't you?!")



guess_number(10)
