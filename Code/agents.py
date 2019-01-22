from mesa import Agent
from utility import *
import matplotlib.pyplot as plt
import random
from globals import *
class agent(Agent):
    """ An agent with fixed initial preference and opinion."""

    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.preference = set_rand_unifrom_preference()
        self.opinion = set_opinion()
        # print(self.preference)

    
    def select_A(self, A_preference):
        """ Adapt preference score and opinion to A"""
        if self.opinion == 1:
            self.preference = 1 - self.preference
        
        self.opinion = 0
        update_preference(self.preference, A_preference)

    def select_B(self, B_preference):
        """ Adapt preference score and opinion to A"""
        if self.opinion == 0:
            self.preference = 1 - self.preference

        self.opinion = 1
        update_preference(self.preference, B_preference)

    def form_opinion(self, neighbors):
        """ Function to determine if opninion needs to be adapted based on neighbors""" 
        #function 
        neighbor_preference = []
        A_preference = []
        B_preference = []

        for neighbor in neighbors:
            neighbor_preference.append(neighbor.preference)
            if neighbor.opinion == 0:
                A_preference.append(neighbor.preference)
            else:
                B_preference.append(neighbor.preference)

        if(len(neighbor_preference)!=0):
            probability_rate_A = sum(A_preference)/sum(neighbor_preference)
            probability_rate_B = sum(B_preference)/sum(neighbor_preference)

            if (self.opinion == 0) and (probability_rate_B < self.preference):
                self.select_A(A_preference)
            
            if (self.opinion == 1) and (probability_rate_A < self.preference):
                self.select_B(B_preference)
            if random.uniform(0,1) < probability_rate_A:
                self.select_A(A_preference)
            else:
                self.select_B(B_preference)


    def choose_neighbors(self, neighbors):
        """ Choose whitch neighbors to talk with based on reputation"""
        selected_neighbors = []
        for neighbor in neighbors:
            if neighbor.opinion == self.opinion:
                similarity_constraint = abs(neighbor.preference - self.preference)
            else:
                similarity_constraint = neighbor.preference + self.preference


            reputation = (self.model.G.edges[self.pos,neighbor.pos]['times_agreed']/self.model.G.edges[self.pos,neighbor.pos]['total_encounters'])*(1-(similarity_constraint/2))

            if( reputation > np.random.uniform(0,1)):
                selected_neighbors.append(neighbor)
                if(reputation < high_edge_strength):
                    reputation += edge_strength_chance
            else: 
                if(reputation > low_edge_strength):
                    reputation -= edge_strength_chance

        return selected_neighbors

    def talk(self):
        '''
        Agent sees neighbors. Select neighbors to talk with (based on edge strenght). Increase connection strength if shared opinion. 
        Start Discussion, chance opinion according to probabilitiy function
        '''
        neigbors_nodes = self.model.grid.get_neighbors(self.pos, include_center = False)
        neighbors = self.model.grid.get_cell_list_contents(neigbors_nodes)
        selected_neighbors = self.choose_neighbors(neighbors)


        self.form_opinion(selected_neighbors)

        # new_preference = mean_neighbor_preference(neighbors)
        # self.preference = new_preference
        # print(self.preference)

    def step(self):
        """ Function to intarate over time with the mesa modual"""
        # self.preference += 1
        self.talk()
        # print(self.unique_id)
    # def get_neighbours(self):

    # def get_neigbor_nodes():
