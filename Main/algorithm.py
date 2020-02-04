# simulation package contains the Simulator and all abstract classes
from catsim.simulation import *
# initialization package contains different initial proficiency estimation strategies
from catsim.initialization import *
# selection package contains different item selection strategies
from catsim.selection import *
# estimation package contains different proficiency estimation methods
from catsim.estimation import *
# stopping package contains different stopping criteria for the CAT
from catsim.stopping import *
import numpy as np
import random

class CAT():
    def __init__(self, items):
        self.items = items
        self.responses = []
        self.administered_items = []

        # create a random proficiency initializer
        self.initializer = RandomInitializer()
        print('Creating simulation components...')

        # create a maximum information item selector
        self.selector = MaxInfoSelector()

        # create a hill climbing proficiency estimator
        self.estimator = HillClimbingEstimator()

        # create a stopping criterion that will make tests stop after 10 items
        self.stopper = MaxItemStopper(10)

        # manually initialize an examinee's proficiency as a float variable
        self.est_theta = self.initializer.initialize()
        self.thetas = [self.est_theta]
        print('Examinee initial proficiency:', self.est_theta)

    def item_selection():
        # get the index of the next item to be administered to the current examinee, given the answers they have already given to the previous dummy items
        item_index = selector.select(items=items, administered_items=administered_items, est_theta=est_theta)
        print('Next item to be administered:', item_index)

        # get a boolean value pointing out whether the test should stop
        _stop = stopper.stop(administered_items=items[administered_items], theta=est_theta)
        print('Should the test be stopped:', _stop)
    
        return (_stop, item_index)

    def item_administration():
        # get an new estimated theta
        new_theta = estimator.estimate(items=items, administered_items=administered_items, response_vector=responses, est_theta=est_theta)
        print('Estimated proficiency, given answered items:', new_theta)
        thetas.append(new_theta)

    def process():
        while True:
            administered_items.append(item_index)
    
            response = bool(int(input())) # Get user respone for current question
            responses.append(response)
    
            item_administration()
    
            (_stop, item_index) = item_selection() # Get next item
    
            if _stop:
                break