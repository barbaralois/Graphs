from room import Room
from player import Player
from world import World
from util import Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']

# store the opposites of each direction for easy access
opposite = {
    'n': 's',
    'e': 'w',
    's': 'n',
    'w': 'e'
}


def lets_go(path=[], visited={}, prior_room=None, prior_direction=None):
    while len(visited) < len(room_graph) - 1:    
        print('went from', prior_room, 'to', player.current_room.id)
        # if the current room is not yet in visited, add it and add the connected directions
        if player.current_room.id not in visited:
            visited[player.current_room.id] = {}
            for direction in player.current_room.get_exits():
                visited[player.current_room.id][direction] = '?'
        # if we came from a prior room, update the both rooms with that information
        if prior_room is not None:
            visited[prior_room][prior_direction] = player.current_room.id
            visited[player.current_room.id][opposite[prior_direction]] = prior_room
        # if we find a direction in the current room with ?, move to it (updating all variables)
        for direction in visited[player.current_room.id]:
            if visited[player.current_room.id][direction] == '?':
                print('moving', direction)
                path.append(direction)
                prior_room = player.current_room.id 
                prior_direction = direction
                player.travel(direction)
                # run it again!
                lets_go(path, visited, prior_room, prior_direction)
        # if we didn't find any ?, go back the way we came
        # I want this to simply skip the room we just came from but I couldn't figure it out
        # obviously the opposite isn't always ideal (like when we move up then need to go down and over)  
        path.append(opposite[prior_direction])
        prior_room = player.current_room.id
        prior_direction = path[-1]
        print('moving:', path[-1])
        player.travel(prior_direction)
        print('went from', prior_room, 'to', player.current_room.id)
        # print('path', path)
        return path

# currently this explores half of the "fork" map
# on the loop, it just keeps going and going even when the path surpasses the length of the rooms list

traversal_path = lets_go()


# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
