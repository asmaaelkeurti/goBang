import numpy as np
import pandas as pd
import random

import copy

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
        
    
    def go(self,position,value):        
        self.board[position[0],position[1]] = value
        
    def who_is_next(self):
        if self.board.sum() == 1:
            return -1
        else:
            return 1
    
    def exist_5(self,array):
        i = 0
        count = 0
        value = 0
        while i < len(array):
            if array[i] != 0:
                if array[i] != value:
                    value = array[i]
                    count = 0
                count = count + 1
            i = i + 1
            
            
        if count >= 5:
            return value
        else:
            return 0
    
    def game_over(self):
        #check vertical
        for i in range(self.size):
            if self.exist_5(self.board[:,i]) != 0:
                return self.exist_5(self.board[:,i])
        
        #check horizontal
        for row in a.board:
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
        

    def random_next_move(self):
        df = self.data_structure()
        df = df[df['v'] == 0]
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
        

class Nodo
        


a = go_bang(10)
#a.go([8,3],-1)
#a.go([7,4],-1)
#a.go([6,5],-1)
#a.go([5,6],-1)
#a.go([4,7],-1)

print(a.game_over())
print(a.board)








