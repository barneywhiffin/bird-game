#%% Preliminaries

import os
import json
from datetime import datetime
import pygame
pygame.mixer.init()
import random

#%% Setup

audio_path = "assets/audio"

# list of all birds which works adaptively (can add more birds to project)
birds = [
    folder for folder in os.listdir(audio_path)
    if os.path.isdir(os.path.join(audio_path, folder))
    and os.listdir(os.path.join(audio_path, folder)) # checks that the folder is not empty
]

#%% Functions

def print_commands(birds):
    print(f"""
        Enter a bird name to make a guess
        Possible answers are: {birds}
          
        Controls:
        Enter 'p' to play the sound
        Enter 'k' to pause/unpause the sound
        Enter 'b' for a reminder of the available birds
        Enter 'q' to quit
    """)

def create_test_bird(birds):
    test_bird = random.choice(birds)
    birds_tested.append(test_bird)
    return test_bird

def write_score(username, score, scores_file, high_scores_file):
    new_score = {
        "username": username,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "time": datetime.now().strftime("%H:%M:%S"),
        "score": score
    }

    filename = scores_file

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

    write_high_score(scores_file, high_scores_file)

def write_high_score(scores_file, high_scores_file):
    with open(scores_file, "r") as file:
        data = json.load(file)

    grouped = {}

    for entry in data:
        grouped.setdefault(
            entry["username"],
            []
        ).append(entry["score"])

    highscores = []

    for username, scores in grouped.items():
        best_score = max(scores)
        highscores.append([username, best_score])

    with open(high_scores_file, "w") as file:
        json.dump(highscores, file, indent=4)

def reveal_answers(birds_tested):
    print(":: Correct Answers ::")
    for index, bird in enumerate(birds_tested):
        print(f"Round {index}: {bird}")


#%% Random Choice of Bird and Audio

birds_tested = []

def get_bird_and_audio(root_path):

    test_bird = create_test_bird(birds)

    # make dictionary of everything in folder for that bird
    # ideally actually we would preload all of these.... 
    # instead of scanning directory from blank each round of game
    test_bird_dict = {}

    path_string = root_path + '/' + test_bird

    for filename in os.listdir(path_string):
        if filename.endswith(".wav"):
            name = os.path.splitext(filename)[0]
            test_bird_dict[name] = pygame.mixer.Sound(
                os.path.join(path_string, filename)
            )

    # random choice of example of that bird
    test_bird_key, test_bird_song = random.choice(list(test_bird_dict.items()))

    test_bird_song_file = root_path + '/' + test_bird + '/' + test_bird_key + '.wav'
    
    return test_bird, test_bird_song_file

#%%

def main():

    #%% User Interaction

    print("Enter Username:")
    username = input()

    score = 0

    test_bird, test_bird_song_file = get_bird_and_audio(audio_path)
    pygame.mixer.music.load(test_bird_song_file)
    print("Game starting")
    print_commands(birds)
    print(f"Round {score+1}:")

    while True:

        user_input = input(">> ").lower()

        # --- COMMANDS ---

        if user_input == 'q':
            pygame.mixer.music.stop()
            print(f'Final score = {score}')
            write_score(username, score, "scores.json", "highscores.json")
            # reveal_answers(birds_tested)
            break 

        elif user_input == 'admin':
            print(birds_tested)
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

        elif user_input == 'b':
            print(f"Possible answers are: {birds}")

        elif user_input == "r":
            score = 0
            print(f"Score = {score}")
            print(f'Round {score+1}:')
            test_bird, test_bird_song_file = get_bird_and_audio(audio_path)
            pygame.mixer.music.load(test_bird_song_file)

        elif user_input == test_bird:
            pygame.mixer.music.stop()
            score += 1
            print('Correct!')
            print(f'Round {score+1}:')
            test_bird, test_bird_song_file = get_bird_and_audio(audio_path)
            pygame.mixer.music.load(test_bird_song_file)
            continue

        # this counts any typed letters that are not captured by above ifs
        # must be kept as the final check for this reason
        elif user_input.isalpha():
            pygame.mixer.music.stop()
            print(f'Not quite, that one was a {test_bird}')
            print("Enter 'p' to hear the sound again, 'r' to reset score and continue, or 'q' to quit")

            continue


    #%%

if __name__ == "__main__":
    main()
