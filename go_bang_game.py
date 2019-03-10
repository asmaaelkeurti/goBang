import pandas as pd
import numpy as np
import math
import copy
import unittest

class go_bang:
    def __init__(self,size):
        self.size = size
        self.board = np.zeros((self.size,self.size))
        self.last_move = [-1,-1]
    
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
        self.last_move = [position[0],position[1]]
        
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
        x,y = self.last_move[0],self.last_move[1]
        if (x < 0 or y < 0):
            return 0
        
        horizontal_list = []
        upper_left_lower_right_list = []
        lower_left_upper_right_list = []
        vertical_list = []
        #Upper left lower right
        #
        for i in range(-5,6):
            if x+i > 0 and x+i < self.size:
                horizontal_list = horizontal_list + [self.board[x+i,y]]
                if y+i > 0 and y+i < self.size:
                    upper_left_lower_right_list = upper_left_lower_right_list + [self.board[x+i,y+i]]
                if y-i > 0 and y-i < self.size:
                    lower_left_upper_right_list = lower_left_upper_right_list + [self.board[x+i,y-i]]
            if y+i > 0 and y+i < self.size:
                vertical_list = vertical_list + [self.board[x,y+i]]
                
        for l in [horizontal_list,upper_left_lower_right_list,lower_left_upper_right_list,vertical_list]:
            if self.exist_5(l) != 0:
                return self.exist_5(l)
        
        
        
        df = self.data_structure()
        df = df[df['v'] == 0]
        if len(df) == 0:
            return 2    
        
        return 0
        
    
    def game_over_1(self):
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
        
class go_bang_unit_test(unittest.TestCase):
    def test_horizontal_game_over(self):
        game = go_bang(10)

        game.go([0,2],-1)
        game.go([0,3],-1)
        game.go([0,4],-1)
        game.go([0,5],-1)
        
        game.go([9,2],1) 
        game.go([9,3],1)
        game.go([9,4],1) 
        game.go([9,5],1)
        game.go([9,6],1)
        self.assertEqual(game.game_over(),1)
    
    def test_vertical_game_over(self):
        a = go_bang(10)

        a.go([0,2],-1)
        a.go([0,3],-1)
        a.go([0,4],-1)
        a.go([0,5],-1)
        
        a.go([5,4],1) 
        a.go([6,4],1)
        a.go([7,4],1) 
        a.go([8,4],1)
        a.go([9,4],1)
        self.assertEqual(a.game_over(),1)
        
    def test_upper_left_to_lower_right_game_over_1(self):
        a = go_bang(10)

        a.go([0,2],-1)
        a.go([0,3],-1)
        a.go([0,4],-1)
        a.go([0,1],-1)
        
        a.go([5,2],1) 
        a.go([6,3],1)
        a.go([7,4],1) 
        a.go([8,5],1)
        a.go([9,6],1)
    
        self.assertEqual(a.game_over(),1)
        
    def test_upper_right_to_lower_left_game_over_1(self):
        a = go_bang(10)

        a.go([0,2],-1)
        a.go([0,3],-1)
        a.go([0,4],-1)
        a.go([0,1],-1)
        
        a.go([5,6],1) 
        a.go([6,5],1)
        a.go([7,4],1) 
        a.go([8,3],1)
        a.go([9,2],1)
    
        self.assertEqual(a.game_over(),1)


if __name__ == '__main__':
    unittest.main()
