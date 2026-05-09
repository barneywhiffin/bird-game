#%%

import pygame

#%%

def print_commands():
    print("""
        Enter a bird name to make a guess
          
        Controls:
        Enter 'p' to play/replay the sound
        Enter ' ' to pause/unpause the sound
        # Enter 'n' to proceed to the next bird
        Enter 'q' to quit
    """)

def main():

    #%% User Interaction

    score = 0

    print("Game starting")
    print_commands()

    pygame.mixer.init()
    pygame.mixer.music.load('audio/wren1.wav')

    bird = 'wren'

    while True:
        user_input = input(">> ").lower()

        # --- COMMANDS ---

        if user_input == 'q':
            break 

        if user_input == 'p':
            # print('Round starting')
            pygame.mixer.music.play()
            continue

        elif user_input == ' ':
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
        
        elif user_input == 'k':
            pygame.mixer.music.stop()
            continue

        elif user_input == bird:
            score += 1
            print('yeah class mate')
            print(f'Score = {score}')
            print("Next bird....")

        # this counts any typed and entered letters that are the wrong answer
        elif user_input.isalpha():
            score = 0
            print(f'does that sound like a {user_input} you plonker')
            print(f'Score = {score}')
            print("Next bird....")


    #%%


if __name__ == "__main__":
    main()
