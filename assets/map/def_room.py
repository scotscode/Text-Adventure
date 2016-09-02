import baseroom

'''This file contains all the room data for the rooms loaded by default.'''

init_room = baseroom.Rooms([0,0],"The initial room",["ball", "apple"])
west_room = baseroom.Rooms([-1,0],"The western room",["sword","sandwhich"])
east_room = baseroom.Rooms([1,0],"The Soviet room",["Stalin", "knife"])
north_room = baseroom.Rooms([0,1],"The northern room",["plate"])
south_room = baseroom.Rooms([0,-1],"the southern room",["ice"])
room11 = baseroom.Rooms([1,1], "the (1,1) room", ["watch"])
roomneg1neg1 = baseroom.Rooms([-1,-1], "the (-1,-1) room", ["paper"])
room1neg1 = baseroom.Rooms([1,-1], "the (1,-1) room", ['pen'])

roomlist = [init_room, west_room, east_room, north_room, south_room, room11, roomneg1neg1, room1neg1]
