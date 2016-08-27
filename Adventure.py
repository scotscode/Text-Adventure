import sys
#sys.path.insert(0, 'C:/Users/philipp/Documents/Python/Text Adventure/assets/characters')
import time
import os
import random
#import Defaultchara


class Character(object):
    ''' Base class for all characters (users and enemy)'''
    def __init__(self, name, health, descr, loc_id):
        self.name = name
        self.health = health
        self.invobj = []
        self.life = True
        self.enemies = []
        self.descr = descr
        self.loc_id = loc_id

    def injure(self, amount):
        if amount >= self.health:
            self.health -= amount
            self.life = False
            return self.health
        else:
            self.health -= amount
            return self.health
    def heal(self, amount):
        self.health += amount
        return self.health
    def takeobj(self, stuff):
        #maximise user inventory items to 10
        if len(self.invobj) <= 10:
            self.invobj.append(stuff)
            return self.invobj
        else:
            print "You have 10 items in your inventory already"
    def dropobj(self, stuff):
        try:
            self.invobj.remove(stuff)
            return True
        except ValueError:
            print "Object not in inventory"
    #coordinate system movement (x,y)
    def move(self, direction):
        if direction == "east":
            self.loc_id[0] += 1
            return self.loc_id
        elif direction == "west":
            self.loc_id[0] -= 1
            return self.loc_id
        elif direction == "north":
            self.loc_id[1] += 1
            return self.loc_id
        elif direction == "south":
            self.loc_id[1] -= 1
            return self.loc_id

class Rooms(object):
    '''Base class for all rooms'''
    def __init__(self,id, descr, objects):
        self.id = id
        self.descr = descr
        self.character = []
        self.objects = objects
    def add_character(self, character):
        self.character.append(character)
        return self.character
    def remove_character(self, charactername):
        self.character.remove(charactername)
        return self.character
    def rmobj(self, object):
        try:
            self.objects.remove(object)
        except:
            return False
    def addobj(self, object):
        try:
            self.objects.append(object)
        except:
            pass

#puts objects into user's inventory and remove from room's inventory
def take(character, obj):
    for room in roomlist:
        if room.id == character.loc_id:
            # rmobj() returns True if successful and false if unsuccessful
            truth = room.rmobj(obj)
            if truth == False:
                print "object %s not in room"%(obj)
            else:
                moved = character.takeobj(obj)
                print "object", obj, "taken"

def drop(character, obj):
    for room in roomlist:
        if room.id == character.loc_id:
            success = user.dropobj(obj)
            if success == True:
                room.addobj(obj)
                print "object", obj, "dropped"

#room description
def rmdescription():
    for room in roomlist:
        if room.id == user.loc_id:
            print room.descr

#remove objects from current room
def rmobjects():
    for room in roomlist:
        if room.id == user.lod_id:
            return room.objects

#initialise our rooms. Arguments as follows: coordinates (list), description (string), objects (list)
init_room= Rooms([0,0],"The initial room",["ball", "apple"])
west_room= Rooms([-1,0],"The western room",["sword","sandwhich"])
east_room= Rooms([1,0],"The Soviet room",["Stalin", "knife"])
north_room = Rooms([0,1],"The northern room",["plate"])
south_room = Rooms([0,-1],"the southern room",["ice"])
room11 = Rooms([1,1], "the (1,1) room", ["watch"])
roomneg1neg1 = Rooms([-1,-1], "the (-1,-1) room", ["paper"])
room1neg1 = Rooms([1,-1], "the (1,-1) room", ['pen'])
#roomneg11 = Rooms()



#update roomlist when initialising new rooms
roomlist = [init_room, west_room, east_room, north_room, south_room, room11, roomneg1neg1, room1neg1]

#initialise our characters. Arguments as follows: name, health, description, coordinates (init location)
user = Character('user', 100, None, [0,0])
brokus = Character('brokus', random.randrange(30, 60), "You have encountered a dark character called brokus", [random.randrange(-1,1),random.randrange(-1,1)])

character_list = [user, brokus]

#dict for amount of health improvements for foods
food_dict = {"apple":10, "sandwhich":20}
#dict to determine injury on player
weapons ={"sword":60, "knife":30}

print '''Welcome to Text Adeventure (Anniversary Edition) \n
by Scots.code() '''


def analyse(user_input):
    '''splits input into list with words'''
    split = user_input.split()
    return split

def check_walls( x_or_y, pos_or_neg):
    for rooms in roomlist:
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
def move(direction, x, y):
    check = check_walls(x,y)
    if check != True:
        print "You have encountered a wall"
    else:
        user.move(direction)
        rmdescription()
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
	    sys.exit()
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
                        for cha in character_list:
                            if cha.name == user.enemies[0]:
                                print cha.injure(damage)
                                #removes enemy from user's enemy list if killed
                                if cha.life == False:
                                    user.enemies.remove(cha.name)
                                    print "you have killed", cha.name
                                    # remove killed character from room
                                    for room in roomlist:
                                        if room.id == user.loc_id:
                                            room.remove_character(cha.name)
                # executes if a weapon is listed but not in user's inventory
                    if members in list1:
                        if members not in user.invobj:
                            print "you don't have the weapon", members
        else:
            print "cannot see enemy"

    elif "list" in list1:
        print user.invobj

    else:
        print "command entered not valid"
while True:

    for room in roomlist:
        for users in character_list:
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
            for charas in character_list:
                if charas.name in room.character and charas.name != "user":
                    #print the desription of enemy and add to user's enemy list
                    print charas.descr
                    user.enemies.append(charas.name)
    # remove character from user's enemy list if not in same room
    for enemy in character_list:
        if user.loc_id != enemy.loc_id:
            try:
                user.enemies.remove(enemy.name)
            except:
                pass
#            print rooms.descr

    command = raw_input(">>> ")
    split_words = analyse(command)
    Callfunc(split_words)
