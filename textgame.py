import time

# Player state (inventory, etc.)
player_state = {
    'inventory': [],
    'current_room': 'bedroom'
}

# Game map
game_map = {
    'bedroom': {
        'description': (
            'You find yourself in a small, dimly lit bedroom. The bed is unmade, with sheets slightly askew, '
            'as if someone left in a hurry. A single wooden door leads to the hallway. There’s a strange '
            'silence, with only the faint ticking of an old clock mounted on the wall. Shadows flicker across the room.'
        ),
        'actions': {
            'explore': (
                'You crouch down and look under the bed, feeling around in the darkness. Your fingers brush '
                'against something cold and metallic—a small key. You add it to your inventory, feeling a strange '
                'sense of foreboding.'
            ),
            'go hallway': 'You gently open the creaking door and step into the hallway.'
        },
        'next_room': {
            'go hallway': 'hallway'
        },
        'items': ['key']
    },

    'hallway': {
        'description': (
            'You are in a long, narrow hallway lined with faded wallpaper. An eerie silence hangs in the air, and the faint scent '
            'of mildew permeates the space. Ahead, you can see a door to what appears to be a kitchen, and a dark, steep staircase '
            'leads down to the basement.'
        ),
        'actions': {
            'go kitchen': 'You step cautiously into the kitchen, each creak of the floorboards echoing down the hallway.',
            'go basement': 'You gather your courage and descend the stairs into the basement.'
        },
        'next_room': {
            'go kitchen': 'kitchen',
            'go basement': 'basement'
        },
        'items': []
    },

    'kitchen': {
        'description': (
            'The kitchen feels surprisingly intact, as if someone had recently prepared a meal here. The light flickers '
            'slightly, and the air is stale, carrying hints of rotten food. A fridge stands in one corner, an old rusty appliance '
            'that hums quietly, and a door on the other side leads to the backyard.'
        ),
        'actions': {
            'open fridge': (
                'You pull open the creaking fridge door, and a cold blast hits your face. Inside, you find a sandwich, '
                'still wrapped neatly. Although it looks a bit stale, you eat it anyway.'
            ),
            'go backyard': 'You open the door and step into the backyard.'
        },
        'next_room': {
            'go backyard': 'backyard'
        },
        'items': ['sandwich']
    },

    'basement': {
        'description': (
            'The basement is damp and smells of mold, with walls covered in shadows that seem to shift as you move. '
            'There are old crates and broken furniture scattered around. In the far corner, you notice a faint glint—it could be '
            'something useful.'
        ),
        'actions': {
            'explore': (
                'You approach the corner and see an old, dust-covered flashlight. Picking it up, you realize it still works, '
                'casting a small but steady beam of light. You add it to your inventory.'
            ),
            'run away':(
            ),
        },
        'next_room': {
            'run away': 'hallway'
        },
        'items': ['flashlight']
    },

    'backyard': {
        'description': (
            'You step into the backyard, surrounded by overgrown weeds and wild grass. The faint outline of a shed sits '
            'on the far side, looking abandoned. To your left, a narrow path leads toward a dense forest.'
        ),
        'actions': {
            'go shed': (
                'You cautiously approach the shed, its door hanging slightly ajar. Inside, you find a small assortment of tools—'
                'a crowbar, a rope, and an old lantern. You can only take one with you.'
            ),
            'go forest': (
                'You decide to follow the path into the forest. The trees seem to close in around you, their branches creating a canopy '
                'that blocks out the moonlight as you venture deeper.'
            )
        },
        'next_room': {
            'go shed': 'shed',
            'go forest': 'forest'
        },
        'items': []
    },
    'shed': {
        'description': (
            'You step inside the shed, the air thick with the scent of aged wood and rust. Shadows dance across the walls, illuminated by beams of '
            'moonlight filtering through the cracks. Tools hang neatly on the walls—some worn with use, others covered in a thin layer of dust, '
            'suggesting they haven’t seen action in years. In the corner, a rickety workbench holds an assortment of items: a crowbar, a length of sturdy '
            'rope, and a classic pump-action shotgun, its barrel slightly rusted but still gleaming with potential. The floor creaks underfoot as you take a cautious step further inside.'
        ),
        'actions': {
            'explore': (
                'As you look around, you notice an assortment of items scattered about:'
                '1. **Crowbar**: A sturdy crowbar, its metal surface worn but still robust. It could be useful for prying open doors or crates.'
                '2. **Rope**: A length of sturdy rope, weathered but reliable, perfect for climbing or securing items.'
                '3. **Lantern**: An old lantern, dusty but functional. When lit, it casts a warm glow, illuminating the shadows around you.'
                '4. **Shotgun**: A classic pump-action shotgun, its barrel slightly rusted but still gleaming with potential. It’s loaded and ready, promising power and protection in this perilous place.'
                'You take all of theme.'
            ),
            'go backyard': 'You open the creaking door and step into the backyard.'
        },
        'next_room': {
            'go backyard': 'backyard'
        },
        'items': ['crowbar', 'rope', 'shotgun']
    },
    'forest': {
        'description': (
            'You find yourself in the middle of a dense forest, surrounded by towering trees that block out the sky. '
            'The air is thick with the scent of pine and damp earth. In the distance, you hear the faint trickle of water and the occasional hoot '
            'of an owl. The path in front of you branches off, one leading deeper into the forest and another back toward what you think is home.'
        ),
        'actions': {
            'explore': (
                'You search the forest floor and come across an old, tattered map. It appears to show parts of the area, including an unfamiliar structure '
                'deeper in the woods. You add it to your inventory.'
            ),
            'go home': (
                'Feeling a mix of relief and uncertainty, you follow the path that you believe will lead you back home, hoping the journey was worth it.'
            )
        },
        'next_room': {
            'go home': 'bedroom'
        },
        'items': ['map']  # Ensure 'map' is here
    }
}

# Function to display current location
def show_location():
    room = player_state['current_room']
    print(f"\n{game_map[room]['actions']}")
    print("\nWhat will you do? Your options are:")
    for action in game_map[room]['actions']:
        print(f"- {action}")
    print("\n")
    item_hint()


# Function to get the player action
def get_action():
    room = player_state['current_room']
    action = input("Enter your action: ").lower()

    # Check if action is valid in the current room
    if action in game_map[room]['actions']:
        # If action is 'explore', find all items in the room
        if action == 'explore':
            found_items = []

            # Loop through all items in the room's item list
            for item in game_map[room]['items']:
                print(f"\nYou found a {item} and added it to your inventory.")
                player_state['inventory'].append(item)
                found_items.append(item)

            # Remove all found items from the room's item list
            for item in found_items:
                game_map[room]['items'].remove(item)

            # If no items were found in the room
            if not found_items:
                print("\nThere's nothing else to find here.")

        # Handle other actions that are not 'explore'
        else:
            print(f"\n{game_map[room]['actions'][action]}")

        # Return the next room if there is one; otherwise, stay in the current room
        return game_map[room]['next_room'].get(action, room)
    else:
        print("\nInvalid action. Try again.")
        return room


# Function to display inventory
def show_inventory():
    print("\nYour inventory contains:")
    if player_state['inventory']:
        for item in player_state['inventory']:
            print(f"- {item}")
    else:
        print("Nothing.")


#Function to use items
def use_item():
    room = player_state['current_room']
    use = input("Which item do you want to use: ").lower()

    if use == 'flashlight':
        if 'flashlight' in player_state['inventory'] and room == 'forest':
            player_state['inventory'].remove('flashlight') #Remove the flashlight
            print("\nYou light an old path in front of you...")
            time.sleep(3)
            print("\nAfter some walking, your flashlight dies out, but you find an old lever")
            player_state['inventory'].append('lever') #Adds the leaver
        elif 'flashlight' not in player_state['inventory']: #Checks if flashlight in inventory
            print("\nYou don't have flashlight in your inventory, go and find it")

    if use == 'map':
        if 'shotgun' in player_state['inventory'] and 'map' in player_state['inventory'] and 'lever' in player_state['inventory'] and room == 'basement' :
            player_state['inventory'].remove('map') #Remove the map
            print("\nMap shows you where lever can be installed")
            print("\nYou install the lever on the marked spot, and the door slowly opens.")
            player_state['inventory'].remove('shotgun') #Remove the shotgun
            time.sleep(3)
            print("\nA monster appears in front of you and leaps at you...")
            time.sleep(3)
            print("\nAfter a hard fight, you successfully kill the monster and progress further...")
            time.sleep(3)
            print("\nTime passes, and you find yourself in front of a solid stone wall, what will you do?")
            time.sleep(3)
            if 'crowbar' in player_state['inventory']: #Crowbar use
                print("\nTime passes as you think, and you hear the monster reviving itself, your only way out is to dig your way through ")
                time.sleep(3)
                print ("\nYou use your crowbar to dig through it...")
                time.sleep(3)
                print("\nInto light...")
                time.sleep(3)
                win_screen()
            elif 'crowbar' not in player_state['inventory']: #Check if crowbar in inventory
                print("\nTime passes as you think, and you hear the monster reviving itself, your only way out is to dig your way through ")
                time.sleep(3)
                print("\nYou look through your inventory, but you have nothing to dig with...")
                time.sleep(3)
                print("\nThe monster closes in, grabbing you with sudden force and snapping your neck...")
                time.sleep(3)
                death_screen()

        elif 'map' in player_state['inventory'] and 'lever' in player_state['inventory'] and room == 'basement':
            player_state['inventory'].remove('map') #Remove the map
            print("\nMap shows you where lever can be installed")
            print("\nYou install the lever on the marked spot, and the door slowly opens.")
            time.sleep(5)
            print("\nA monster appears in front of you and kills you")
            time.sleep(2)
            death_screen()

        elif 'map' not in player_state['inventory'] and 'lever' not in player_state['inventory']: #Cheks for map in inventory
            print("\nYou don't have map in your inventory, go and find it")

    if use == 'rope': #Kys option
        if 'rope' in player_state['inventory']:
            answer = input("\nYou really want to do this...? ")
            if answer == 'yes':
                print("...")
                time.sleep(5)
                death_screen()
            else:
                print("\nGood choice")
        elif 'rope' not in player_state['inventory']:
            print("\nYou don't have rope in your inventory, go and find it")


def item_hint():
    room = player_state['current_room']

    if 'map' in player_state['inventory'] and 'lever' in player_state['inventory'] and room == 'basement': #Map use hint
        print("\nHint: your map starts to feel hotter as you go deeper in the basement, maybe you should use ti")
        print("\n")

    if 'flashlight' in player_state['inventory'] and room == 'forest': #Flashlight use hint
        print("\nHint: its dark here, maybe you should light my path")
        print("\n")


#Win screen
def win_screen():
    while True:
        print("""
    ===================================================        
     __     ______  _    _  __          ______  _   _  
     \ \   / / __ \| |  | | \ \        / / __ \| \ | | 
      \ \_/ / |  | | |  | |  \ \  /\  / / |  | |  \| | 
       \   /| |  | | |  | |   \ \/  \/ /| |  | |     | 
        | | | |__| | |__| |    \  /\  / | |__| | |\  | 
        |_|  \____/ \____/      \/  \/   \____/|_| \_| 
    ===================================================
    
    
                1. Main Menu
                2. Instructions
                3. Exit           
    """)
        user_input = input("Enter your choice (1, 2, or 3): ").strip()

        if user_input == '1':
            main_menu()  # main menu
        elif user_input == '2':
            show_instructions()  # Show instructions
        elif user_input == '3':
            print("Thank you for playing! Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")


#Death screen
def death_screen():
    while True:
        print("""
    ======================================================
     __     ______  _    _     ____ _____ ______ ______   
     \ \   / / __ \| |  | |   |  __ \_   _|  ____|  __ \  
      \ \_/ / |  | | |  | |   | |  | || | | |__  | |  | | 
       \   /| |  | | |  | |   | |  | || | |  __| | |  | | 
        | | | |__| | |__| |   | |__| || |_| |____| |__| | 
        |_|  \____/ \____/    |_____/_____|______|_____/      
    ======================================================     
    
    
                1. Main Menu
                2. Instructions
                3. Exit                                         
    """)
        user_input = input("Enter your choice (1, 2, or 3): ").strip()

        if user_input == '1':
            main_menu()  # Start the game
        elif user_input == '2':
            show_instructions()  # Show instructions
        elif user_input == '3':
            print("Thank you for playing! Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")



# Function to start and play the game
def play_game():
    print("Welcome to HADES, the Text Adventure Game!")
    print("You will navigate through rooms and make choices to move forward.\n")

    while True:
        show_location()
        user_input = input("Enter your action or type 'inventory' to view items or 'use' to use them: ").lower()

        if user_input == 'inventory':
            show_inventory()
        elif user_input == 'quit':
            print("Thank you for playing! Goodbye!")
            break
        elif user_input == 'use':
            use_item()
        else:
            player_state['current_room'] = get_action()  # Correct assignment


# Main menu function
def main_menu():
    while True:
        print("""
        =====================================
                   WELCOME TO HADES
        =====================================
         _    _          _____  ______  _____ 
        | |  | |   /\   |  __ \|  ____|/ ____|
        | |__| |  /  \  | |  | | |__  | (___  
        |  __  | / /\ \ | |  | |  __|  \___ \ 
        | |  | |/ ____ \| |__| | |____ ____) |
        |_|  |_/_/    \_\_____/|______|_____/ 


               1. Start Game
               2. Instructions
               3. Exit

        =====================================
        """)

        choice = input("Enter your choice (1, 2, or 3): ").strip()

        # Handle the main menu options
        if choice == '1':
            play_game()  # Start the game
        elif choice == '2':
            show_instructions()  # Show instructions
        elif choice == '3':
            print("Thank you for playing! Goodbye!")
            break  # Exit the game loop
        else:
            print("Invalid choice. Please select 1, 2, or 3.")


# Instructions function
def show_instructions():
    print("""
    === INSTRUCTIONS ===

    Welcome to HADES, the Text Adventure Game!
    In this game, you will explore different locations and make choices to progress.
    Type the available actions listed in each room to explore and move forward.
    You can also type 'inventory' to check your items and 'quit' to exit the game.

    Good luck!
    """)


# Start the program with the main menu
main_menu()