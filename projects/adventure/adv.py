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
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

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


def lets_go(path=[], current_path=[], visited={}, prior_room=None, prior_direction=None):
    while len(visited) < len(room_graph):
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
                path.append(direction)
                current_path.append(opposite[direction])
                prior_room = player.current_room.id 
                prior_direction = direction
                player.travel(direction)
                # run it again!
                lets_go(path, current_path, visited, prior_room, prior_direction)
        # if we didn't find any ?, go back the way we came one step at a time until you find a ?
        # right now I think this takes you all the way back to the start which isn't great
        # but it does work
        if len(current_path):
            go_back = current_path.pop()        
            player.travel(go_back)
            path.append(go_back)
            prior_room = player.current_room.id
            prior_direction = path[-1]
            return path
        else:
            break
    return path

# currently this explores half of the "fork" map and then gets stuck
# on the loop, it just keeps going and going even when the path surpasses the length of the rooms list
# skips the 3-4 connection?

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
