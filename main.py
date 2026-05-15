#%% Preliminaries

import os
import json
from datetime import datetime
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame
pygame.mixer.init()
import random

# should eventually have easy medium and hard difficulties (reflecting number of birds + how easy to distinguish them)
# and a custom mode where specifically the birds tested are to be included (needs a catch case for need to select at least 2 more, and at least 1 more)

# for now should just be a user input option at the start saying, are there any birds you would like to exclude ?

# should also be choice to include calls (or just have songs)
# would this need additional calls folder in each bird folder, and then associated ifs and path 'calls/' whatever?
# this should be simple tick, birds to exclude should be dropdown with ticks? (eventually)

# we can now take away the option to play/pause, as the audio is all v short

# space in input when this is the wrong answer breaks the game !! just skips to next input

# would be nice to have replay sound or next bird.... but in terminal this would be long

# maybe just... only have songbirds?

# change the jsons to be templates, with your private ones in .gitignore
# then if can't find data/scores.json, it makes a copy of scores template called this
# allowing people to have their own

# add some kind of audio normalisation too

#%% Setup

audio_path = "assets/audio"

# list of all birds which works adaptively (can add more birds to project)
birds = [
    folder for folder in os.listdir(audio_path)
    if os.path.isdir(os.path.join(audio_path, folder))
    and os.listdir(os.path.join(audio_path, folder)) # checks that the folder is not empty
]

corvids = []
for i in birds:
    if i == 'crow':
        corvids.append('crow')
    if i == 'magpie':
        corvids.append('magpie')
    if i == 'jackdaw':
        corvids.append('jackdaw')
    if i == 'rook':
        corvids.append('rook')
    

#%% Functions

def print_commands(corvids):
    print(f"""
        Enter 'p' to play or replay the sound
        Enter a bird name to make a guess
        Enter 'birds' to see the available birds
        Enter 'help' to view this menu again
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

    print("""
          
            ::::::::: BIRD GAME :::::::::
        
    """)
    print_commands(corvids)

    print("Enter Username:")
    username = input()

    print("Fuck corvids: y/n?")
    while True:
        fcorvids = input().lower()
        if fcorvids == 'y':
            for i in corvids:
                birds.remove(i)
            print('Corvids removed!')
            break
        elif fcorvids == 'n':
            break
        else:
            print("that was not a 'y' or 'n'")


    score = 0

    test_bird, test_bird_song_file = get_bird_and_audio(audio_path)
    pygame.mixer.music.load(test_bird_song_file)
    
    print(f"Round {score+1}:")

    while True:

        user_input = input(">> ").lower().strip()

        # --- COMMANDS ---

        if user_input == 'q':
            pygame.mixer.music.stop()
            print(f'Final score = {score}')
            write_score(username, score, "data/scores.json", "data/highscores.json")
            # reveal_answers(birds_tested)
            break 

        elif user_input == 'p':
            print('Bird singing 🎶 🦜')
            pygame.mixer.music.play()
        
        elif user_input == 'admin':
            print(birds_tested)

        elif user_input == 'help':
            print_commands(corvids)

        elif user_input == 'birds':
            print(f"Possible answers are: {birds}")

        # need to make this only pressable sometimes... or have confim input
        elif user_input == "r":
            score = 0
            birds_tested.clear()
            print(f"Score = {score}")
            test_bird, test_bird_song_file = get_bird_and_audio(audio_path)
            pygame.mixer.music.load(test_bird_song_file)
            print(f'Round {score+1}:')

        elif user_input == test_bird:
            pygame.mixer.music.stop()
            score += 1
            print('Correct!')
            test_bird, test_bird_song_file = get_bird_and_audio(audio_path)
            pygame.mixer.music.load(test_bird_song_file)
            print(f'Round {score+1}:')

        # this counts any typed letters that are not captured by above ifs
        # must be kept as the final check for this reason
        # is there a reason this isn't just an 'else'?
        elif user_input.isalpha():
            pygame.mixer.music.stop()
            print(f'Not quite, that one was a {test_bird}')
            print(f"""
                  Enter 'p' to hear the sound again
                  Enter 'r' to play again
                  Enter 'q' to quit
                  """)
                            #   Enter 'more' to hear further examples of a {test_bird}


    #%%

if __name__ == "__main__":
    main()
