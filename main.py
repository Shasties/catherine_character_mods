import os
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

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)
        input("See error message")
