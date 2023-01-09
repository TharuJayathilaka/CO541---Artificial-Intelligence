'''
This is an AIMA-Python-based solution for the 8-puzzle problem.

- The states are represented a 1D strings of the form '012345678'. The '0' indicates the space. 
The first three numbers of the tiles on the top row, and so forth.

- The actions are represented as single characters: 'u' for up (that is, move the tile "above" the 
empty space down so as to "move" the space "up"); 'd' for down; 'r' for right and 'l' for left. 

@author: kvlinden
@version 31jan2013

@modified-by: trbandara
'''

'''----------------------------ANSWERS---------------------------------'''

'''
------------------------------------------------------------------------------------------------------------------------------------------------------------
Name : H.A.D.T.T. Jayathilaka
E.No: E/16/156

TODO 2:

1.Run the code as it is. What puzzle configuration does it solve? Does it give the right solution?
  Comment your answer in eight.py.
  
  solution: []
  steps: 0
  time: 0.000 seconds
  
  goal_state = "012345678"
  initial_state = "012345678"
  
  It gives this result and this means this gives the initial state of final solutions since goal state and initial state is same.
  There is nothing to be done to acieve goal state since it already in the goal state.



------------------------------------------------------------------------------------------------------------------------------------------------------------
'''

from search import Problem, astar_search
import time

class EightPuzzle(Problem):
    '''This is an AIMA Problem sub-class that implements the traditional 8 puzzle.'''
    
    def __init__(self, initial, goal):
        '''This method initializes a standard AIMA search problem for the 8 puzzle.'''
        self.initial = initial
        self.goal = goal
        
    def actions(self, state):
        # TODO: Implement a proper actions() method here.
        
        zero_pos = state.find('0') # Should find a blank postion
       
        if zero_pos == 0:
            return ['d', 'r']
        elif zero_pos == 1:
            return ['d', 'l', 'r']
        elif zero_pos == 2:
            return ['d', 'l']
        elif zero_pos == 3:
            return ['u', 'd', 'r']
        elif zero_pos == 4:
            return ['u', 'd', 'l', 'r']
        elif zero_pos == 5:
            return ['u', 'd', 'l']
        elif zero_pos == 6:
            return ['u', 'r']
        elif zero_pos == 7:
            return ['u', 'l', 'r']
        elif zero_pos == 8: 
            return ['u', 'l']
    
    def result(self, state, action):
        # TODO: Implement a proper result() method here.

        zero_pos = state.find('0') # Should find a blank postion
        
        next_pos = -100; 

        if action == 'l':
            if (zero_pos > 0 and zero_pos < 3) or (zero_pos > 3 and zero_pos < 6) or (zero_pos > 6 and zero_pos <= 8):
                next_pos = zero_pos - 1
                
        elif action == 'r': 
            if zero_pos < 2 or (zero_pos > 2 and zero_pos < 5) or (zero_pos > 5 and zero_pos < 8):
                next_pos = zero_pos + 1

        elif action == 'd':
            if zero_pos >= 0 and zero_pos <= 5:
                next_pos = zero_pos + 3
                
        elif action == 'u':
            if zero_pos >= 3 and zero_pos <= 8:
                next_pos = zero_pos - 3
        
        return self.swap(state, zero_pos, next_pos)
    
    def goal_test(self, state):
        '''This method determines if the given state is a goal state.'''
        return state == self.goal
    
    def h(self, node):
        '''This calls the chosen heuristic.'''
        return self.h_disabled(node);
    
    def h_disabled(self, node):
        '''This version of h() is disabled (but still admissible because it always underestimates everything).'''
        return 0
    
    def h_mismatched_tiles(self, node):
        count = 0
        for i, val in enumerate(node.state):
            tile = int(val) 
            if(tile != 0 and i != tile): 
                count += 1 
        return count
        
    
    def h_manhattan_distance(self, node):

        allPositions = [(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
        totalDistance = 0
        for i, val in enumerate(node.state):
            tile = int(val)
            if(tile != 0):
                totalDistance += manhattan_distance(allPositions[i], allPositions[tile])
        return totalDistance
    
    def swap(self, state, x, y):
        '''This method swaps the tile values in the two given state coordinates.'''
        result = state.replace(state[x], "*")
        result = result.replace(state[y], state[x])
        return result.replace("*", state[y])

            
goal_state = "012345678"
# initial_state = "032415678" # 4 steps
# initial_state = "125634780" # 8 steps
initial_state = "063712854" # 16 steps

p = EightPuzzle(initial_state, goal_state)

time1 = time.time()
solution = astar_search(p).solution()
time2 = time.time()
print ("solution: " + str(solution))
print ("steps: " + str(len(solution)))
print ("time: %0.3f seconds" % (time2 - time1))


