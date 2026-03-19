import random
import time

# Global variables
character_name = ""
weapon = 0
armor = 0
hitpoints = 30
inventory = []

dungeon = []
visited = []

enemies_choice = ["cultist", "robber", "goblin"]
enemy_type = ""
enemies = []
room_modifier = []

play = True

lwidth = 80

room_types = {
    0: "cell",
    1: "storage room",
    2: "smithy",
    3: "kitchen",
    4: "library",
    5: "barracks",
    1024: "boss room"
}

weapon_types = {
    0: "unarmed",
    1: "dagger",
    2: "club",
    3: "sword",
    4: "cursed sword",
    5: "magic sword"
}
weapon_damage = {
    0: [0, 2],
    1: [1, 4],
    2: [1, 6],
    3: [2, 8],
    4: [2, 8],
    5: [2, 8]
}

armor_types = {
    0: "no armor",
    1: "thick cloth",
    2: "leather vest",
    3: "chainmail",
    4: "mithril mail",
    5: "cursed chainmail"
}

armor_value = {
    0: 0,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 2
}

item_ids = {
    0: "health potion",
    1: "acid potion",
    10: "golden crown",
    11: "feast leftovers",
    12: "magic book"
}

enemy_fighters = {
    "robber": [8, [1, 4]],
    "highwayman": [8, [1, 4]],
    "green goblin": [8, [1, 4]],
    "black goblin": [12, [2, 4]],
    "low cultist": [12, [2, 4]],
    "high cultist": [12, [2, 4]],
    "mimic": [16, [3, 5]],
    "hobgoblin": [20, [3, 5]],
    "wizard": [20, [3, 5]],
    "bandit lord": [20, [3, 5]],
    "wendigo": [25, [3, 6]],
    "minotaur": [30, [3, 6]],
    "cave dragon": [40, [4, 7]],
}

# Encounters


def initial_encounter():
    """
    interact function for the initial room.
    called by the interact function
    Input: None
    Return: result: -2 for player death, -1 for quit, >= 0 for success
    """

    global character_name
    global enemy_type
    global weapon

    print_sleep(
        "As you come to your senses you notice you are not alone in the room."
    )
    print_sleep(
        f"A {enemy_type} is standing next to you with "
        f"{"its" if enemy_type == "Goblin" else "his"} back to you."
    )

    option = [f"Punch the {enemy_type}.", "Pretend being asleep."]
    action = select(option)

    if action == 2:
        print_sleep("You pretend being asleep but squint at the foe.")
        print_sleep(
            f"The {enemy_type} is slowly turning to you,"
            " holding a nasty dagger in one hand."
        )
        print_sleep(
            f"A bloodthirsty look in "
            f"{"its" if enemy_type == "Goblin" else "his"} gleaming eyes."
        )

        action = 0
        option = [f"Punch the {enemy_type}.", "Continue pretend being asleep."]
        action = select(option)

        if action == 2:
            print_sleep(f"The {enemy_type} rams the dagger into your chest.")
            print_sleep(
                "You feel extraordinary pain before everything goes black."
            )
            return dead("Due to a stab wound to the chest.")

    if action == 1:
        print_sleep(f"You punch the {enemy_type}.")
        print_sleep(
            f"{"It" if enemy_type == "Goblin" else "He"}"
            " falls over unconcious, a dagger clanking on the floor."
        )

    if action == -1:
        # quit
        return -1

    return 1


def special_boss_encounter(encounter: str):
    """
    interact function for the boss monsters.
    called by the interact function
    Input: None
    Return: result: -2 for player death, -1 for quit, >= 0 for success
            enemy: updated enemy string
    """
    enemy = encounter
    result = 1
    if encounter == "wendigo" and 11 in inventory:
        print_sleep(
            "The wendigo starts sniffing."
            " Suddenly it doesn't look aggressive anymore."
        )
        print_sleep("After some moents it starts pointing at your bag.")
        print_sleep(
            "Maybe it wants the leftovers of the feats you took with you."
        )
        action = select(["Give the food to the wendigo.", "Keep the food."])
        if action < 0:
            result = action
        elif action == 1:
            print_sleep(
                "The wendigo starts munching on the food."
                " It completely ignores you."
            )
            print_sleep("You can escape the dungeon!")
            enemy = None
        else:
            print_sleep(
                "The wendigo is angry that you wouldn't give it the food."
            )

    elif encounter == "minotaur" and 10 in inventory:
        print_sleep(
            "As the minotaur sees the crown on your head it halts."
        )
        print_sleep(
            "In a raspy voice it says: "
            "\"The king may pass. I will not attack\"."
        )
        print_sleep(
            "The minotaur bows it's head and puts down it's weapon."
        )
        action = select(
            ["Accept the offer of non-violence.",
             "Fight the monster."]
        )
        if action < 0:
            result = action
        elif action == 1:
            print_sleep(
                "The minotaur keeps motionless as you pass through the room."
            )
            print_sleep("You can escape the dungeon!")
            enemy = None
        else:
            print_sleep(
                "\"As you wish.\" the minotaur says."
                " This fight will be to the death."
            )

    elif encounter == "cave dragon" and 12 in inventory:
        print_sleep("You are frozen in fear when you see the dragon.")
        print_sleep("Then you hear a voice from your bag: \"Let me help!\".")
        print_sleep(
            "The book you found earlier bursts out of "
            "your bag as you open it and flies to the dragon."
        )
        print_sleep(
            "\"Master! Please do not hurt this mortal."
            " It saved me.\" The book says."
        )
        action = select(
            ["Offer the book to the dragon.",
             "Keep the book."]
        )
        if action < 0:
            result = action
        elif action == 1:
            print_sleep("You feel the amusement emitting from the dragon.")
            print_sleep(
                "Even though it didn't say a word"
                " you feel like you are safe to pass.."
            )
            print_sleep("You can escape the dungeon!")
            enemy = None
        else:
            print_sleep("The dragon roars in anger.")
    return result, enemy


def magic_chest_encounter():
    """
    interact function for the storage room encounter.
    called by the interact function
    Input: None
    Return: result: -2 for player death, -1 for quit, >= 0 for success
            enemy: updated enemy string
    """
    enemy = None
    result = 1
    print_sleep(
        "In one corner of the room you can see a gleaming chest."
    )
    print_sleep(
        "This seems odd. Most of the boxes and "
        "barrels were opened but this looks untouched."
        )
    action = select(["Open the chest.", "Ignore the chest."])
    if action == 1:
        print_sleep("As soon as you touch the chest it opens by itself.")
        print_sleep("Startled you jump back as the chest reveals:")
        rand_enc = random.randint(1, 10)
        if rand_enc == 1:
            print_sleep(
                "A goblin was hiding in the box "
                "and jumps at you ready for a fight."
            )
            enemy = "green goblin"
        elif rand_enc < 4:
            print_sleep("You find a golden crown in the chest.")
            print_sleep("It seems valuable so you decide to take it.")
            add_item(10)
        elif rand_enc < 9:
            print_sleep("You find a gleaming chainmail in the chest.")
            print_sleep(
                "It is lighter than normal metal but seems very sturdy."
            )
            change_armor(4)
        else:
            print_sleep("The chest transforms in front of your eyes.")
            print_sleep("It's a mimic! Fight for your life!")
            enemy = "mimic"
    elif action < 0:
        result = action
    else:
        print_sleep(
            "You decide to ignore the chest and focus on the rest of the room."
        )
    return result, enemy


def magic_sword_encounter():
    """
    interact function for the smithy encounter.
    called by the interact function
    Input: None
    Return: result: -2 for player death, -1 for quit, >= 0 for success
            enemy: updated enemy string
    """
    enemy = None
    result = 1
    print_sleep("On the anvil you see a gleaming sword.")
    print_sleep("It looks very sharp and emmits a strange glow.")
    action = select(["Take the sword.", "Ignore the sword."])
    if action == 1:
        rand_enc = random.randint(1, 10)
        if rand_enc < 2:
            print_sleep(
                "As you grab the sword you feel a drain on your energy."
            )
            change_weapon(4)
        elif rand_enc < 4:
            print_sleep("The sword vanishes in front of your eyes.")
            print_sleep("It was just an illusion.")
            print_sleep("A cultist set a trap for you.")
            enemy = "high cultist"
        else:
            print_sleep("As you take the sword you the might of this weapon.")
            change_weapon(5)
    elif action < 0:
        result = action
    else:
        print_sleep(
            "You decide to ignore the sword and focus on the rest of the room."
        )
    return result, enemy


def talking_book_encounter():
    """
    interact function for the library encounter.
    called by the interact function
    Input: None
    Return: result: -2 for player death, -1 for quit, >= 0 for success
            enemy: updated enemy string
    """
    global hitpoints
    enemy = None
    result = 1

    print_sleep("As you look around the library you hear some noise.")
    print_sleep(
        "Searching for the source of the sound"
        " you find a book which is chained shut."
    )
    action = select(["Open the book.", "Ignore the book."])
    if action == 1:
        rand_enc = random.randint(1, 10)
        if rand_enc < 2:
            print_sleep("The book opens it's pages showing fangs.")
            print_sleep("It's a mimic! Fight for your life!")
            enemy = "mimic"
        elif rand_enc < 5:
            print_sleep("The book can talk!")
            print_sleep(
                "It thanks you for freeing it and "
                "asks you to leave it alone in exchange for healing."
            )
            hitpoints = 30
            print_sleep("*** You are fully healed.***")
        else:
            print_sleep("The book can talk!")
            print_sleep(
                "It asks you to take it with you"
                " and promisses it will be helpful in the future."
            )
            add_item(12)
    elif action < 0:
        result = action
    else:
        print_sleep(
            "You decide to ignore the book and focus on the rest of the room."
        )
    return result, enemy


def armory_encounter():
    """
    interact function for the armory encounter.
    called by the interact function
    Input: None
    Return: result: -2 for player death, -1 for quit, >= 0 for success
            enemy: updated enemy string
    """
    enemy = None
    result = 1

    print_sleep("You find a collection of weapons and armor.")
    action = select(["Take the equipment.", "Leave it."])
    if action == 1:
        rand_enc = random.randint(1, 10)
        if rand_enc < 2:
            print_sleep(
                "As you try to fit armor pieces you suddenly feel unwell."
            )
            change_armor(5)
        elif rand_enc < 4:
            print_sleep(
                "Unfortunately the pieces only looked "
                "usable on first glance but are completely rotten."
            )
            print_sleep(
                "Metal rusted, straps falling"
                " off and dull edges on the weapons."
            )
            print_sleep("What a disapointment.")
        elif rand_enc < 6:
            print_sleep("You find a nice sword in the collection.")
            change_weapon(3)
        elif rand_enc < 8:
            print_sleep("You find usable chainmail in the collection.")
            change_armor(3)
        else:
            print_sleep(
                "You find a good sword and chainmail in the collection."
            )
            change_weapon(3)
            change_armor(3)
    elif action < 0:
        result = action
    else:
        print_sleep(
            "You decide to ignore the equipment, it looked like trash anyway."
        )

    return result, enemy


# Game functions


def dead(cause: str):
    """
    Small function to display the Death message
    including the cause
    Input: cause - string describing the cause of death
    Return: -2 (player death result value)
    """
    global character_name
    print_sleep(f"{character_name} died in the Dungeon.")
    print_sleep(f"{cause}")
    print_sleep("=" * lwidth)
    return -2


def select(options):
    """
    This function is used for inputs of the player.
    It will display the options in a input text
    Input: list of strings which are options for the input.
    Return: integer value of the chosen option
    """
    global play
    text = ""
    print_sleep("What do you want to do?")
    # Build input command text from provided list of strings
    for idx in range(0, len(options)):
        text = text + str(idx + 1) + ". " + options[idx] + "\n"
    selection = 0
    while True:
        # Endless loop until valid input is given
        choice = input(text)
        print_sleep("")
        if choice.lower() == "quit":
            # Quit command to close the game
            play = False
            return -1
        if choice.isnumeric():
            # Numerical command is valid if int 0 < input <= amount of choices
            selection = int(choice)
            if selection in range(0, len(options) + 1):
                return selection
        print_sleep("This is not a valid option.")


def room_choice(current_step: int):
    """
    This function is for the selection of the next room
    or step in the corridor
    player can choose a room left or rigth or continue on
    expects the current progress step as input
    returns the chosen room and current progress step
    Input: current_step the game progression (steps in corridor) integer
    Return: next_room room identifier integer, current_step
    """
    global dungeon
    next_room = 0

    while next_room == 0:
        print_sleep("You leave the room and find yourself in a corridor.")
        print_sleep("Left and right of you are doors.")

        boss_ahead = current_step == int(len(dungeon) / 2) - 2
        straight = (
            f"Straight ahead is "
            f"{"a door with a skull" if boss_ahead else "a long corridor"}."
        )
        print_sleep(straight)

        selection = select(["Left", "Right", "Straight"])

        # we count corridor steps and choose available rooms left and right
        # from dungeon map according to number of steps

        if selection == -1:
            # quit command received, return values don't matter
            return next_room, current_step
        elif selection == 1:
            next_room = current_step * 2 + 1
        elif selection == 2:
            next_room = current_step * 2 + 2
        elif selection == 3:
            # straight, go further down the corridor
            if current_step == int(len(dungeon) / 2 - 2):
                # boss room = last entry in list
                next_room = -1
            else:
                current_step += 1
                print_sleep("=" * lwidth)
        else:
            print_sleep("Error: Unexpected return value from room selection")

    print_sleep("=" * lwidth)

    return next_room, current_step


def search_room(current_room: int):
    """
    Function which handles the search interaction
    Input: current_room the room id in the dungeon
    Return: result: -2 for player death, -1 for quit, >= 0 for success
    """
    action = select(["Search the room.", "Continue on."])
    result = 1
    if action < 0:
        return action
    if action == 1:
        # search
        print_sleep(f"You search the {room_types[current_room]}")
        # randomize loot
        loot = random.randint(1, 10)
        if current_room == 0:
            # starting room always has dagger
            result = change_weapon(1)
        elif loot < 6:
            # 50% chance to find nothing
            print_sleep("Unfortunately you didn't find anything.")
        elif loot < 9:
            # 30% chance to find potion
            print_sleep("You found a potion.")
            add_item(random.randint(0, 1))
        elif loot < 10:
            # 10% chance to find weapon
            result = change_weapon(random.randint(1, 3))
        else:
            # 10% chance to find armor
            result = change_armor(random.randint(1, 3))

    return result


def fight(enemy: str):
    """
    Function which handles the fight interaction
    Input: enemy as string variable
    Return: result: -2 for player death, -1 for quit, >= 0 for success
    """
    global hitpoints
    global weapon
    global weapon_types
    global weapon_damage
    global armor
    global armor_types
    global armor_value
    global enemy_fighters

    print_sleep("\n" + "/" * int(lwidth / 2) + "\\" * int(lwidth / 2))
    print_sleep(f"Get ready to fight {enemy}!")
    status = (
        f"Current Hitpoints: {hitpoints}"
        f"||  Weapon: {weapon_types[weapon]}"
        f"||  Armor: {armor_types[armor]}"
    )
    print_sleep(status)

    # get damage values from weapons and monsters list
    dmg_low = weapon_damage[weapon][0]
    dmg_high = weapon_damage[weapon][1]
    prot = armor_value[armor]

    enemy_hp = enemy_fighters[enemy][0]
    enemy_dmg_low = enemy_fighters[enemy][1][0]
    enemy_dmg_high = enemy_fighters[enemy][1][1]

    # Build options to select from, either fight or use item
    options = ["Fight!"]
    if 0 in inventory:
        options.append("Drink Healing Potion.")
    if 1 in inventory:
        options.append("Throw Acid Potion.")

    action = 0
    while action != 1 and enemy_hp > 0:
        # get inputs from input dialogue until
        # action = 1 fight start or enemy dead
        action = select(options)
        if action < 0:
            return action
        elif (action == 2):
            if 0 in inventory:
                print_sleep(
                    "You drink a healing potion before the fight starts."
                )
                hitpoints = min(30, hitpoints + 15)
                print_sleep(f"Current Hitpoints: {hitpoints}")
                inventory.remove(0)
                if 0 not in inventory:
                    options.remove("Drink Healing Potion.")
            else:
                print_sleep(
                    "You throw the acid potion. It deals heavy damage."
                )
                enemy_hp -= 15
                inventory.remove(1)
                if 1 not in inventory:
                    options.remove("Throw Acid Potion.")
        elif (action == 3):
            print_sleep(
                "You throw the acid potion. It deals heavy damage."
            )
            enemy_hp -= 15
            inventory.remove(1)
            if 1 not in inventory:
                options.remove("Throw Acid Potion.")

    while enemy_hp > 0:
        # automatic fight
        dmg = random.randint(dmg_low, dmg_high)
        print_sleep(f"You hit the {enemy} for {dmg} Damage.")
        enemy_hp -= dmg
        dmg_enemy = max(
            1,
            random.randint(enemy_dmg_low, enemy_dmg_high) - prot
        )
        hitpoints -= dmg_enemy
        enemy_hit = (
            f"{enemy.capitalize()} hits you for for {dmg_enemy} Damage."
            f"You have {hitpoints} left."
        )
        print_sleep(enemy_hit)
        if hitpoints <= 0:
            print_sleep("/" * int(lwidth / 2) + "\\" * int(lwidth / 2) + "\n")
            return dead(f"Killed in combat by a {enemy}.")
    print_sleep(f"You killed the {enemy}.")
    print_sleep("/" * int(lwidth / 2) + "\\" * int(lwidth / 2) + "\n")
    return 1


def add_item(new_item: int):
    """
    On find of a new item this function add the item to the inventory
    Input: New item id integer
    Return: None
    """
    inventory.append(new_item)
    message = (
        "%" * lwidth + "\n"
        f"{item_ids[new_item].capitalize()} added to inventory."
        "\n" + "%" * lwidth
    )
    print_sleep(message)


def change_weapon(new_weapon: int):
    """
    On find of a new weapon this function will display
    current and new stats and give the choice to change
    Input: New weapon id integer
    Return: None
    """
    global weapon
    global weapon_types
    global weapon_damage

    # calculate improvement due to new weapon
    new_min, new_max = weapon_damage[new_weapon]
    old_min, old_max = weapon_damage[weapon]
    improvement = ((new_min - old_min) + (new_max - old_max)) / 2

    improve_message = (
        f"The new weapon {"improves" if improvement > 0 else "reduces"}"
        f" your damage by {improvement}."
    )

    print_sleep(f"You found a {weapon_types[new_weapon]}.")
    if "cursed" in weapon_types[weapon]:
        # old weapon is cursed
        print_sleep(
            "You are wielding a cursed weapon and cannot use another one."
        )

    elif "cursed" in weapon_types[new_weapon]:
        # new weapon is cursed
        print_sleep("The curse forces you to pick the weapon.")
        print_sleep(improve_message)
        weapon = new_weapon

    else:
        # show improvement and give option to use new weapon
        print_sleep(
            f"Currently you are "
            f"{"" if weapon == 0 else "wielding a "}"
            f"{weapon_types[weapon]}."
        )
        print_sleep(improve_message)
        action = select(["Keep my old weapon.", "Use the new weapon."])
        if action < 0:
            return action
        elif action == 2:
            weapon = new_weapon
            print_sleep(
                "%" * lwidth + "\n"
                f"{weapon_types[new_weapon].capitalize()} equipped."
                "\n" + "%" * lwidth
            )
    return 1


def change_armor(new_armor: int):
    """
    On find of a new armor this function will display
    current and new stats and give the choice to change
    Input: New armor id integer
    Return: None
    """
    global armor
    global armor_types
    global armor_value

    # calculate improvement due to new armor
    improvement = armor_value[new_armor] - armor_value[armor]
    improve_message = (
        f"The new armor {"improves" if improvement > 0 else "reduces"}"
        f" your protection by {improvement}."
    )

    print_sleep(f"You found a {armor_types[new_armor]}.")
    if "cursed" in armor_types[armor]:
        # old armor is cursed
        print_sleep(
            "You are wearing a cursed armor and cannot use another one."
        )

    elif "cursed" in armor_types[new_armor]:
        # new armor is cursed
        print_sleep(
            "The curse forces you to put on the new armor."
        )
        print_sleep(improve_message)
        armor = new_armor

    else:
        # show improvement and give option to use new armor
        print_sleep(
            f"Currently you are {"" if armor == 0 else "wearing a "}"
            f"{armor_types[armor]}."
        )
        print_sleep(improve_message)
        action = select(["Keep my old armor.", "Wear the new armor."])
        if action < 0:
            return action
        elif action == 2:
            armor = new_armor
            message = (
                "%" * lwidth + "\n"
                f"{armor_types[new_armor].capitalize()} equipped."
                "\n" + "%" * lwidth
            )
            print_sleep(message)
    return 1


def interact(encounter: str, enemy: str):
    """
    This function describe the encounters which happen in the current room.
    Bigger encounters might be moved to seperate functions
    Input: encounter and enemy as string variables
    Return: enemy as string variable, result:
    -2 for player death, -1 for quit, >= 0 for success
    """
    global enemy_type
    global inventory
    result = 1

    if encounter is None:
        print_sleep("There is an enemy in this room.")

    elif encounter == "initial":
        # Starter room
        result = initial_encounter()

    elif encounter == enemy and encounter is not None:
        # boss room
        if encounter in ["wendigo", "minotaur", "cave dragon"]:
            print_sleep(
                f"To your horror you see a {enemy}"
                "in the middle of the room staring at you."
            )
            print_sleep(
                f"This creature must have subjugated the {enemy_type}s.\n"
            )

            result, enemy = special_boss_encounter(encounter)

        else:
            print_sleep(
                "In the middle of the room you"
                f" can see the leader of the {enemy_type}s, the {enemy}."
            )

    elif encounter == "magic chest":
        result, enemy = magic_chest_encounter()

    elif encounter == "magic sword":
        result, enemy = magic_sword_encounter()

    elif encounter == "feast":
        print_sleep("The kitchen holds a delicious feast.")
        print_sleep("You eat as much as you can and take some more with you.")
        add_item(11)

    elif encounter == "talking book":
        result, enemy = talking_book_encounter()

    elif encounter == "armory":
        result, enemy = armory_encounter()

    print_sleep("")
    return enemy, result


def define_encounter(current_room: int):
    """
    This function define the encounter and enemy in the current room.
    These are defined by the values in the enemies list
    (random values defined at the beginning of the game)
    and the room_modifier list
    (currently unused, could later be used for finetuning)
    Input: current_room the room id in the dungeon
    Return: encounter and enemy as string variables
    """

    global enemies
    global room_modifier

    encounter = None
    enemy = None

    room_type = dungeon[current_room]

    if room_type == 1024:
        # boss room
        if enemies[-1] < 60:
            # 60% chance for boss of normal enemy type
            if enemy_type == "cultist":
                enemy = "wizard"
            elif enemy_type == "robber":
                enemy = "bandit lord"
            elif enemy_type == "goblin":
                enemy = "hobgoblin"
        elif enemies[-1] < 75:
            # 15% chance for Wendigo boss
            enemy = "wendigo"
        elif enemies[-1] < 90:
            # 15% chance for Minotaur boss
            enemy = "minotaur"
        else:
            # 0% chance for Dragon boss
            enemy = "cave dragon"
        encounter = enemy
        return encounter, enemy

    if current_room == 0:
        # Starting room
        encounter = "initial"
        return encounter, enemy

    encounter_rating = enemies[current_room] * room_modifier[current_room]
    # currently the room_modifier is not used but would allow finetuning

    if encounter_rating < 41:
        # 40% chance to have no enemy but encounter
        if room_type == 1:
            # storage room
            encounter = "magic chest"
        if room_type == 2:
            # smithy
            encounter = "magic sword"
        if room_type == 3:
            # kitchen
            encounter = "feast"
        if room_type == 4:
            # library
            encounter = "talking book"
        if room_type == 5:
            # barracks
            encounter = "armory"

    elif encounter_rating < 86:
        # 45% to have a small enemy
        if enemy_type == "cultist":
            enemy = "low cultist"
        elif enemy_type == "robber":
            enemy = "robber"
        elif enemy_type == "goblin":
            enemy = "green goblin"

    else:
        # 15% to have a big enemy
        if enemy_type == "cultist":
            enemy = "high cultist"
        elif enemy_type == "robber":
            enemy = "highwayman"
        elif enemy_type == "goblin":
            enemy = "black goblin"

    return encounter, enemy


def describe_room(current_room_type: int):
    """
    This function describe the room the player enters.
    Bigger encounters might be moved to seperate functions
    Input: current_room_type the room type identifier integer
    Return: none
    """

    global room_types
    global character_name
    global enemy_type

    if current_room_type == 0:
        # Starter room
        print_sleep(
            f"{character_name} you wake up in a "
            "dark room, unsure how you got here."
        )
        print_sleep(
            "The last thing you remember is having some "
            "drinks with your friends in the tavern of your hometown."
        )

    elif current_room_type == 1:
        # Storage room
        print_sleep("This room seems to be a messy storage room.")
        print_sleep(
            "There are crates and barrels "
            "standing around. Some of them smashed open."
        )

    elif current_room_type == 2:
        # Smithy
        print_sleep("You enter a room which seems to be used as a smithy.")
        print_sleep(
            "Although it is cold and dark "
            "now it seems to have been used recently."
        )

    elif current_room_type == 3:
        # Kitchen
        print_sleep("This room is obviously a kitchen.")
        print_sleep(
            "Cooking utensils lie around and a big pot is on a fireplace."
        )

    elif current_room_type == 4:
        # Library
        if enemy_type == "cultist":
            print_sleep("You enter a room which seems to be a library.")
            print_sleep(
                "There are rows of book cases, books with eery "
                "symbols on them and some reading stands."
            )
        else:
            print_sleep("You enter a room which might have been a library.")
            print_sleep(
                "There are empty book cases on the "
                "walls and still some books lying around."
            )
            print_sleep("The place is not in a good shape.")

    elif current_room_type == 1024:
        # Boss room
        print_sleep("The door with the skull lead you to a big round room.")


def room(current_room: int):
    """
    This is the main function
    which handles all interactions in the current room
    It will call subfunctions for description, setup of encounters,
    interactions, fights and room search
    Input: current_room the room id in the dungeon
    Return: result
      -3 for beating the boss
      -2 for player death,
      -1 for quit,
      >= 0 for success in room
    """
    if visited[current_room] is True:
        # If we already visited this room
        print_sleep(
            "You already searched this room. There is nothing new to discover."
        )
        print_sleep("=" * lwidth)
        return 1

    # First time visit we set to visited
    visited[current_room] = True

    # Call description function
    describe_room(dungeon[current_room])

    # Load Encounters for the room
    encounter, enemy = define_encounter(current_room)

    # Call the itneraction function
    enemy, result = interact(encounter, enemy)
    if result < 0:
        # character dead or quit command
        return result

    if enemy is not None:
        # Initiate the fight function
        result = fight(enemy)
        if result < 0:
            # character dead or quit command
            return result

    if dungeon[current_room] == 1024:
        # If we get this far in the function
        # and being in the boss room we beat the boss.
        print_sleep(
            f"Congratulations! You bested the dungeon and beat the {enemy}!"
        )
        print_sleep("=" * lwidth)
        return -3
    else:
        # Other rooms than the boss room can be searched
        result = search_room(dungeon[current_room])
        if result < 0:
            # character dead or quit command
            return result
        print_sleep("=" * lwidth)

        return 1


def init_dungeon():
    """
    Function to inititialize and randomize the dungeon.
    All values will be set in global parameters.
    Input: None
    Return: None
    """

    global dungeon
    global visited
    global enemy_type
    global enemies
    global loot
    global boss
    global room_modifier
    global weapon
    global armor
    global inventory
    global hitpoints

    number_of_rooms = 4

    print_sleep("=" * lwidth)
    print_sleep("Building rooms.")
    # dungeon map
    dungeon = [0] + random.sample(
        range(1, number_of_rooms + 1), number_of_rooms
    ) + [1024]
    visited = [False] * (number_of_rooms + 2)

    print_sleep("Choosing equipment.")
    weapon = 0
    armor = 0
    inventory = []
    hitpoints = 30

    print_sleep("Herding monsters.")
    enemy_type = random.choice(enemies_choice)
    enemies = random.choices(range(1, 101), k=number_of_rooms + 1)
    room_modifier = [1] * (number_of_rooms + 1)

    print_sleep("Hiding treasures.")
    # rolls will happen directly in the room
    # loot = random.choices(loot_choice, k=number_of_rooms + 1)

    print_sleep("Waking dragon.")
    print_sleep("=" * lwidth)


def print_sleep(message_to_print):
    """
    Helper function to include delays in print messages
    Input: message_to_print will be displayed in terminal
    Return: None
    """
    print(message_to_print)
    time.sleep(.1)


def start_game():
    """
    Main game function
    """
    global character_name
    global play

    print_sleep("*" * lwidth)
    welcome = "Welcome to the world of Dungeonerum."
    print_sleep(" " * int((80 - len(welcome)) / 2) + welcome)
    print_sleep("*" * lwidth)

    character_name = input("Please tell me your name.\n")
    print_sleep("")
    print_sleep(f"Hello {character_name}, let us go on an adventure.")
    print_sleep("=" * lwidth)
    print_sleep(
        "[You can always end the game "
        "by typing \"quit\" in the choice dialogue.]"
    )

    current_step = 0
    current_room = 0
    play = True

    while play:

        if current_room == 0:
            # new game starts in room 0
            init_dungeon()

        # deal with current room
        result = room(current_room)

        if result >= 0:
            # if game is not over choose next room from hallway
            current_room, current_step = room_choice(current_step)

        else:
            # game is over
            if result == -1:
                # quit command
                print_sleep("*" * lwidth)
                break
            go = "Game Over"
            go = " " * int((80 - len(go)) / 2) + go
            go += "\n" + "=" * lwidth

            print_sleep(go)
            # retry?
            choice = input("Do you want to play again? y/n ")
            if choice != "y":
                # any other input is ok to close the game
                play = False
                print_sleep("*" * lwidth)
            else:
                current_room = 0
                current_step = 0
                play = True
                print_sleep("=" * lwidth)

    goodbye = "Goodbye from the world of Dungeonerum."
    visitagain = "Visit us again soon."
    print(" " * int((80 - len(goodbye)) / 2) + goodbye)
    print(" " * int((80 - len(visitagain)) / 2) + visitagain)
    print("*" * lwidth)


# entry point of the program
def main():
    start_game()


if __name__ == "__main__":
    main()
