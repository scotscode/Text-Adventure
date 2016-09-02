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
