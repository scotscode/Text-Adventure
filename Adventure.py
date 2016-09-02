import sys
import os
import pickle
from assets.characters import *
from assets.map import *

mapchoice = def_room
charchoice = def_characters
#puts objects into user's inventory and remove from room's inventory
user = charchoice.user
global current_user_file
current_user_file = ""

def newUser():
    user_files = len(os.listdir("users/"))
    new_user_file = open("users/User%d.xml" %(user_files), "wb+")
    new_user_file.close()
    name = raw_input("Please enter your name: ")
    user.name = name
    global current_user_file
    current_user_file = "users/User%d.xml"%(user_files)

if not os.path.exists("users/User0.xml"):
    init_open = open("users/User0.xml", "w")
    current_user_file = "users/User0.xml"
    name = raw_input("Please enter your name: ")
    user.name = name
    print user.name
    init_open.close()

else:
    if len(os.listdir("users/")) == 1:
        read = open("users/User0.xml", "rb+")
        try:
            user_data = pickle.load(read)
        except Exception:
            raise IOError
        else:
            read.close()
            chosen_user = user_data.name
            user_choice = raw_input("Do you want to continue your game as '%s'? (y/n) " %(chosen_user))
            if user_choice == "y":
                current_user_file = "users/User0.xml"
                user = user_data
            elif user_choice == "n":
                new_user = raw_input("Do you want to make a new user? (y/n) ")
                if new_user == "y":
                    newUser()
                elif new_user == "n":
                    pass
                else:
                    print "user input not recgnised"

            else:
                raise Exception("invalid user input")

    else:
        choose_new_old = raw_input("To select a user name press 1, to make a new user account press 2 ")
        if choose_new_old == "2":
            newUser()
        elif choose_new_old == "1":
            selectname = raw_input("Enter your username: ")
            founduser = False
            for files in (os.listdir("users/")):
                if os.stat("users/"+files).st_size == 0:
                    continue
                check_file = open("users/%s"%(files), "rb+")
                file_data = pickle.load(check_file)
                check_file.close()
                if file_data.name == selectname:
                    user = file_data
                    current_user_file = "users/"+files
                    print "Sucess, user found!"
                    founduser = True
            if founduser == False:
                print "user not found"


def save():
    with open(current_user_file, "wb") as output:
        pickle.dump(user,output)
    for files in (os.listdir("users/")):
        if os.stat("users/"+files).st_size == 0:
            os.remove("users/"+files)

def take(character, obj):
    truth = current_room.rmobj(obj)
    if truth == False:
        print "object %s not in room"%(obj)
    else:
        moved = character.takeobj(obj)
        print "object", obj, "taken"

def drop(character, obj):
        success = user.dropobj(obj)
        if success == True:
            current_room.addobj(obj)
            print "object", obj, "dropped"

def move(direction, x, y):
    check = check_walls(x,y)
    if check != True:
        print "You have encountered a wall"
    else:
        user.move(direction)
        CurrentRoom()
        rmdescription()

#room description
def rmdescription():
    print current_room.descr

#remove objects from current room
def rmobjects():
    current_room.objects

def check_walls( x_or_y, pos_or_neg):
    for rooms in mapchoice.roomlist:
        theoposition = user.loc_id[x_or_y] + pos_or_neg
        if x_or_y == 1:
            fullpos = [user.loc_id[0], theoposition]
        elif x_or_y == 0:
            fullpos = [theoposition, user.loc_id[1]]
#       print fullpos, theoposition, rooms.id, roomlist
        if fullpos == rooms.id:
            return True
        if fullpos != rooms.id:
            pass
                #print False

def CurrentRoom():
    for room in mapchoice.roomlist:
        if room.id == user.loc_id:
            global current_room
            current_room = room
            return room

def analyse(user_input):
    '''splits input into list with words'''
    split = user_input.split()
    return split

def Callfunc(list1):
    '''analyse single words and call functions/methods as appropiate'''
    if "go" in list1:
        if "west" in list1:
            move("west", 0, -1)
        elif "east" in list1:
            move("east",0, 1)
        elif "south" in list1:
            move("south", 1, -1)
        elif "north" in list1:
            move("north", 1, 1)
        else:
            print "You need to specify a valid direction"
    elif "take" in list1:
        for word in list1:
            if "take" not in word:
                obje = word
                take(user, obje)
    elif "drop" in list1:
        for word in list1:
            if "drop" not in word:
                obje = word
                drop(user,obje)
    elif "quit" in list1:
        progress_check = raw_input("Do you want to save your progress? (y/n) ")
        if progress_check == "y":
            save()
            sys.exit()
        elif progress_check == "n":
	        sys.exit()
        else:
            print "user input not recognised"
    elif "save" in list1:
        save()
    elif "health" in list1:
        print "You're health is: ", user.health
    elif "look" in list1:
        rmdescription()
    elif "eat" in list1:
        #checks whether second word entered is a food and is in the user's inventory(invobj)
        if list1[1] in (food_dict and user.invobj):
            user.dropobj(list1[1])
            # find value for health increase from food_dict
            healthincrease = food_dict[list1[1]]
            user.heal(healthincrease)
            print "you're health is now: ", user.health
        elif list1[1] not in user.invobj:
            if list1[1] in food_dict:
                print "food not in user inventory"
            elif list1[1] not in food_dict:
                print "food not recognised"
    elif "hit" in list1:
        # there is only ever one enemy in a user's enemy list
        if user.enemies:
            if user.enemies[0] in list1:
                for members in weapons:
                    # checks whether the user has entered a weapon to use and if its in the user inventory
                    if members in (list1 and user.invobj):
                        damage = weapons[members]
                        # finds instance name of enemy and reduced health if found
                        for cha in charchoice.character_list:
                            if cha.name == user.enemies[0]:
                                print cha.injure(damage)
                                #removes enemy from user's enemy list if killed
                                if cha.life == False:
                                    user.enemies.remove(cha.name)
                                    print "you have killed", cha.name
                                    # remove killed character from room
                                    for room in mapchoice.roomlist:
                                        if room.id == user.loc_id:
                                            room.remove_character(cha.name)
                # executes if a weapon is listed but not in user's inventory
                    if members in list1:
                        if members not in user.invobj:
                            print "you don't have a", members
        else:
            print "cannot see enemy"

    elif "list" in list1:
        print user.invobj

    else:
        print "command entered not valid"

#dict for amount of health improvements for foods
food_dict = {"apple":10, "sandwhich":20}
#dict to determine injury on player
weapons ={"sword":60, "knife":30}

print '''Welcome to Text Adeventure (Anniversary Edition) \n
by Scots.code() '''


while True:
    CurrentRoom()
    for room in mapchoice.roomlist:
        for users in charchoice.character_list:
            if room.id == users.loc_id:
                # adds character to room unless dead
                if users.name not in room.character and users.life == True:
                    room.add_character(users.name)
            #if the room and user don't have same coordinate, it attempts to remove user from room
            if room.id != users.loc_id:
                try:
                    room.remove_character(users.name)
                except ValueError:
                    pass
    #checks for other characters (enemy) in room and displays enemy info
        if len(room.character) > 1:
            for charas in charchoice.character_list:
                if charas.name in room.character and charas.name != "user":
                    #print the desription of enemy and add to user's enemy list
                    print charas.descr
                    charchoice.user.enemies.append(charas.name)
                    if "health" not in split_words:
                        print split_words
                        charchoice.user.injure(charas.hp)
                        print "you have been hit by", charas.name, "you're health is now", charchoice.user.health
                        if not charchoice.user.life:
                            print "You have died"
                            sys.exit()
    # remove character from user's enemy list if not in same room
    for enemy in charchoice.character_list:
        if charchoice.user.loc_id != enemy.loc_id:
            try:
                user.enemies.remove(enemy.name)
            except:
                pass

    command = raw_input(">>> ")
    split_words = analyse(command)
    Callfunc(split_words)
