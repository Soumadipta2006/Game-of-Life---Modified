This file contains the code for a modified version of the Game of Life.
It has been made using the pygame library and basic Python without OOPs.
The modifications include:
1. Using hexagonal grid cells instead of the regular square ones.
2. Every dead cell resurrects after 6 generations irrespective of the number of live neighbors.
3. All the resurrected cells cannot die by how they previously died.
4. Every 4 generations a random dead cell comes to life irrespective of the number of live neighbors.
