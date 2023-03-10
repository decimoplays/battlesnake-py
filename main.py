# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
	print("INFO")

	return {
		"apiversion": "1",
		"author": "decimo",  # TODO: Your Battlesnake Username
		"color": "#f0c300",  # TODO: Choose color
		"head": "cosmic-horror",  # TODO: Choose head
		"tail": "cosmic-horror",  # TODO: Choose tail
	}


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
	print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
	print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:

	is_move_safe = {"up": True, "down": True, "left": True, "right": True}

	# We've included code to prevent your Battlesnake from moving backwards
	my_head = game_state["you"]["body"][0]  # Coordinates of your head
	my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

	if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
		is_move_safe["left"] = False

	elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
		is_move_safe["right"] = False

	elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
		is_move_safe["down"] = False

	elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
		is_move_safe["up"] = False

	# TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
	board_width = game_state['board']['width']
	board_height = game_state['board']['height']
	
	if my_head["x"] - 1 < 0:
		is_move_safe["left"] = False
	
	if my_head["y"] - 1 < 0:
		is_move_safe["down"] = False
	
	if my_head["x"] + 1 >= board_width:
		is_move_safe["right"] = False
	
	if my_head["y"] + 1 >= board_height:
		is_move_safe["up"] = False
	
	
	# TODO: Step 2 - Prevent your Battlesnake from colliding with itself
	my_body = game_state['you']['body']
	
	for position in my_body:
		if my_head["x"] + 1 == position["x"] and my_head["y"] == position["y"]:
			is_move_safe["right"] = False
		if my_head["x"] == position["x"] and my_head["y"] + 1 == position["y"]:
			is_move_safe["up"] = False
		if my_head["x"] - 1 == position["x"] and my_head["y"] == position["y"]:
			is_move_safe["left"] = False
		if my_head["x"] == position["x"] and my_head["y"] - 1 == position["y"]:
			is_move_safe["down"] = False
	
	# TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
	opponents = game_state['board']['snakes']
	for foe in opponents:
		snake_body=foe['body']
		for snake_position in snake_body:
			if my_head["x"] + 1 == snake_position["x"] and my_head["y"] == snake_position["y"]:
				is_move_safe["right"] = False
			if my_head["x"] == snake_position["x"] and my_head["y"] + 1 == snake_position["y"]:
				is_move_safe["up"] = False
			if my_head["x"] - 1 == snake_position["x"] and my_head["y"] == snake_position["y"]:
				is_move_safe["left"] = False
			if my_head["x"] == snake_position["x"] and my_head["y"] - 1 == snake_position["y"]:
				is_move_safe["down"] = False
		
		# THE TWO SERPENTS HEAD FIND THEMSELVES IN THE SAME SPOT
		if len(my_body) <= len(snake_body):
			if my_head["x"] + 1 == foe["head"]["x"] - 1 and my_head["y"] == foe["head"]["y"]: #you right vs left opponent
				is_move_safe["right"] = False
			if my_head["x"] == foe["head"]["x"] and my_head["y"] + 1 == foe["head"]["y"] - 1: #you up vs down opponent
				is_move_safe["up"] = False
			if my_head["x"] - 1 == foe["head"]["x"] + 1 and my_head["y"] == foe["head"]["y"]: #you left vs right opponent
				is_move_safe["left"] = False
			if my_head["x"] == foe["head"]["x"] and my_head["y"] - 1 == foe["head"]["y"] + 1: #you down vs up opponent
				is_move_safe["down"] = False
		
			# ~ if my_head["x"] + 1 == foe["head"]["x"] and (my_head["y"] == foe["head"]["y"] - 1 
			# ~ or my_head["y"] == foe["head"]["y"] + 1): #supposing opponent goes down or up and you want go right
				# ~ is_move_safe["right"] = False
			# ~ elif my_head["x"] - 1 == foe["head"]["x"] and (my_head["y"] == foe["head"]["y"] - 1 
			# ~ or my_head["y"] == foe["head"]["y"] + 1): #supposing opponent goes down or up and you want go left
				# ~ is_move_safe["left"] = False
			# ~ elif my_head["y"] + 1 == foe["head"]["y"] and (my_head["x"] == foe["head"]["x"] - 1 
			# ~ or my_head["x"] == foe["head"]["x"] + 1): #supposing opponent goes left or right and you want go up
				# ~ is_move_safe["up"] = False
			# ~ elif my_head["y"] - 1 == foe["head"]["y"] and (my_head["x"] == foe["head"]["x"] - 1 
			# ~ or my_head["x"] == foe["head"]["x"] + 1): #supposing opponent goes left or right and you want go down 
				# ~ is_move_safe["down"] = False
	print(opponents)
	print(is_move_safe)
	# Are there any safe moves left?
	safe_moves = []
	for move, isSafe in is_move_safe.items():
		if isSafe:
			safe_moves.append(move)

	if len(safe_moves) == 0:
		print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
		return {"move": "down"}

	# Choose a random move from the safe ones
	next_move = random.choice(safe_moves)

	# TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
	# food = game_state['board']['food']

	print(f"MOVE {game_state['turn']}: {next_move}")
	return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
	from server import run_server

	run_server({"info": info, "start": start, "move": move, "end": end})
