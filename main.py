#%% Preliminaries

import os
# from pathlib import Path
import pygame
pygame.mixer.init()
import random

#%% Functions

def print_commands():
    print("""
        Enter a bird name to make a guess
          
        Controls:
        Enter 'p' to play/replay the sound
        Enter ' ' to pause/unpause the sound
        # Enter 'n' to proceed to the next bird
        Enter 'q' to quit
    """)

birds_tested = []

def create_test_bird(birds):
    test_bird = random.choice(birds)
    birds_tested.append(test_bird)
    return test_bird

#%% Setup

# list of all birds which works adaptively (can add more birds to project)
birds = [
    folder for folder in os.listdir("audio")
    if os.path.isdir(os.path.join("audio", folder))
    and os.listdir(os.path.join("audio", folder)) # checks that the folder is not empty
]

print(birds)

#%% Random Choice of Bird

test_bird = create_test_bird(birds)
print(test_bird)

#%% make dictionary of everything in folder for that bird

# possibly this can be massively simplified if we never care about which wav it was??

test_bird_kvps = {}

root_path = "audio/"
path_string = root_path + test_bird

for filename in os.listdir(path_string):
    if filename.endswith(".wav"):
        name = os.path.splitext(filename)[0]
        test_bird_kvps[name] = pygame.mixer.Sound(
            os.path.join(path_string, filename)
        )

print(test_bird_kvps)

#%% random choice of example of that bird

test_bird_song = random.choice(list(test_bird_kvps.values()))

print(test_bird_song)

#%%

def main():

    #%% User Interaction

    print("Game starting")
    print_commands()

    score = 0
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
