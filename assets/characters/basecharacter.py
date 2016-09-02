class Character(object):
    ''' Base class for all characters (users and enemy)'''
    def __init__(self, name, health, descr, loc_id, hp):
        self.name = name
        self.health = health
        self.invobj = []
        self.life = True
        self.enemies = []
        self.descr = descr
        self.loc_id = loc_id
        self.hp = hp

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
