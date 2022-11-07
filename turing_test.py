import serial
import time
import pandas as pd
from os import chdir, listdir, getcwd, path
import ctypes
import keyboard

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

arduino = serial.Serial(port='COM7', baudrate=9600)
time.sleep(5)


def speak(phrase):
    arduino.write(bytes(phrase, 'utf-8'))
    while True:
        response = str(arduino.readline())
        if response[2] != "!":
            print(response[2], end="")
        else:
            print('')
            break


def generate_phrase():
    phrase = 'hello world'
    return phrase


def preset_dialogue(file, names):
    name = names[0]
    data = pd.read_csv(file)
    dialogue = list(data['dialogue'])
    for phrase in dialogue:
        print(f'Robot {name}', end=": ")
        speak(phrase)
        if name is names[0]:
            name = names[1]
        else:
            name = names[0]


def chatterbot_user_talk():
    cwd = getcwd()

    bot = ChatBot("Frankenstein")
    trainer = ListTrainer(bot)
    file = path.join(cwd, 'frankenstein.csv')
    data = pd.read_csv(file)
    dialogue = list(data['dialogue'])
    trainer.train(dialogue)

    while True:
        query = input("> ")
        if query == 'q':
            break
        else:
            print(f"Robot: {bot.get_response(query)}")


def chatterbot_talk():
    cwd = getcwd()
    v_folder = path.join(cwd, 'VFrankenstein')
    a_folder = path.join(cwd, 'AFrankenstein')

    chdir(v_folder)
    vfrankenstein = ChatBot("VFrankenstein")
    vfrankenstein_trainer = ListTrainer(vfrankenstein, read_only=True)
    files = listdir(v_folder)
    for f in files:
        if 'csv' in f:
            file = path.join(v_folder, f)
            data = pd.read_csv(file)
            dialogue = list(data['dialogue'])
            vfrankenstein_trainer.train(dialogue)

    chdir(a_folder)
    afrankenstein = ChatBot("AFrankenstein")
    afrankenstein_trainer = ListTrainer(afrankenstein, read_only=True)
    files = listdir(a_folder)
    for f in files:
        if 'csv' in f:
            file = path.join(a_folder, f)
            data = pd.read_csv(file)
            dialogue = list(data['dialogue'])
            afrankenstein_trainer.train(dialogue)

    turn_screen_off('')

    query = 'death'
    while True:
        response = vfrankenstein.get_response(query)
        print('frankenbot', end=": ")
        speak(str(response))
        query = afrankenstein.get_response(response)
        print('frankenbotjr', end=": ")
        speak(str(query))
        if keyboard.is_pressed('x'):
            turn_screen_on('')


def turn_screen_off(x):
    ctypes.windll.user32.SendMessageW(65535, 274, 61808, 2)


def turn_screen_on(x):
    ctypes.windll.user32.SendMessageW(65535, 274, 61808, -1)


if __name__ == '__main__':
    keyboard.on_release(turn_screen_off)
    chatterbot_talk()
    time.sleep(1)
    turn_screen_on('')
    #preset_dialogue(file, ['A','B'])
    #speak(generate_phrase())


