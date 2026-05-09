#%%

from playsound3 import playsound

#%%

def main():

    #%%

    # print("Hello from bird-game!")

    score = 0

    playsound('audio/wren1.wav')

    bird = 'wren'

    user_bird = input()

    if user_bird == bird:
        score += 1
        print('yeah class mate')

    else:
        score = 0
        print(f'does that sound like a {user_bird} you plonker')

    print(f'Score = {score}')


    #%%


if __name__ == "__main__":
    main()
