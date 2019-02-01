import numpy as np
import random
import math

class game_state : 
    
    def __init__(self) : 
        # the state should be defaulted
        # to all 1s for the 0th element 
        # of the 3rd dimensons and 0 for
        # the others
        self.state = np.array( [ np.ones( 9 ), 
                                 np.zeros( 9 ),
                                 np.zeros( 9 ),
                              ])

        self._result = None

        self._win_conditions = [ 
                                 # horizontal
                                 [1, 1, 1, 0, 0, 0, 0, 0, 0], 
                                 [0, 0, 0, 1, 1, 1, 0, 0, 0], 
                                 [0, 0, 0, 0, 0, 0, 1, 1, 1], 
                                 #vertical
                                 [1, 0, 0, 1, 0, 0, 1, 0, 0], 
                                 [0, 1, 0, 0, 1, 0, 0, 1, 0], 
                                 [0, 0, 1, 0, 0, 1, 0, 0, 1], 
                                 #diagonal
                                 [1, 0, 0, 0, 1, 0, 0, 0, 1],
                                 [0, 0, 1, 0, 1, 0, 1, 0, 0],
                               ]
                                 

    def valid_action( self, action ) : 
        # check if an action is allowed
        # It is only allowed if a piece
        # has not been played in that location
        # ie that the 0th state is 1
        if self.state[0][action] == 0 : 
            return False
        else : 
            return True

    def end( self ) : 
        if self.state[0].sum() == 0 : 
            return True
        for cond in self._win_conditions : 
            if self.state[1].dot( np.array( cond ) ) == 3 : 
                self._result = 1
                return True
            if self.state[2].dot( np.array( cond ) ) == 3 : 
                self._result = 2
                return True
        return False

    def get_result( self, piece ) : 
        if self._result is None : 
            if not self.end() : 
                print ('game_state::get_result -- WARNING : cannot retrieve result if game has not ended' ) 
                return None

        return (self._result == piece)

    def update_state( self, action, piece ) : 
        if piece not in [1,2] : 
            print ('game_state::update_state -- ERROR : piece must be 1 or 2' )
            return

        if self.valid_action( action ) : 
            self.state[0][action] = 0
            self.state[piece][action] = 1
        else : 
            print ('game_state::update_state -- WARNING : action %d taken py piece %d is not valid!' %( action, piece ) )


class player :
    
    def __init__(self, piece, mode='Train') : 

        self._fail = False
        if piece not in [1,2] : 
            print ('player::__init__ -- ERROR : piece must be 1 or 2 (1=X, 2=O)')
            self._fail = True
            return

        self._piece = piece
        self._policy_history = []

        # either build policy or load it
        self._policy = np.zeros( (9, 3, 9) )

        self._action_collect_range = 0.05

        self.action_reward = 1
        self.finish_rewards = { 'success' : 10, 
                                 'fail' : -10,
                                 'draw' : 2 }

        self.discount = 0.1

        self.policy.set( 0, [], [0,2,6,8] )

        self.policy.set( 1, [0], 4 )
        self.policy.set( 1, [1], 4 )
        self.policy.set( 1, [2], 4 )
        self.policy.set( 1, [3], 4 )
        self.policy.set( 1, [4], [0,2,6,8] )
        self.policy.set( 1, [5], 4 )
        self.policy.set( 1, [6], 4 )
        self.policy.set( 1, [7], 4 )
        self.policy.set( 1, [8], 4 )

        self.policy.set( 2, [0,1], 3 )
        self.policy.set( 2, [0,2], 3 )
        self.policy.set( 2, [0,3], 1 )
        self.policy.set( 2, [0,4], 1 )
        self.policy.set( 2, [0,5], 4 )
        self.policy.set( 2, [0,6], 1 )
        self.policy.set( 2, [0,7], 2 )
        self.policy.set( 2, [0,8], 2 )

        self.policy.set( 2, [2,0], 5 )
        self.policy.set( 2, [2,1], 5 )
        self.policy.set( 2, [2,3], 8 )
        self.policy.set( 2, [2,4], 5 )
        self.policy.set( 2, [2,5], 1 )
        self.policy.set( 2, [2,6], 6 )
        self.policy.set( 2, [2,7], 4 )
        self.policy.set( 2, [2,8], 1 )

        self.policy.set( 2, [6,0], 7 )
        self.policy.set( 2, [6,1], 4 )
        self.policy.set( 2, [6,2], 0 )
        self.policy.set( 2, [6,3], 7 )
        self.policy.set( 2, [6,4], 3 )
        self.policy.set( 2, [6,5], 0 )
        self.policy.set( 2, [6,7], 3 )
        self.policy.set( 2, [6,8], 3 )

        self.policy.set( 2, [8,0], 6 )
        self.policy.set( 2, [8,1], 6 )
        self.policy.set( 2, [8,2], 7 )
        self.policy.set( 2, [8,3], 4 )
        self.policy.set( 2, [8,4], 7 )
        self.policy.set( 2, [8,5], 7 )
        self.policy.set( 2, [8,6], 5 )
        self.policy.set( 2, [8,7], 5 )

        self.policy.set( 3, [0,4,1], 2 )
        self.policy.set( 3, [0,4,2], 1 )
        self.policy.set( 3, [0,4,3], 6 )
        self.policy.set( 3, [0,4,5], 7 )
        self.policy.set( 3, [0,4,6], 3 )
        self.policy.set( 3, [0,4,7], 5 )
        self.policy.set( 3, [0,4,8], 1 )

        self.policy.set( 3, [1,4,0], 2 )
        self.policy.set( 3, [1,4,2], 0 )
        self.policy.set( 3, [1,4,3], 2 )
        self.policy.set( 3, [1,4,5], 0 )
        self.policy.set( 3, [1,4,6], 5 )
        self.policy.set( 3, [1,4,7], 0 )
        self.policy.set( 3, [1,4,8], 3 )

        self.policy.set( 3, [2,4,0], 1 )
        self.policy.set( 3, [2,4,1], 0 )
        self.policy.set( 3, [2,4,3], 7 )
        self.policy.set( 3, [2,4,5], 8 )
        self.policy.set( 3, [2,4,6], 1 )
        self.policy.set( 3, [2,4,7], 3 )
        self.policy.set( 3, [2,4,8], 5 )

        self.policy.set( 3, [3,4,0], 6 )
        self.policy.set( 3, [3,4,1], 2 )
        self.policy.set( 3, [3,4,2], 7 )
        self.policy.set( 3, [3,4,5], 0 )
        self.policy.set( 3, [3,4,6], 0 )
        self.policy.set( 3, [3,4,7], 0 )
        self.policy.set( 3, [3,4,8], 1 )

        self.policy.set( 3, [4,0,1], 7 )
        self.policy.set( 3, [4,0,2], 6 )
        self.policy.set( 3, [4,0,3], 5 )
        self.policy.set( 3, [4,0,5], 3 )
        self.policy.set( 3, [4,0,6], 2 )
        self.policy.set( 3, [4,0,7], 1 )
        self.policy.set( 3, [4,0,8], 2 )

        self.policy.set( 3, [4,2,0], 8 )
        self.policy.set( 3, [4,2,1], 7 )
        self.policy.set( 3, [4,2,3], 5 )
        self.policy.set( 3, [4,2,5], 3 )
        self.policy.set( 3, [4,2,6], 8 )
        self.policy.set( 3, [4,2,7], 1 )
        self.policy.set( 3, [4,2,8], 0 )

        self.policy.set( 3, [4,6,0], 8 )
        self.policy.set( 3, [4,6,1], 7 )
        self.policy.set( 3, [4,6,2], 0 )
        self.policy.set( 3, [4,6,3], 5 )
        self.policy.set( 3, [4,6,5], 3 )
        self.policy.set( 3, [4,6,7], 1 )
        self.policy.set( 3, [4,6,8], 0 )

        self.policy.set( 3, [4,8,0], 6 )
        self.policy.set( 3, [4,8,1], 7 )
        self.policy.set( 3, [4,8,2], 6 )
        self.policy.set( 3, [4,8,3], 5 )
        self.policy.set( 3, [4,8,5], 3 )
        self.policy.set( 3, [4,8,6], 2 )
        self.policy.set( 3, [4,8,7], 1 )

        self.policy.set( 3, [5,4,0], 7 )
        self.policy.set( 3, [5,4,1], 0 )
        self.policy.set( 3, [5,4,2], 8 )
        self.policy.set( 3, [5,4,3], 0 )
        self.policy.set( 3, [5,4,6], 1 )
        self.policy.set( 3, [5,4,7], 2 )
        self.policy.set( 3, [5,4,8], 2 )

        self.policy.set( 3, [6,4,0], 3 )
        self.policy.set( 3, [6,4,1], 5 )
        self.policy.set( 3, [6,4,2], 1 )
        self.policy.set( 3, [6,4,3], 0 )
        self.policy.set( 3, [6,4,5], 1 )
        self.policy.set( 3, [6,4,7], 8 )
        self.policy.set( 3, [6,4,8], 7 )

        self.policy.set( 3, [7,4,0], 3 )
        self.policy.set( 3, [7,4,1], 5 )
        self.policy.set( 3, [7,4,2], 1 )
        self.policy.set( 3, [7,4,3], 0 )
        self.policy.set( 3, [7,4,5], 2 )
        self.policy.set( 3, [7,4,6], 8 )
        self.policy.set( 3, [7,4,8], 6 )

        self.policy.set( 3, [8,4,0], 1 )
        self.policy.set( 3, [8,4,1], 3 )
        self.policy.set( 3, [8,4,2], 5 )
        self.policy.set( 3, [8,4,3], 1 )
        self.policy.set( 3, [8,4,5], 2 )
        self.policy.set( 3, [8,4,6], 7 )
        self.policy.set( 3, [8,4,8], 6 )

        self.policy.set( 4, [0,1,3,2], 6 )
        self.policy.set( 4, [0,1,3,4], 6 )
        self.policy.set( 4, [0,1,3,5], 6 )
        self.policy.set( 4, [0,1,3,6], 4 )
        self.policy.set( 4, [0,1,3,7], 6 )
        self.policy.set( 4, [0,1,3,8], 6 )

        self.policy.set( 4, [0,2,3,1], 6 )
        self.policy.set( 4, [0,2,3,4], 6 )
        self.policy.set( 4, [0,2,3,5], 6 )
        self.policy.set( 4, [0,2,3,6], 4 )
        self.policy.set( 4, [0,2,3,7], 6 )
        self.policy.set( 4, [0,2,3,8], 6 )

        self.policy.set( 4, [0,3,1,2], 4 )
        self.policy.set( 4, [0,3,1,4], 2 )
        self.policy.set( 4, [0,3,1,5], 2 )
        self.policy.set( 4, [0,3,1,6], 2 )
        self.policy.set( 4, [0,3,1,7], 2 )
        self.policy.set( 4, [0,3,1,8], 2 )

        self.policy.set( 4, [0,4,1,2], 6 )
        self.policy.set( 4, [0,4,1,3], 2 )
        self.policy.set( 4, [0,4,1,5], 2 )
        self.policy.set( 4, [0,4,1,6], 2 )
        self.policy.set( 4, [0,4,1,7], 2 )
        self.policy.set( 4, [0,4,1,8], 2 )

        self.policy.set( 4, [0,5,4,1], 8 )
        self.policy.set( 4, [0,5,4,2], 8 )
        self.policy.set( 4, [0,5,4,3], 8 )
        self.policy.set( 4, [0,5,4,6], 8 )
        self.policy.set( 4, [0,5,4,7], 8 )
        self.policy.set( 4, [0,5,4,8], 2 )

        self.policy.set( 4, [0,6,1,2], 4 )
        self.policy.set( 4, [0,6,1,3], 2 )
        self.policy.set( 4, [0,6,1,4], 2 )
        self.policy.set( 4, [0,6,1,5], 2 )
        self.policy.set( 4, [0,6,1,7], 2 )
        self.policy.set( 4, [0,6,1,8], 2 )

        self.policy.set( 4, [0,7,2,1], 4 )
        self.policy.set( 4, [0,7,2,3], 2 )
        self.policy.set( 4, [0,7,2,4], 2 )
        self.policy.set( 4, [0,7,2,5], 2 )
        self.policy.set( 4, [0,7,2,6], 2 )
        self.policy.set( 4, [0,7,2,8], 2 )

        self.policy.set( 4, [0,8,2,1], 6 )
        self.policy.set( 4, [0,8,2,3], 1 )
        self.policy.set( 4, [0,8,2,4], 1 )
        self.policy.set( 4, [0,8,2,5], 1 )
        self.policy.set( 4, [0,8,2,6], 1 )
        self.policy.set( 4, [0,8,2,7], 1 )

        self.policy.set( 4, [2,0,5,1], 8 )
        self.policy.set( 4, [2,0,5,3], 8 )
        self.policy.set( 4, [2,0,5,4], 8 )
        self.policy.set( 4, [2,0,5,6], 8 )
        self.policy.set( 4, [2,0,5,7], 8 )
        self.policy.set( 4, [2,0,5,8], 4 )

        self.policy.set( 4, [2,1,5,0], 8 )
        self.policy.set( 4, [2,1,5,3], 8 )
        self.policy.set( 4, [2,1,5,4], 8 )
        self.policy.set( 4, [2,1,5,6], 8 )
        self.policy.set( 4, [2,1,5,7], 8 )
        self.policy.set( 4, [2,1,5,8], 4 )

        self.policy.set( 4, [2,3,8,0], 5 )
        self.policy.set( 4, [2,3,8,1], 5 )
        self.policy.set( 4, [2,3,8,4], 5 )
        self.policy.set( 4, [2,3,8,5], 4 )
        self.policy.set( 4, [2,3,8,6], 5 )
        self.policy.set( 4, [2,3,8,7], 5 )

        self.policy.set( 4, [2,4,5,0], 8 )
        self.policy.set( 4, [2,4,5,1], 8 )
        self.policy.set( 4, [2,4,5,3], 8 )
        self.policy.set( 4, [2,4,5,6], 8 )
        self.policy.set( 4, [2,4,5,7], 8 )
        self.policy.set( 4, [2,4,5,8], 0 )

        self.policy.set( 4, [2,5,1,0], 4 )
        self.policy.set( 4, [2,5,1,3], 0 )
        self.policy.set( 4, [2,5,1,4], 0 )
        self.policy.set( 4, [2,5,1,6], 0 )
        self.policy.set( 4, [2,5,1,7], 0 )
        self.policy.set( 4, [2,5,1,8], 0 )

        self.policy.set( 4, [2,6,8,0], 5 )
        self.policy.set( 4, [2,6,8,1], 5 )
        self.policy.set( 4, [2,6,8,3], 5 )
        self.policy.set( 4, [2,6,8,4], 5 )
        self.policy.set( 4, [2,6,8,5], 0 )
        self.policy.set( 4, [2,6,8,7], 5 )

        self.policy.set( 4, [2,7,4,0], 6 )
        self.policy.set( 4, [2,7,4,1], 6 )
        self.policy.set( 4, [2,7,4,3], 6 )
        self.policy.set( 4, [2,7,4,5], 6 )
        self.policy.set( 4, [2,7,4,6], 8 )
        self.policy.set( 4, [2,7,4,8], 6 )

        self.policy.set( 4, [2,8,1,0], 4 )
        self.policy.set( 4, [2,8,1,3], 0 )
        self.policy.set( 4, [2,8,1,4], 0 )
        self.policy.set( 4, [2,8,1,5], 0 )
        self.policy.set( 4, [2,8,1,6], 0 )
        self.policy.set( 4, [2,8,1,7], 0 )

        self.policy.set( 4, [6,0,7,1], 8 )
        self.policy.set( 4, [6,0,7,2], 8 )
        self.policy.set( 4, [6,0,7,3], 8 )
        self.policy.set( 4, [6,0,7,4], 8 )
        self.policy.set( 4, [6,0,7,5], 8 )
        self.policy.set( 4, [6,0,7,8], 4 )

        self.policy.set( 4, [6,1,4,0], 2 )
        self.policy.set( 4, [6,1,4,2], 0 )
        self.policy.set( 4, [6,1,4,3], 2 )
        self.policy.set( 4, [6,1,4,5], 2 )
        self.policy.set( 4, [6,1,4,7], 2 )
        self.policy.set( 4, [6,1,4,8], 2 )

        self.policy.set( 4, [6,2,0,1], 3 )
        self.policy.set( 4, [6,2,0,3], 8 )
        self.policy.set( 4, [6,2,0,4], 3 )
        self.policy.set( 4, [6,2,0,5], 3 )
        self.policy.set( 4, [6,2,0,7], 3 )
        self.policy.set( 4, [6,2,0,8], 3 )

        self.policy.set( 4, [6,3,7,0], 8 )
        self.policy.set( 4, [6,3,7,1], 8 )
        self.policy.set( 4, [6,3,7,2], 8 )
        self.policy.set( 4, [6,3,7,4], 8 )
        self.policy.set( 4, [6,3,7,5], 8 )
        self.policy.set( 4, [6,3,7,8], 4 )

        self.policy.set( 4, [6,4,3,0], 8 )
        self.policy.set( 4, [6,4,3,1], 0 )
        self.policy.set( 4, [6,4,3,2], 0 )
        self.policy.set( 4, [6,4,3,5], 0 )
        self.policy.set( 4, [6,4,3,7], 0 )
        self.policy.set( 4, [6,4,3,8], 0 )

        self.policy.set( 4, [6,5,0,1], 3 )
        self.policy.set( 4, [6,5,0,2], 3 )
        self.policy.set( 4, [6,5,0,3], 4 )
        self.policy.set( 4, [6,5,0,4], 3 )
        self.policy.set( 4, [6,5,0,7], 3 )
        self.policy.set( 4, [6,5,0,8], 3 )

        self.policy.set( 4, [6,7,3,0], 4 )
        self.policy.set( 4, [6,7,3,1], 0 )
        self.policy.set( 4, [6,7,3,2], 0 )
        self.policy.set( 4, [6,7,3,4], 0 )
        self.policy.set( 4, [6,7,3,5], 0 )
        self.policy.set( 4, [6,7,3,8], 0 )

        self.policy.set( 4, [6,8,3,0], 4 )
        self.policy.set( 4, [6,8,3,1], 0 )
        self.policy.set( 4, [6,8,3,2], 0 )
        self.policy.set( 4, [6,8,3,4], 0 )
        self.policy.set( 4, [6,8,3,5], 0 )
        self.policy.set( 4, [6,8,3,7], 0 )

        self.policy.set( 4, [8,0,6,1], 7 )
        self.policy.set( 4, [8,0,6,2], 7 )
        self.policy.set( 4, [8,0,6,3], 7 )
        self.policy.set( 4, [8,0,6,4], 7 )
        self.policy.set( 4, [8,0,6,5], 7 )
        self.policy.set( 4, [8,0,6,7], 2 )

        self.policy.set( 4, [8,1,6,0], 7 )
        self.policy.set( 4, [8,1,6,2], 7 )
        self.policy.set( 4, [8,1,6,3], 7 )
        self.policy.set( 4, [8,1,6,4], 7 )
        self.policy.set( 4, [8,1,6,5], 7 )
        self.policy.set( 4, [8,1,6,7], 4 )

        self.policy.set( 4, [8,2,7,0], 6 )
        self.policy.set( 4, [8,2,7,1], 6 )
        self.policy.set( 4, [8,2,7,3], 6 )
        self.policy.set( 4, [8,2,7,4], 6 )
        self.policy.set( 4, [8,2,7,5], 6 )
        self.policy.set( 4, [8,2,7,6], 4 )

        self.policy.set( 4, [8,3,4,0], 6 )
        self.policy.set( 4, [8,3,4,1], 0 )
        self.policy.set( 4, [8,3,4,2], 0 )
        self.policy.set( 4, [8,3,4,5], 0 )
        self.policy.set( 4, [8,3,4,6], 0 )
        self.policy.set( 4, [8,3,4,7], 0 )

        self.policy.set( 4, [8,4,7,0], 6 )
        self.policy.set( 4, [8,4,7,1], 6 )
        self.policy.set( 4, [8,4,7,2], 6 )
        self.policy.set( 4, [8,4,7,3], 6 )
        self.policy.set( 4, [8,4,7,5], 6 )
        self.policy.set( 4, [8,4,7,6], 2 )

        self.policy.set( 4, [8,5,7,0], 6 )
        self.policy.set( 4, [8,5,7,1], 6 )
        self.policy.set( 4, [8,5,7,2], 6 )
        self.policy.set( 4, [8,5,7,3], 6 )
        self.policy.set( 4, [8,5,7,4], 6 )
        self.policy.set( 4, [8,5,7,6], 4 )

        self.policy.set( 4, [8,6,5,0], 2 )
        self.policy.set( 4, [8,6,5,1], 2 )
        self.policy.set( 4, [8,6,5,2], 4 )
        self.policy.set( 4, [8,6,5,3], 2 )
        self.policy.set( 4, [8,6,5,4], 2 )
        self.policy.set( 4, [8,6,5,7], 2 )

        self.policy.set( 4, [8,7,5,0], 2 )
        self.policy.set( 4, [8,7,5,1], 2 )
        self.policy.set( 4, [8,7,5,2], 4 )
        self.policy.set( 4, [8,7,5,3], 2 )
        self.policy.set( 4, [8,7,5,4], 2 )
        self.policy.set( 4, [8,7,5,6], 2 )

        self.policy.set( 5, [0,4,1,2,3], 6 )
        self.policy.set( 5, [0,4,1,2,5], 6 )
        self.policy.set( 5, [0,4,1,2,6], 3 )
        self.policy.set( 5, [0,4,1,2,7], 6 )
        self.policy.set( 5, [0,4,1,2,8], 6 )

        self.policy.set( 5, [0,4,2,1,3], 7 )
        self.policy.set( 5, [0,4,2,1,5], 7 )
        self.policy.set( 5, [0,4,2,1,6], 7 )
        self.policy.set( 5, [0,4,2,1,7], 3 )
        self.policy.set( 5, [0,4,2,1,8], 7 )

        self.policy.set( 5, [0,4,3,6,1], 2 )
        self.policy.set( 5, [0,4,3,6,2], 1 )
        self.policy.set( 5, [0,4,3,6,5], 2 )
        self.policy.set( 5, [0,4,3,6,7], 2 )
        self.policy.set( 5, [0,4,3,6,8], 2 )

        self.policy.set( 5, [0,4,5,7,1], 2 )
        self.policy.set( 5, [0,4,5,7,2], 1 )
        self.policy.set( 5, [0,4,5,7,3], 1 )
        self.policy.set( 5, [0,4,5,7,6], 1 )
        self.policy.set( 5, [0,4,5,7,8], 1 )

        self.policy.set( 5, [0,4,6,3,1], 5 )
        self.policy.set( 5, [0,4,6,3,2], 5 )
        self.policy.set( 5, [0,4,6,3,5], 1 )
        self.policy.set( 5, [0,4,6,3,7], 5 )
        self.policy.set( 5, [0,4,6,3,8], 5 )

        self.policy.set( 5, [0,4,7,5,1], 3 )
        self.policy.set( 5, [0,4,7,5,2], 3 )
        self.policy.set( 5, [0,4,7,5,3], 6 )
        self.policy.set( 5, [0,4,7,5,6], 3 )
        self.policy.set( 5, [0,4,7,5,8], 3 )

        self.policy.set( 5, [0,4,8,1,2], 7 )
        self.policy.set( 5, [0,4,8,1,3], 7 )
        self.policy.set( 5, [0,4,8,1,5], 7 )
        self.policy.set( 5, [0,4,8,1,6], 7 )
        self.policy.set( 5, [0,4,8,1,7], 6 )

        self.policy.set( 5, [1,4,0,2,3], 6 )
        self.policy.set( 5, [1,4,0,2,5], 6 )
        self.policy.set( 5, [1,4,0,2,6], 3 )
        self.policy.set( 5, [1,4,0,2,7], 6 )
        self.policy.set( 5, [1,4,0,2,8], 6 )

        self.policy.set( 5, [1,4,2,0,3], 8 )
        self.policy.set( 5, [1,4,2,0,5], 8 )
        self.policy.set( 5, [1,4,2,0,6], 8 )
        self.policy.set( 5, [1,4,2,0,7], 8 )
        self.policy.set( 5, [1,4,2,0,8], 5 )

        self.policy.set( 5, [1,4,3,2,0], 6 )
        self.policy.set( 5, [1,4,3,2,5], 6 )
        self.policy.set( 5, [1,4,3,2,6], 0 )
        self.policy.set( 5, [1,4,3,2,7], 6 )
        self.policy.set( 5, [1,4,3,2,8], 6 )

        self.policy.set( 5, [1,4,5,0,2], 8 )
        self.policy.set( 5, [1,4,5,0,3], 8 )
        self.policy.set( 5, [1,4,5,0,6], 8 )
        self.policy.set( 5, [1,4,5,0,7], 8 )
        self.policy.set( 5, [1,4,5,0,8], 2 )

        self.policy.set( 5, [1,4,6,5,0], 3 )
        self.policy.set( 5, [1,4,6,5,2], 3 )
        self.policy.set( 5, [1,4,6,5,3], 0 )
        self.policy.set( 5, [1,4,6,5,7], 3 )
        self.policy.set( 5, [1,4,6,5,8], 3 )

        self.policy.set( 5, [1,4,7,0,2], 8 )
        self.policy.set( 5, [1,4,7,0,3], 8 )
        self.policy.set( 5, [1,4,7,0,5], 8 )
        self.policy.set( 5, [1,4,7,0,6], 8 )
        self.policy.set( 5, [1,4,7,0,8], 6 )

        self.policy.set( 5, [1,4,8,3,0], 5 )
        self.policy.set( 5, [1,4,8,3,2], 5 )
        self.policy.set( 5, [1,4,8,3,5], 2 )
        self.policy.set( 5, [1,4,8,3,6], 5 )
        self.policy.set( 5, [1,4,8,3,7], 5 )

        self.policy.set( 5, [2,4,0,1,3], 7 )
        self.policy.set( 5, [2,4,0,1,5], 7 )
        self.policy.set( 5, [2,4,0,1,6], 7 )
        self.policy.set( 5, [2,4,0,1,7], 3 )
        self.policy.set( 5, [2,4,0,1,8], 7 )

        self.policy.set( 5, [2,4,1,0,3], 8 )
        self.policy.set( 5, [2,4,1,0,5], 8 )
        self.policy.set( 5, [2,4,1,0,6], 8 )
        self.policy.set( 5, [2,4,1,0,7], 8 )
        self.policy.set( 5, [2,4,1,0,8], 5 )

        self.policy.set( 5, [2,4,3,7,0], 1 )
        self.policy.set( 5, [2,4,3,7,1], 0 )
        self.policy.set( 5, [2,4,3,7,5], 1 )
        self.policy.set( 5, [2,4,3,7,6], 1 )
        self.policy.set( 5, [2,4,3,7,8], 1 )

        self.policy.set( 5, [2,4,5,8,0], 1 )
        self.policy.set( 5, [2,4,5,8,1], 0 )
        self.policy.set( 5, [2,4,5,8,3], 0 )
        self.policy.set( 5, [2,4,5,8,6], 0 )
        self.policy.set( 5, [2,4,5,8,7], 0 )

        self.policy.set( 5, [2,4,6,1,0], 7 )
        self.policy.set( 5, [2,4,6,1,3], 7 )
        self.policy.set( 5, [2,4,6,1,5], 7 )
        self.policy.set( 5, [2,4,6,1,7], 8 )
        self.policy.set( 5, [2,4,6,1,8], 7 )

        self.policy.set( 5, [2,4,7,3,0], 5 )
        self.policy.set( 5, [2,4,7,3,1], 5 )
        self.policy.set( 5, [2,4,7,3,5], 8 )
        self.policy.set( 5, [2,4,7,3,6], 5 )
        self.policy.set( 5, [2,4,7,3,8], 5 )

        self.policy.set( 5, [2,4,8,5,0], 3 )
        self.policy.set( 5, [2,4,8,5,1], 3 )
        self.policy.set( 5, [2,4,8,5,3], 1 )
        self.policy.set( 5, [2,4,8,5,6], 3 )
        self.policy.set( 5, [2,4,8,5,7], 3 )

        # 6 more ...

        self.policy.set( 6, [0,1,3,6,4,2], [5,8] )
        self.policy.set( 6, [0,1,3,6,4,5], 8 )
        self.policy.set( 6, [0,1,3,6,4,7], [5,8] )
        self.policy.set( 6, [0,1,3,6,4,8], 5 )

        self.policy.set( 6, [0,2,3,6,4,1], [5,8] )
        self.policy.set( 6, [0,2,3,6,4,5], 8 )
        self.policy.set( 6, [0,2,3,6,4,7], [5,8] )
        self.policy.set( 6, [0,2,3,6,4,8], 5 )

        self.policy.set( 6, [0,3,1,2,4,5], [7,8] )
        self.policy.set( 6, [0,3,1,2,4,6], [7,8] )
        self.policy.set( 6, [0,3,1,2,4,7], 8 )
        self.policy.set( 6, [0,3,1,2,4,8], 7 )

        self.policy.set( 6, [0,4,1,2,6,3], 5 )
        self.policy.set( 6, [0,4,1,2,6,5], 3 )
        self.policy.set( 6, [0,4,1,2,6,7], 3 )
        self.policy.set( 6, [0,4,1,2,6,8], 3 )

        self.policy.set( 6, [0,5,4,8,2,1], [3,6] )
        self.policy.set( 6, [0,5,4,8,2,3], [1,6,7] )
        self.policy.set( 6, [0,5,4,8,2,6], [1,7] )
        self.policy.set( 6, [0,5,4,8,2,7], [1,6] )

        self.policy.set( 6, [0,6,1,2,4,3], [7,8] )
        self.policy.set( 6, [0,6,1,2,4,5], [7,8] )
        self.policy.set( 6, [0,6,1,2,4,7], 8 )
        self.policy.set( 6, [0,6,1,2,4,8], 7 )

        self.policy.set( 6, [0,7,2,1,4,3], [6,8] )
        self.policy.set( 6, [0,7,2,1,4,5], [6,8] )
        self.policy.set( 6, [0,7,2,1,4,6], 8 )
        self.policy.set( 6, [0,7,2,1,4,8], 6 )

        self.policy.set( 6, [0,8,2,1,6,3], 4 )
        self.policy.set( 6, [0,8,2,1,6,4], 3 )
        self.policy.set( 6, [0,8,2,1,6,5], [3,4] )
        self.policy.set( 6, [0,8,2,1,6,7], [3,4] )

        # 4 more sets to include original rotation

        self.policy.set( 7, [0,4,1,2,6,3,5], 7 )
        self.policy.set( 7, [0,4,1,2,6,3,7], 5 )
        self.policy.set( 7, [0,4,1,2,6,3,8], 5 )

        self.policy.set( 7, [0,4,2,1,7,3,5], 8 )
        self.policy.set( 7, [0,4,2,1,7,3,6], 5 )
        self.policy.set( 7, [0,4,2,1,7,3,8], 5 )

        self.policy.set( 7, [0,4,3,6,2,1,5], 7 )
        self.policy.set( 7, [0,4,3,6,2,1,7], 5 )
        self.policy.set( 7, [0,4,3,6,2,1,8], 7 )

        self.policy.set( 7, [0,4,5,7,1,2,3], 6 )
        self.policy.set( 7, [0,4,5,7,1,2,6], 3 )
        self.policy.set( 7, [0,4,5,7,1,2,8], 6 )

        self.policy.set( 7, [0,4,6,3,5,1,2], 7 )
        self.policy.set( 7, [0,4,6,3,5,1,7], 8 )
        self.policy.set( 7, [0,4,6,3,5,1,8], 7 )

        self.policy.set( 7, [0,4,7,5,3,6,1], 2 )
        self.policy.set( 7, [0,4,7,5,3,6,2], 1 )
        self.policy.set( 7, [0,4,7,5,3,6,8], 2 )

        self.policy.set( 7, [0,4,8,1,7,6,2], 5 )
        self.policy.set( 7, [0,4,8,1,7,6,3], 2 )
        self.policy.set( 7, [0,4,8,1,7,6,5], 2 )

        # 9 times more with different x starts




    def init_game( self ) : 
        # reset for new game
        self._policy_history = []

    def act(self, game_state) : 

        # the distribution of actions should be given
        # by the dot of the policy and state
        pref_actions  = np.tensordot( self._policy, game_state.state, axes=([1,2],[0,1]) )
        print ('Actions')
        print(pref_actions)

        # normalize (perhaps build normalization into policy)
        act_sum = pref_actions.sum()
        if act_sum != 0 : 
            pref_actions = pref_actions/act_sum

        sorted_action = []
        for idx, val in enumerate(pref_actions) : 
            if game_state.valid_action( idx ) : 
                sorted_action.append( ( val, idx ) )

        
        sorted(sorted_action, reverse=True )
        max_val = sorted_action[0][0]

        # collect the best actions within the collect range
        collected_actions = []
        for val, idx in sorted_action : 
            if math.fabs( max_val - val ) < self._action_collect_range : 
                collected_actions.append(idx)

        coll_len = len(collected_actions)
        if  coll_len > 1 : 
            sel_idx = random.randint( 0, coll_len-1 )
            selected_action = collected_actions[sel_idx]
        else : 
            selected_action = collected_actions[0]

        print ('Piece %d takes action %d' %( self._piece, selected_action ) )
        game_state.update_state( selected_action, self._piece )
        self.store_policy( game_state.state, selected_action )

        return game_state

    def finish_game( self, result ) : 

        #self.update_policy( self.finish_rewards[result] )
        self._policy_history = []

    def store_policy( self, state, action ) : 

        # store the history.  Simply take the inner product
        # between the state and the action, which has the
        # structure of the policy, and store it along with the reward
        action_encode = np.zeros( 9 ) 
        action_encode[action] = 1
        self._policy_history.append( np.tensordot( state, action_encode, axes=0 ) )

    def update_policy(self, reward )  :

        n_steps = len( self._policy_history ) 

        updated_policy = self._policy_history[-1][0]

        updated_policy = updated_policy*(reward + self._policy_history[-1][1] )

        for step, policy_reward in enumerate( self._policy_history[:-1] ) : 
            # check
            discount =(  n_steps - step )*self.discount
            print ('Policy history length = %d' %n_steps )
            print ('On step %d, diff = %d, discount = %f ' %( step, n_steps- step, discount ) )

            #cutoff the discount
            if discount > 0.9 : 
                discount = 0.9

            updated_policy += policy_reward[0] * ( reward + policy_reward[1] ) * (1. - discount )

        self.propagate_to_policy( updated_policy )

    def propagate_to_policy(self, updated )  :

        updated.normalize()

        self._policy = ( self._policy + updated ) *0.5

