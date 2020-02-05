# this function generates an item bank, in case the user cannot provide one
from catsim.cat import generate_item_bank
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

def generate_bank():
    # generating an item bank
    print('Generating item bank...')
    bank_size = 100
    
    return(generate_item_bank(bank_size, '1PL'))

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

    def item_selection(self):
        # get the index of the next item to be administered to the current examinee, given the answers they have already given to the previous dummy items
        item_index = self.selector.select(items=self.items, administered_items=self.administered_items, est_theta=self.est_theta)
        print('Next item to be administered:', item_index)

        # get a boolean value pointing out whether the test should stop
        _stop = self.stopper.stop(administered_items=self.items[self.administered_items], theta=self.est_theta)
        print('Should the test be stopped:', _stop)
    
        return (_stop, item_index)

    def item_administration(self):
        # get an new estimated theta
        new_theta = self.estimator.estimate(items=self.items, administered_items=self.administered_items, response_vector=self.responses, est_theta=self.est_theta)
        print('Estimated proficiency, given answered items:', new_theta)
        self.thetas.append(new_theta)