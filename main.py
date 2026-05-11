#%% Preliminaries

import os
import json
from datetime import datetime
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
        Enter 'n' to proceed to new round
        Enter 'p' to play the sound
        Enter 'k' to pause/unpause the sound
        Enter 'q' to quit
    """)

def create_test_bird(birds):
    test_bird = random.choice(birds)
    birds_tested.append(test_bird)
    return test_bird

def write_score(username, score, file):
    new_score = {
        "username": username,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "score": score
    }

    filename = file

    # Load existing scores
    if os.path.exists(filename):
        with open(filename, "r") as file:
            scores = json.load(file)
    else:
        scores = []

    # Add new score
    scores.append(new_score)

    # Save updated list
    with open(filename, "w") as file:
        json.dump(scores, file, indent=4)

def reveal_answers(birds_tested):
    print(":: Correct Answers ::")
    for index, bird in enumerate(birds_tested):
        print(f"Round {index}: {bird}")

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

    print("Enter Username:")
    username = input()

    score = 0
    round = 1
    flag = False

    test_bird, test_bird_song_file = get_bird_and_audio("audio/")
    pygame.mixer.music.load(test_bird_song_file)
    print("Game starting")
    print_commands(birds)
    print(f"Round {round}:")

    # add a simple json or smt which can hold all time highest scores!!
    # this needs to read scores json, if score higher than existing for that username, then write to highscores.json too

    # and add a print at game over which compares guesses to correct answers
    # actually would be better here to just make the game politer and tell you each round, and offer an immediately replay of sound

    while True:

        user_input = input(">> ").lower()

        # --- COMMANDS ---

        if user_input == 'q':
            pygame.mixer.music.stop()
            break 

        elif user_input == 'admin':
            print(birds_tested)
            continue

        # we should probably remove this entirely, and have round 1, and all following rounds automated (reduces room for problems too)
        # although perhaps tidying this can wait until we switch to react?
        elif user_input == 'n':
            if flag == False:
                print("Bird guess required before new round")
            if flag == True:
                flag = False
                print(f'Round {score+1}:')
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
            flag = True
            pygame.mixer.music.stop()
            score += 1
            print('yeah class mate')
            print(f'Score = {score}')
            continue

        # this counts any typed and entered letters that are the wrong answer
        # must be kept as the final check for this reason
        elif user_input.isalpha():
            flag = True
            print(f'does that sound like a {user_input} you plonker')
            print(f'Score = {score}')
            write_score(username, score, "scores.json")

            # we need to show them the correct answers, then quit game. or offer replay?
            # either way it needs to be nested if options here, so they can't keep playing

            score = 0

            reveal_answers(birds_tested)

            break



    #%%


if __name__ == "__main__":
    main()
