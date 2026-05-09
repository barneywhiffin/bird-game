#%%

import os
import pygame
import random


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

#%% Setup

score = 0
pygame.mixer.init()
wrens = {}
robins = {}

for filename in os.listdir("audio/wren"):
    if filename.endswith(".wav") or filename.endswith(".mp3"):
        name = os.path.splitext(filename)[0]
        wrens[name] = pygame.mixer.Sound(
            os.path.join("audio/wren", filename)
        )

for filename in os.listdir("audio/robin"):
    if filename.endswith(".wav") or filename.endswith(".mp3"):
        name = os.path.splitext(filename)[0]
        robins[name] = pygame.mixer.Sound(
            os.path.join("audio/robin", filename)
        )

print(wrens.keys())
print(robins.keys())

# sounds['wren1'].play()

wren, wren_song = random.choice(list(wrens.items()))

print(wren)
print(wren_song)

#%%

def main():

    #%% User Interaction

    print("Game starting")
    print_commands()

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
