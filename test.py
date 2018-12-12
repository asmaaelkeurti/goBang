import pandas as pd
import numpy as np
import random
import math
import copy
import time

class go_bang:
    def __init__(self,size):
        self.size = size
        self.board = np.zeros((self.size,self.size))
    
    def data_structure(self):
        l = []
        for i in range(self.size):
            for j in range(self.size):
                l = l + [[i,j,self.board[i,j]]]
                
        return pd.DataFrame(l,columns=['r','c','v'])
        
    def how_many_moves(self):
        df = self.data_structure()
        df = df[df['v'] == 0]
        return self.size * self.size - len(df)
    
    
    def go(self,position,value): 
        self.board[position[0],position[1]] = value
        
    def who_is_next(self):
        if self.board.sum() == 1:
            return -1
        else:
            return 1
        
    def who_is_last(self):
        if self.board.sum() == 1:
            return 1
        else:
            return -1
    
    def exist_5(self,array):
        i = 0
        count = 0
        value = 0
        while i < len(array):
            if array[i] != value:
                value = array[i]
                count = 0
            count = count + 1
            if count >=5 and value != 0:
                return value
            
            i = i + 1

        return 0
    
    
    def game_over(self):
        #check vertical
        for i in range(self.size):
            if self.exist_5(self.board[:,i]) != 0:
                return self.exist_5(self.board[:,i])
        
        #check horizontal
        for row in self.board:
            if self.exist_5(row) != 0:
                return self.exist_5(row)
    
        #check upper right to lower left
        for i in range(self.size):
            upper_right_lower_left_array = []
            
            j = 0
            jj = i
            while j <= i:
                upper_right_lower_left_array = upper_right_lower_left_array + [self.board[j,jj]]
                jj = jj -1
                j = j + 1
            
            if self.exist_5(upper_right_lower_left_array) != 0:
                return self.exist_5(upper_right_lower_left_array)

        for i in range(self.size):
            upper_right_lower_left_array = []
            
            j = self.size - 1
            jj = self.size - 1 - i
            while jj <= self.size - 1:
                upper_right_lower_left_array = upper_right_lower_left_array + [self.board[jj,j]]
                jj = jj + 1
                j = j - 1
            if self.exist_5(upper_right_lower_left_array) != 0:
                return self.exist_5(upper_right_lower_left_array)
            

        #check upper left to lower right
        for i in range(self.size):
            upper_left_lower_right_array = []
            
            j = self.size - 1 - i
            jj = 0
            while jj <= i:

                upper_right_lower_left_array = upper_right_lower_left_array + [self.board[j,jj]]
                jj = jj + 1
                j = j + 1
            
            if self.exist_5(upper_left_lower_right_array) != 0:
                return self.exist_5(upper_left_lower_right_array)
        
        for i in range(self.size):
            upper_left_lower_right_array = []
            
            j = self.size - 1 - i
            jj = 0
            while jj <= i:

                upper_left_lower_right_array = upper_left_lower_right_array + [self.board[jj,j]]
                jj = jj + 1
                j = j + 1
            
            if self.exist_5(upper_left_lower_right_array) != 0:
                return self.exist_5(upper_left_lower_right_array)
            
        df = self.data_structure()
        df = df[df['v'] == 0]
        if len(df) == 0:
            return 2    
        
        
        return 0
    
    
        
    
    def possible_position(self):
        df = self.data_structure()
        
        df_available = df[df['v'] == 0]
        df_unavailable = df[df['v'] != 0]
        
        def is_close_enough(x,y):
            for index, row in df_unavailable.iterrows():
                distance = math.sqrt((x-row['r'])**2 + (y-row['c'])**2)
                if distance < 3:
                    return 1
            return 0
        
        df_available['is_close'] = df_available[['r','c']].apply(lambda x : is_close_enough(*x),axis=1)
        
        df_available = df_available[df_available['is_close'] == 1]
        
        del df_available['is_close']
        return df_available
        
        
    

    def random_next_move(self):
        df = self.data_structure()
        df = df[df['v'] == 0]
        #df = self.possible_position()
        rows = np.random.choice(df.index.values, 1)
        df = df.loc[rows]
        next_value = self.who_is_next()
        self.go([int(df['r'].iloc[0]),int(df['c'].iloc[0])],next_value)
        return [df['r'].iloc[0],df['c'].iloc[0],next_value]
        

    def random_search(self):
        
        n1 = copy.deepcopy(self) 
        next_value = n1.who_is_next()
        
        [x,y,v] = n1.random_next_move()
        
        win = 0
        loss = 0
        
        for i in range(100):
            n1_next = copy.deepcopy(n1)
            while n1_next.game_over() == 0:
                n1_next.random_next_move()
            if n1_next.game_over() == next_value:
                win = win + 1
            elif n1_next.game_over() != 2:
                loss = loss + 1
        
        print([x,y,v,win,loss])
    


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
        start = time.time()
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
        
        end = time.time()
        print(end-start)
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

        

a = go_bang(10)
#a.go([0,1],-1)
a.go([0,2],-1)
a.go([0,3],-1)
a.go([0,4],-1)

#a.go([9,1],1)
a.go([9,2],1)
a.go([9,3],1)
a.go([9,4],1)
#a.go([9,5],1)
#print(a.game_over())
#print(a.board)
#
#
def go_next(current_state):
    root = node(current_state,current_state.who_is_next(),True,0,[])

    mcts = MCTS(root)
    mcts.running(1,300)
    position = mcts.make_move(1)
    print(position)
    current_state.go(position,current_state.who_is_next())
    print(current_state.board)
    
    return current_state


#root = node(a,a.who_is_next(),True,0,[])
#mcts = MCTS(root)
#mcts.running(1,200)
#r_df = mcts.stats()
#
#top_1 = r_df[(r_df['last_move_x'] == 9) & (r_df['last_move_y'] == 5)]['visit_times'].iloc[0]
#top_2 = r_df[(r_df['last_move_x'] == 9) & (r_df['last_move_y'] == 1)]['visit_times'].iloc[0]
#
#print([top_1,top_2,r_df['visit_times'].max()])
#counter = 200
#
#while not(top_1 == r_df['visit_times'].max() or top_2 == r_df['visit_times'].max()):
#    mcts.running(1,50)
#    r_df = mcts.stats()
#
#    top_1 = r_df[(r_df['last_move_x'] == 9) & (r_df['last_move_y'] == 5)]['visit_times'].iloc[0]
#    top_2 = r_df[(r_df['last_move_x'] == 9) & (r_df['last_move_y'] == 1)]['visit_times'].iloc[0]
#    
#    counter = counter + 50
#    print([top_1,top_2,r_df['visit_times'].max()])
#    print(counter)
    
    
#root.simulation()
#print(root.is_termination())
#n1=[node for node in mcts.root.leaves if node.last_move==[9,5]][0]
#print(n1.is_termination())
#a.go(go_next(a),a.who_is_next())

#[[i.score,i.win,i.loss,i.visit_times,i.last_move[0],i.last_move[1]] for i in mcts.root.leaves]
#df = pd.DataFrame(l,columns=['score','win','loss','visit_times','last_move_x','last_move_y'])
