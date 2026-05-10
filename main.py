#%% Preliminaries

import os
# from pathlib import Path
import pygame
pygame.mixer.init()
import random

#%% Setup

# list of all birds which works adaptively (can add more birds to project)
birds = [
    folder for folder in os.listdir("audio")
    if os.path.isdir(os.path.join("audio", folder))
    and os.listdir(os.path.join("audio", folder)) # checks that the folder is not empty
]

#%% Functions

# i reckon add n for proceed to next bird? nice pause in between rounds then
def print_commands(birds):
    print(f"""
        Enter a bird name to make a guess
        Possible answers are: {birds}
          
        Controls:
        Enter 'n' to start, and proceed to new round
        Enter 'p' to play the sound
        Enter 'k' to pause/unpause the sound
        Enter 'q' to quit
    """)

def create_test_bird(birds):
    test_bird = random.choice(birds)
    birds_tested.append(test_bird)
    return test_bird



#%% Random Choice of Bird and Audio

birds_tested = []

# we need to functionise everything below so it is callable in loop during game
# the function should be passed nothing and return nothing
# simply adds new bird to list of tested, and loads bird audio file into mixer?
# or we could have it return the audio file, and correct answer if cleaner

def get_bird_and_audio(root_path):

    test_bird = create_test_bird(birds)

    # make dictionary of everything in folder for that bird
    # ideally actually we would preload all of these.... 
    # instead of scanning directory from blank each round of game
    test_bird_dict = {}

    path_string = root_path + test_bird

    for filename in os.listdir(path_string):
        if filename.endswith(".wav"):
            name = os.path.splitext(filename)[0]
            test_bird_dict[name] = pygame.mixer.Sound(
                os.path.join(path_string, filename)
            )

    # random choice of example of that bird
    test_bird_key, test_bird_song = random.choice(list(test_bird_dict.items()))

    test_bird_song_file = root_path + test_bird + '/' + test_bird_key + '.wav'
    
    return test_bird, test_bird_song_file

#%%

def main():

    #%% User Interaction

    print("Game starting")
    print_commands(birds)

    score = 0

    while True:

        user_input = input(">> ").lower()

        # --- COMMANDS ---

        if user_input == 'q':
            pygame.mixer.music.stop()
            break 

        elif user_input == 'admin':
            print(birds_tested)
            continue

        elif user_input == 'n':
            print('Next round')
            test_bird, test_bird_song_file = get_bird_and_audio("audio/")
            pygame.mixer.music.load(test_bird_song_file)
            continue

        elif user_input == 'p':
            print('Bird singing')
            pygame.mixer.music.play()
            continue

        elif user_input == 'k':
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()
            continue

        elif user_input == test_bird:
            score += 1
            print('yeah class mate')
            print(f'Score = {score}')
            test_bird, test_bird_song_file = get_bird_and_audio("audio/")
            pygame.mixer.music.load(test_bird_song_file)
            continue

        # this counts any typed and entered letters that are the wrong answer
        elif user_input.isalpha():
            score = 0
            print(f'does that sound like a {user_input} you plonker')
            print(f'Score = {score}')
            test_bird, test_bird_song_file = get_bird_and_audio("audio/")
            pygame.mixer.music.load(test_bird_song_file)
            continue


    #%%


if __name__ == "__main__":
    main()
