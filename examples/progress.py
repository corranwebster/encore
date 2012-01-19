import time
import random
from uuid import uuid4
from encore.events.api import EventManager, ProgressManager
from encore.terminal.api import ProgressDisplay

class CosmicRayError(Exception):
    """ An artifical exception type to play with """
    pass

class ProgressApplication(object):
    """ A simple application that demonstrates ProgressManagers and ProgressDisplays """
    
    def __init__(self):
        self.event_manager = EventManager()
        self.display = ProgressDisplay(self.event_manager)
    
    def run(self):
        # create some dummy progress bars
        for j in range(10):
            operation_id = uuid4()
            steps = random.randint(0,600)
            known = random.randint(0,4)
            fail_point = random.randint(0, 2400)
            
            # create a progress manager
            progress = ProgressManager(self.event_manager, source=self,
                operation_id=operation_id,
                steps=steps if known else -1,
                message="Doing something %d" % j)
            try:
                with progress:
                    for i in range(steps):
                        time.sleep(random.uniform(0, 0.01))
                        if i > fail_point:
                            raise CosmicRayError('Cosmic ray hit a memory location')
                        progress(step=i+1, message="Working...")
            except CosmicRayError:
                # skip our artificial exceptions and move on with the next iteration
                pass

def main():
    app = ProgressApplication()
    app.run()
    

if __name__ == '__main__':
    main()