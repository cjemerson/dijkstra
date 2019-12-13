#!/usr/bin/env python3
# example.py
#
# Charles Emerson
# December 13, 2019
#
# Simple visual example to showcase the Dijkstra's algorithm by running
# on a tile map similar to what you might expect from a game

from dijkstra import dijkstra

### INPUT (*** change me ***)

STARTING_ROW = 0
STARTING_COLUMN = 0
CULL_DISTANCE = 100

# A few example tile maps, a tile is positive if it is walkable
# (Top-left is row = zero, column = zero)
# tile_map = [
# [1, 1,],
# [0, 1,],
# ]
# tile_map = [
# [1, 1, 1],
# [0, 1, 0],
# [1, 1, 1]
# ]
tile_map = [
[1, 1, 0, 1, 1, 1],
[1, 1, 0, 1, 0, 1],
[0, 1, 1, 0, 1, 1],
[1, 0, 1, 0, 1, 0],
[0, 1, 1, 1, 1, 1],
]


### SETUP

NUM_COLS = len(tile_map[0])
NUM_ROWS = len(tile_map)

# Construct adjacency list for each walkable tile
adjacency_list = { }

for r in range(NUM_ROWS):
	for c in range(NUM_COLS):
		index = r * NUM_COLS + c

		# Neighboring vertices are keys which map to their distance
		vertex_adj_list = {}

		# If the tile is non-walkable, ignore it (simple optimization)
		if (tile_map[r][c] == 0):
			continue

		# NORTH
		if (r != 0 and tile_map[r-1][c] > 0):
			vertex_adj_list[index - NUM_COLS] = 1

		# WEST
		if (c != 0 and tile_map[r][c-1] > 0):
			vertex_adj_list[index - 1] = 1

		# SOUTH
		if (r != NUM_ROWS - 1 and tile_map[r+1][c] > 0):
			vertex_adj_list[index + NUM_COLS] = 1

		# EAST
		if (c != NUM_COLS - 1 and tile_map[r][c+1] > 0):
			vertex_adj_list[index + 1] = 1

		# Add to the adjacency list if vertex has at least one neighbor
		# (simple optimization)
		if (len(vertex_adj_list) != 0):
			adjacency_list[index] = vertex_adj_list

# Translate tile map to reuse print_2d_array function
for r in range(NUM_ROWS):
	for c in range(NUM_COLS):
		if tile_map[r][c] == 0:
			tile_map[r][c] = -1

# Helper function for printing 2d array
def print_2d_array(array_2d):
	num_rows = len(array_2d)
	num_columns = len(array_2d[0])

	for r in range(-2, num_rows):
		for c in range(-1, num_columns):
			if (r == -2 and c != -1):
				print(f"{c: >4}", end = "")
			elif (r == -1):
				print("{0: >4}".format("----"), end = "")
			elif (c == -1 and r > -1):
				print(f"{r: >3}|", end = "")
				print
			elif (r > -1 and c > -1 and array_2d[r][c] != -1):
				print(f"{array_2d[r][c]: >4}".format(), end = "")
			else:
				print("{0: >4}".format(""), end = "")
		print()
	print()

print("TILE MAP (Empty-Space is Non-Walkable)")
print_2d_array(tile_map)


### EXECUTION

print(f"Running Dijkstra's Algorithm from (row = {STARTING_ROW}, column = {STARTING_COLUMN})")
print(f"With a maximum reachable distance of {CULL_DISTANCE - 1}")
print()

source_vertex = STARTING_ROW * NUM_COLS + STARTING_COLUMN
distance_map = dijkstra(adjacency_list, source_vertex, CULL_DISTANCE)

# Overwrites tile_map to all -1 entries
distances = tile_map # Shallow copy
for r in range(NUM_ROWS):
	for c in range(NUM_COLS):
		distances[r][c] = -1

# Overwrites with the reachable distances
for vertex, distance in distance_map.items():
	row = int(vertex / NUM_COLS)
	col = vertex % NUM_COLS
	distances[row][col] = distance


print("DISTANCE MAP (Empty-Space is Unreachable)")
print_2d_array(distances)
