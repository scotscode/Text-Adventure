import basecharacter
import random

user = basecharacter.Character('user', 100, None, [0,0], 5)
brokus = basecharacter.Character('brokus', random.randrange(30, 60), "You have encountered a dark character called brokus", [1,random.randrange(-1,1)],25)

character_list = [user, brokus]
