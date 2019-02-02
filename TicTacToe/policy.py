

class policy : 

    def __init__(self) : 

        self._policy = []
        self._policy.append(np.zeros( 9 ))  
        self._policy.append(np.zeros( (9,9) ))
        self._policy.append(np.zeros( (9,9,9) ))
        self._policy.append(np.zeros( (9,9,9,9) ))
        self._policy.append(np.zeros( (9,9,9,9,9) ))
        self._policy.append(np.zeros( (9,9,9,9,9,9) ))
        self._policy.append(np.zeros( (9,9,9,9,9,9,9) ))
        self._policy.append(np.zeros( (9,9,9,9,9,9,9,9) ))


    def set( self, step, state, play ) : 

        if not isinstance( play, list ) : 
            play = [play]

        all_vals = state+play
        counts = [ all_vals.count(i) for i in all_vals ]
        if max( counts ) > 1 : 
            print ('ERROR, duplicate entries for state')
            print (state)
            return

        for i in state : 



        

        self._policy[step]


