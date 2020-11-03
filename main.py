#!/usr/bin/python3
import os
import tkinter as tk
from tkinter import ttk
from shutil import copyfile

def translate_character(name):
    characters = {
            "1": os.path.join("14","c14_00.nif"),# Blue Sheep
            "2": os.path.join("15","c15_00.nif"),# Orange Sheep
            "3": os.path.join("16","c16_00.nif"),# Pink Sheep
            "4": os.path.join("02","c02_00.nif"),# Vincent boxers
            "5": os.path.join("02","c02_16.nif"),# Vincent Shirt
            "6": os.path.join("13","c13_00.nif"),# Rapunzel Prince
            "7": os.path.join("21","c21_00.nif"),# Standard Sheep
            "8": os.path.join("22","c22_00.nif"),# Crazy Sheep
            "9": os.path.join("23","c23_00.nif"),# Spear Sheep
            "10": os.path.join("23","c23_01.nif"),# Fat Sheep
            "11": os.path.join("24","c24_00.nif"),# Slightly Demonic Sheep
            "12": os.path.join("25","c25_00.nif"),# Demonic Sheep
            "98": os.path.join("14","c14_00.nif.bak"),# Blue Sheep
            "99": os.path.join("15","c15_00.nif.bak"),# Orange Sheep
            }
    return characters[name]

def translate_block_textures(name):
    pass
    # Original
    # Rapunzel
    # Babel
    # Debug

def character_prompt(character_path,player):
    char = 0
    while int(char) < 1 or int(char) > 12:
        char = input("Select "+player+"'s character (Numbers 1-12 only): ")
    if char == "1":
        char = "98"
    if char == "2":
        char = "99"
    return os.path.join(character_path,translate_character(char))

def make_backup(backup_file):
    if not os.path.exists(backup_file):
        original_file = backup_file.split(".bak")[0]
        copyfile(original_file,backup_file)

def main():
    # Get Steam library path
    steam_path = input("Enter the path to your Steam library (i.e. C:\Program Files\Steam): ")
    steam_path = os.path.normpath(steam_path)

    # Combine relative path to characters
    character_path = os.path.join(steam_path,"steamapps","common","CatherineClassic","data","character")

    print('''
    Character Selection: \n 
    1: Blue Sheep\n
    2: Orange Sheep\n
    3: Pink Sheep\n
    4: Vincent (Boxers)\n
    5: Vincent (Shirt)\n
    6: The Prince\n
    7: Sheep\n
    8: Crazy Sheep\n
    9: Spear Sheep\n
    10: Fat Sheep\n
    11: Slight Demonic Sheep\n
    12: Demonic Sheep
    ''')

    # Prompt for characters
    p1_path = character_prompt(character_path,"P1")
    p2_path = character_prompt(character_path,"P2")

    # Check for backups
    make_backup(os.path.join(character_path,translate_character("98")))
    make_backup(os.path.join(character_path,translate_character("99")))

    # Replace characters
    p1_play = os.path.join(character_path,translate_character("1"))
    p2_play = os.path.join(character_path,translate_character("2"))
    copyfile(p1_path,p1_play)
    copyfile(p2_path,p2_play)
    input("Finished")

def set_constant_frame(constant_frame):
    config_frame = tk.Frame(constant_frame)

    # General Config (Steam Path)
    library_path_entry = tk.Entry(config_frame,width=50)
    library_path_label = tk.Label(config_frame,text="Steam library path")
    library_path_label.pack(side='left')
    library_path_entry.pack(side='left')
    library_path_entry.insert(0,"C:\Program Files\Steam")

    # buttons
    button_frame = tk.Frame(constant_frame)
    undo_button = tk.Button(button_frame,text='Restore Defaults',width=25,height=5)
    do_button = tk.Button(button_frame,text='Apply Config',width=25,height=5)

    # Packing
    config_frame.pack(side='top')
    button_frame.pack(side='bottom')
    undo_button.pack(side='left')
    do_button.pack(side='left')

def set_character_tab(parent_frame):
    players = ["Player 1", "Player 2"]
    playable_characters = ["Blue Sheep", "Orange Sheep", "Pink Sheep", "Vincent (Boxers)", "Vincent (Shirt)", "The Prince", "Sheep", "Crazy Sheep", "Spear Sheep", "Fat Sheep", "Club Sheep", "Axe Sheep"]
    config_frame = tk.Frame(parent_frame)

    for player in players:
        player_frame = tk.Frame(config_frame)
        tk.Label(player_frame,text=player).pack()
        for character in playable_characters:
            tk.Radiobutton(player_frame,indicatoron=0,text=character).pack()
        player_frame.pack()
        
    # packing
    display_frame = tk.Frame(parent_frame)
    config_frame.pack(side='left')
    display_frame.pack(side='right')


def set_block_tab(parent_frame):
    blocks = ["White", "Cracked", "Heavy", "Immovable", "Ice", "Explosive I", "Explosive II", "Mystery", "Spike", "Black Hole", "Monster"]
    skins_most = ["Original","Rapunzel","Babel","Placeholder"]
    # not all blocks have a Rapunzel variant
    skins_some = ["Original","Babel","Placeholder"]
    config_frame = tk.Frame(parent_frame)

    for block in blocks:
        block_frame = tk.Frame(config_frame,width=100)
        tk.Label(block_frame,text=block).pack()
        skins_to_use = skins_most
        if "Heavy" in block or "Explosive" in block or "Mystery" in block or "Black" in block:
            skins_to_use = skins_some
        for skin in skins_to_use:
            tk.Radiobutton(block_frame,text=skin,width=3).pack(side='left')
        block_frame.pack()

    # packing
    display_frame = tk.Frame(parent_frame)
    display_frame = tk.Frame(parent_frame)
    config_frame.pack(side='left')
    display_frame.pack(side='right')

def set_changing_frame(changing_frame):
    tabControl = ttk.Notebook(changing_frame)
    character_tab = ttk.Frame(tabControl)
    set_character_tab(character_tab)
    block_tab = ttk.Frame(tabControl)
    set_block_tab(block_tab)
    tabControl.add(character_tab, text='Characters')
    tabControl.add(block_tab, text='Blocks')
    tabControl.pack(expand=1, fill="both")

def gui():
    window = tk.Tk()
    window.title('Catherine Helper')
    constant_frame = tk.Frame(master=window)
    changing_frame = tk.Frame(master=window,width=100)
    set_constant_frame(constant_frame)
    set_changing_frame(changing_frame)

    constant_frame.pack(side='left')
    changing_frame.pack(side='right')
    #init_tabs(window)
#    label = tk.Label(
#            text="Hello",
#            foreground="white",
#            background="black"
#            )
#    do_button = tk.Button(
#            text='Apply Config',
#            width=25,
#            height=5,
#            )
#    undo_button = tk.Button(
#            text='Restore Defaults',
#            width=25,
#            height=5,
#            )
#    entry = tk.Entry(width=50)
#    label = tk.Label(entry,text="Steam library path")
#    entry.pack(side='top')
#    label.pack(side='left')
#    entry.insert(0,"C:\Program Files\Steam")
#    do_button.pack()
#    undo_button.pack()
    window.mainloop()

if __name__ == "__main__":
    try:
        #main()
        gui()
    except Exception as e:
        print(e)
        input("See error message")
