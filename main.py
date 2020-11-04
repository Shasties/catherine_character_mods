#!/usr/bin/python3
import os
import re
import tkinter as tk
from tkinter import ttk
from shutil import copyfile

# Convenient logic for transitioning between name & files
def translate_character(name):
    characters = {
            "P1": os.path.join("14","c14_00.nif"),
            "P2": os.path.join("15","c15_00.nif"),
            "Pink Sheep": os.path.join("16","c16_00.nif"),
            "Vincent (Boxers)": os.path.join("02","c02_00.nif"),
            "Vincent (Shirt)": os.path.join("02","c02_16.nif"),
            "The Prince": os.path.join("13","c13_00.nif"),
            "Sheep": os.path.join("21","c21_00.nif"),
            "Crazy Sheep": os.path.join("22","c22_00.nif"),
            "Spear Sheep": os.path.join("23","c23_00.nif"),
            "Fat Sheep": os.path.join("23","c23_01.nif"), 
            "Club Sheep": os.path.join("24","c24_00.nif"),
            "Axe Sheep": os.path.join("25","c25_00.nif"), 
            "Blue Sheep": os.path.join("14","c14_00.nif.bak"),
            "Orange Sheep": os.path.join("15","c15_00.nif.bak"),
            }
    return characters[name]

def translate_block_textures(skin,block):
    type_prefix = {
            "Original": "c001",
            "Rapunzel": "c010",
            "Babel": "c020",
            "Placeholder": "c100"
            }
    blocks = {
            "White": ["000","001","002","003"],
            "Cracked": ["004"],
            "Heavy": ["005"],
            "Immovable": ["006"],
            "Ice": ["007"],
            "Explosive I": ["008"],
            "Explosive II": ["009"],
            "Mystery": ["010"],
            "Spike": ["011"],
            "Black Hole": ["012"],
            "Monster": ["013"]
            }

    suffixes = [".nif",".kfm",".kf"]

    return_files = []
    for b in blocks[block]:
        for s in suffixes:
            return_files.append(type_prefix[skin]+"_"+b+""+s)

    return return_files
    #return [type_prefix[skin]+"_"+b for b in blocks[block]+""+s for s in suffixes]

def make_backup(backup_file):
    if not os.path.exists(backup_file):
        original_file = backup_file.split(".bak")[0]
        copyfile(original_file,backup_file)

def applyConfig(entry_widget,player_dic,block_dic):
    steam_path = entry_widget.get()
    steam_path = os.path.normpath(steam_path)
    character_path = os.path.join(steam_path,"steamapps","common","CatherineClassic","data","character")

    p1_path = os.path.join(character_path,translate_character(player_dic['Player 1'].get()))
    p2_path = os.path.join(character_path,translate_character(player_dic['Player 2'].get()))

    # Check for backups
    make_backup(os.path.join(character_path,translate_character("Blue Sheep")))
    make_backup(os.path.join(character_path,translate_character("Orange Sheep")))

    # Replace characters
    p1_play = os.path.join(character_path,translate_character("P1"))
    p2_play = os.path.join(character_path,translate_character("P2"))
    copyfile(p1_path,p1_play)
    copyfile(p2_path,p2_play)

    # Changing blocks
    block_path = os.path.join(steam_path,"steamapps","common","CatherineClassic","data","puzzle","object")

    for key in block_dic:
        # Check for backups of file
        for original_file in translate_block_textures("Original",key):
            make_backup(os.path.join(block_path,original_file+".bak"))

        # Perform copy
        for from_file in translate_block_textures(block_dic[key].get(),key):
            from_file = os.path.join(block_path,from_file)
            to_file = re.sub("c..._","c001_",from_file)
            
            # i.e. c001_001.nif.bak > c001_001.nif
            if block_dic[key].get() == "Original":
                from_file=from_file+".bak"
            copyfile(from_file,to_file)


def set_constant_frame(constant_frame,player_dic,block_dic):
    config_frame = tk.Frame(constant_frame)

    # General Config (Steam Path)
    library_path_entry = tk.Entry(config_frame,width=50)
    library_path_label = tk.Label(config_frame,text="Steam library path")
    library_path_label.pack(side='left')
    library_path_entry.pack(side='left')
    library_path_entry.insert(0,"C:\Program Files\Steam")

    # buttons
    button_frame = tk.Frame(constant_frame)
    do_button = tk.Button(button_frame,text='Apply Config',width=25,height=5,command=lambda: applyConfig(library_path_entry,player_dic,block_dic))

    # Packing
    config_frame.pack(side='top')
    button_frame.pack(side='bottom')
    do_button.pack(side='left')

def set_character_tab(parent_frame,selected_character):
    players = ["Player 1", "Player 2"]
    playable_characters = ["Blue Sheep", "Orange Sheep", "Pink Sheep", "Vincent (Boxers)", "Vincent (Shirt)", "The Prince", "Sheep", "Crazy Sheep", "Spear Sheep", "Fat Sheep", "Club Sheep", "Axe Sheep"]
    config_frame = tk.Frame(parent_frame)
    
    # drop-down generation
    for player in players:
        player_frame = tk.Frame(config_frame)
        tk.Label(player_frame,text=player).pack()
        variable = tk.StringVar(player_frame)
        selected_character[player] = variable
        variable.set(playable_characters[1] if player == 'Player 2' else playable_characters[0])
        tk.OptionMenu(player_frame,variable,*playable_characters).pack()
        player_frame.pack()
        
    # packing
    display_frame = tk.Frame(parent_frame)
    config_frame.pack(side='left')
    display_frame.pack(side='right')


def set_block_tab(parent_frame,block_select):
    blocks = ["White", "Cracked", "Heavy", "Immovable", "Ice", "Explosive I", "Explosive II", "Mystery", "Spike", "Black Hole", "Monster"]
    skins_most = ["Original","Rapunzel","Babel","Placeholder"]
    # not all blocks have a Rapunzel variant
    skins_some = ["Original","Babel","Placeholder"]
    config_frame = tk.Frame(parent_frame)

    # drop-down generation
    for block in blocks:
        block_frame = tk.Frame(config_frame)
        tk.Label(block_frame,text=block).pack()
        skins_to_use = skins_most
        if "Heavy" in block or "Explosive" in block or "Mystery" in block or "Spike" in block or "Monster" in block:
            skins_to_use = skins_some
        variable = tk.StringVar(block_frame)
        block_select[block] = variable
        variable.set(skins_to_use[0])
        tk.OptionMenu(block_frame,variable,*skins_to_use).pack()
        block_frame.pack()

    # packing
    display_frame = tk.Frame(parent_frame)
    display_frame = tk.Frame(parent_frame)
    config_frame.pack(side='left')
    display_frame.pack(side='right')

def set_changing_frame(changing_frame,player_select,block_select):
    tabControl = ttk.Notebook(changing_frame)
    character_tab = ttk.Frame(tabControl)
    set_character_tab(character_tab,player_select)
    block_tab = ttk.Frame(tabControl)
    set_block_tab(block_tab,block_select)
    tabControl.add(character_tab, text='Characters')
    tabControl.add(block_tab, text='Blocks')
    tabControl.pack(expand=1, fill="both")

def gui():
    # init
    window = tk.Tk()
    window.title('Catherine Helper')
    constant_frame = tk.Frame(master=window)
    changing_frame = tk.Frame(master=window)
    player_select = {}
    block_select = {}
    # move frame logic out of gui()
    set_constant_frame(constant_frame,player_select,block_select)
    set_changing_frame(changing_frame,player_select,block_select)

    # packing & running
    constant_frame.pack(side='left')
    changing_frame.pack(side='left')
    window.mainloop()

if __name__ == "__main__":
    try:
        gui()
    except Exception as e:
        print(e)
        input("See error message")
