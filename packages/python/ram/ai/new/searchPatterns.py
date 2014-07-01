import ram.ai.new.motionStates as motion
import ram.ai.new.utilStates as utilStates
import ram.ai.new.stateMachine as stateMachine
import ram.ai.Utility as oldUtil

#search patterns require a search machine which performs the motions associated with searching, and a function which returns true if the search has failed
#success and failure are the destination state ids for the success and failure cases
#if not present, the failure case will also map to next
#unlike constrainedState, SearchPattern has two parameters for stopping
#the first is the success conditions, the second are the termination conditions
#note that search patterns must ALWAYS have a failure case, if you always wan't to go to the same state then make success and failure both the same state ID
class SearchPattern(utilStates.ConstrainedState):
    def __init__(self,searchMachine,stopConditions,success,failure,constraint = lambda: True):
        #a search pattern only sucforwardceeds if its stop condition is met, it always if the search pattern finishes, or if a constraint is met
        super(SearchPattern,self).__init__(searchMachine,constraint,failure,failure)
        self.setTransition('next', success)
        self._stopConditions = stopConditions
        
    def update(self):
        if(self._stopConditions()):
            self.doTransition('next')
        else:
            super(SearchPattern, self).update()
    
    def leave(self):
        oldUtil.freeze(self.getStateMachine().getLegacyState())


#A simplistic search machine, it merely moves forwards a prespecified distance
class ForwardsSearchMachine(stateMachine.StateMachine):
    def __init__(self,distance):
        super(ForwardsSearchMachine,self).__init__()
        start = self.addState('start',utilStates.Start())
        end = self.addState('end',utilStates.End())
        move = self.addState('move',motion.Forward(distance))
        start.setTransition('next', 'move')
        move.setTransition('next', 'end')
        
class ForwardsSearchPattern(SearchPattern):
    def __init__(self,searchDistance, stopConditions, success, failure,constraint = lambda: True):
        super(ForwardsSearchPattern,self).__init__(ForwardsSearchMachine(searchDistance),stopConditions,success,failure,constraint)
        
