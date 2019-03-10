import pandas as pd
import numpy as np
import random
import math
import copy
import time

class MCTS:
    def __init__(self, root):
        self.root = root
        
        
    def stats(self):
        l = [[i.score,i.win,i.loss,i.visit_times,i.last_move[0],i.last_move[1]] for i in self.root.leaves]
        df = pd.DataFrame(l,columns=['score','win','loss','visit_times','last_move_x','last_move_y'])
        return df
        
    def running(self,c,turns):        
        counter = 0
        while counter < turns:
            counter = counter + 1
            self.run(self.root,c)

            
    def run(self,node,c):
        if not node.is_visited:
            node.simulation()
            node.update_stats(c)
            return
        elif node.is_termination():
            node.simulation()
            node.update_stats(c)
            return
#        elif not node.has_leaves():
#            node.update_stats(c)
#            return
        else:
            child_node = node.select_child_node(c)
            self.run(child_node,c)
            node.update_stats(c)            
        
    def make_move(self,c):
        child = self.root.select_child_node(c)
#        while not child.is_visited:
#            child = self.root.select_child_node(c)
        
        df = self.root.state.data_structure().merge(child.state.data_structure(),on=['r','c'])
        r = df[df['v_x']!=df['v_y']]['r'].iloc[0]
        c = df[df['v_x']!=df['v_y']]['c'].iloc[0]
        
        #self.root = child
        return [r,c]
        
        
        

class node:
    def __init__(self, go_bang_state,who_wants_to_win,is_root,parent_visit_times,last_move):
        self.is_root = is_root
        self.parent_visit_times = parent_visit_times
        self.state = go_bang_state
        self.is_visited = False
        
        self.win = 0            #win or loss is relative to who_wants_to_win
        self.loss = 0
        self.due = 0
        
        self.self_win = 0
        self.self_loss = 0
        self.self_due = 0
        self.self_visit_times = 0
        
        self.visit_times = 0
        
        self.who_is_next = self.state.who_is_next()
        self.who_is_last = self.state.who_is_last()
        self.who_wants_to_win = who_wants_to_win
        self.leaves = []
        self.score = -1
        self.last_move = last_move
        
    def simulation(self):
        self.is_visited = True
        self.self_visit_times = self.self_visit_times + 1
        
        c1 = copy.deepcopy(self.state)
        while c1.game_over() == 0:
            c1.random_next_move()
        if c1.game_over() == self.who_wants_to_win:
            self.self_win = self.self_win + 1
        elif c1.game_over() == 2:
            self.self_due = self.self_due + 1
        else:
            self.self_loss = self.self_loss + 1
        
        if not self.is_termination():
            self.populate_leaves()
        
        
    def is_termination(self):
        if self.state.game_over() != 0:
            return True
        else:
            return False
        
    def has_leaves(self):
        if len(self.leaves) > 0:
            return True
        else:
            return False
            
    def populate_leaves(self):
        #df = self.state.data_structure()
        df = self.state.possible_position()
        df = df[df['v'] == 0].sample(frac=1)
        for index, rows in df.iterrows():
            c1 = copy.deepcopy(self.state)
            c1.go([int(rows['r']), int(rows['c'])],c1.who_is_next())
            self.leaves = self.leaves + [node(c1,self.who_wants_to_win,False,self.visit_times,
                                              [int(rows['r']), int(rows['c'])])]
    
    def select_child_node(self,c):
        #print(self.state.how_many_moves())
        for leaf in self.leaves: 
            leaf.parent_visit_times = self.visit_times
            if not leaf.is_visited:
                return leaf
        self.leaves.sort(key = lambda x:x.score,reverse = True)
        return self.leaves[0]

    def update_stats(self,c):
        self.win = sum(leaf.win for leaf in self.leaves) + self.self_win
        self.loss = sum(leaf.loss for leaf in self.leaves) + self.self_loss
        self.due = sum(leaf.due for leaf in self.leaves) + self.self_due
        self.visit_times = sum(leaf.visit_times for leaf in self.leaves) + self.self_visit_times
        
        if self.is_root:
            pass
        else:
            if self.who_wants_to_win == self.who_is_last:
                self.score = self.win/self.visit_times + c*math.sqrt(math.log10(self.parent_visit_times)/self.visit_times)
            else:
                self.score = self.loss/self.visit_times + c*math.sqrt(math.log10(self.parent_visit_times)/self.visit_times)
