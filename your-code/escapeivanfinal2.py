# -*- coding: utf-8 -*-
"""
Created on Wed Oct 14 21:00:37 2020

@author: picav
"""

# -*- coding: utf-8 -*-
"""
Created on 14 Oct 2020

Escape Room Game

@author: Cinthya Blois, Daniela Oliveira and Ivan Picavet
"""
import time
#text to speech function
from gtts import gTTS 
from io import BytesIO
from pygame import mixer

def text_to_speech(text):
    language = "en"
    texttospeech = gTTS(text = text, lang = language, slow = False)
    mp3 = BytesIO()
    texttospeech.write_to_fp(mp3)
    mp3.seek(0)
    mixer.init()
    mixer.music.load(mp3)
    mixer.music.play()
    return mp3

# define function to call text_to_speech true
def call_text_to_speech(text):
    text_to_speech(text)
    return True
# define rooms and items

couch = {
    "name": "couch",
    "type": "furniture",
}

door_a = {
    "name": "door a",
    "type": "door",
}

key_a = {
    "name": "key for door a",
    "type": "key",
    "target": door_a,
}

piano = {
    "name": "piano",
    "type": "furniture",
}

game_room = {
    "name": "game room",
    "type": "room",
}

queen_bed = {
    "name": "queen bed",
    "type": "furniture",
}

door_b = {
    "name": "door b",
    "type": "door",
}

door_c = {
    "name": "door c",
    "type": "door",
}

key_b = {
    "name": "key for door b",
    "type": "key",
    "target": door_b,
}

bedroom_1 = {
    "name": "bedroom_1",
    "type": "room",
}

door_d = {
    "name": "door d",
    "type": "door",
}

double_bed = {
    "name": "double bed",
    "type": "furniture",
}

dresser = {
    "name": "dresser",
    "type": "furniture",
}

key_c = {
    "name": "key for door c",
    "type": "key",
    "target": door_c,
}

key_d = {
    "name": "key for door d",
    "type": "key",
    "target": door_d,
}

bedroom_2 = {
    "name": "bedroom_2",
    "type": "room",
}

dining_table = {
    "name": "dining table",
    "type": "furniture",
}

living_room = {
    "name": "living_room",
    "type": "room",
}

outside = {
  "name": "outside"
}

all_rooms = [game_room, bedroom_1, bedroom_2, living_room, outside]

all_doors = [door_a, door_b, door_c, door_d]

# define which items/rooms are related

object_relations = {
    "game room": [couch, piano, door_a],
    "piano": [key_a],
    "outside": [door_d],
    "door a": [game_room, bedroom_1],
    "bedroom_1": [door_a, door_b, door_c, queen_bed],
    "queen bed": [key_b],
    "door b": [bedroom_1, bedroom_2],
    "bedroom_2": [door_b, double_bed, dresser],
    "double bed": [key_c],
    "dresser": [key_d],
    "door c": [bedroom_1, living_room],
    "living_room": [door_c, door_d, dining_table],
    "door d": [living_room, outside],
}

# define game state. Do not directly change this dict. 
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This 
# way you can replay the game multiple times.

INIT_GAME_STATE = {
    "current_room": game_room,
    "keys_collected": [],
    "target_room": outside
}

def linebreak():
    """
    Print a line break
    """
    print("\n\n")

def start_game():
    """
    Start the game
    """
    text1 = "to be replaced"
    print(text1)
    text_to_speech(text1)
    time.sleep(1)
    play_room(game_state["current_room"])

def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either 
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if(game_state["current_room"] == game_state["target_room"]):
        text2 = "Congrats! You escaped the room"
        print(text2)
        text_to_speech(text2)
        time.sleep(1)
        text_to_sleep("and now please donate 5 euros to buy this script. paypal and cash acceoted")
    else:
        text3= "You are now in " + room["name"]
        print(text3)
        text_to_speech(text3)
        time.sleep(3)
        text4 = "What would you like to do? Type 'explore' or 'examine'?"
        text_to_speech(text4)
        intended_action = input(text4).strip()
        
        if intended_action == "explore":
            explore_room(room)
            play_room(room)
        elif intended_action == "examine":
            text6 = "What would you like to examine?"
            text_to_speech(text6)
            examine_item(input(text6).strip())
            
        else:
            error_text1 = "Not sure what you mean. Type 'explore' or 'examine'."
            print(error_text1)
            text_to_speech(error_text1)
            time.sleep(3)
            play_room(room)
        linebreak()

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    text5 = "You explore the room. This is " + room["name"] + ". You find " + ", ".join(items)
    print(text5)
    text_to_speech(text5)
    time.sleep(6)

def get_next_room_of_door(door, current_room):
    """
    From object_relations, find the two rooms connected to the given door.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[door["name"]]
    for room in connected_rooms:
        if(not current_room == room):
            return room

def examine_item(item_name):
    """
    Examine an item which can be a door or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a door. Tell player if key hasn't been 
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a door, then check if it contains keys.
    Collect the key if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None
    
    for item in object_relations[current_room["name"]]:
        if(item["name"] == item_name):
            output = "You examine " + item_name + ". "
            text_to_speech(output)
            time.sleep(2)
            if(item["type"] == "door"):
                have_key = False
                for key in game_state["keys_collected"]:
                    if(key["target"] == item):
                        have_key = True
                if(have_key):
                    output += "You unlock it with a key you have."
                    textoutput2 = "You unlock it with a key you have."
                    text_to_speech(textoutput2)
                    time.sleep(2)
                    next_room = get_next_room_of_door(item, current_room)
                else:
                    output += "It is locked but you don't have the key."
                    text_to_speech("It is locked but you don't have the key.")
                    time.sleep(3)
            else:
                if(item["name"] in object_relations and len(object_relations[item["name"]])>0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["keys_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                    textoutput1 = "You find " + item_found["name"] + "."
                    text_to_speech(textoutput1)
                    time.sleep(3)
                else:
                    output += "There isn't anything interesting about it."
                    text_to_speech("There isn't anything interesting about it.")
                    time.sleep(2)
                    
            print(output)
            break

    if(output is None):
        print("The item you requested is not found in the current room.")
        text_to_speech("The item you requested is not found in the current room.")
        time.sleep(2)
    
    if(next_room and call_text_to_speech("Do you want to go to the next room? Enter 'yes' or 'no'")==True and input("Do you want to go to the next room? Enter 'yes' or 'no'").strip()== "yes"):        
        play_room(next_room)
    else:
        play_room(current_room)

game_state = INIT_GAME_STATE.copy()

start_game()