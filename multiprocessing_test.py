from multiprocessing import Pool
from test import *
import copy


def merged_df(df1,df2):
    merged_df = df1[['last_move_x','last_move_y','visit_times']].merge(df2[['last_move_x','last_move_y','visit_times']],on=['last_move_x','last_move_y'])
    merged_df['visit_times'] = merged_df['visit_times_x'] + merged_df['visit_times_y']
    merged_df.drop(['visit_times_x', 'visit_times_y'], axis=1,inplace=True)
    return merged_df

def f(x):
    return x*x

def mcts_running(mcts):
    mcts.running(1.2,200)
    return mcts

if __name__ == '__main__':
    a = go_bang(10)

    a.go([0,2],-1)
    a.go([0,3],-1)
    a.go([0,4],-1)
    
    a.go([9,2],1)
    a.go([9,3],1)
    a.go([9,4],1)
    
    root = node(a,a.who_is_next(),True,0,[])
    mcts = MCTS(root)
    
    mcts_list = [copy.deepcopy(mcts) for i in range(3)]
    
    with Pool(processes=3) as pool:
        result = pool.map(mcts_running, mcts_list)
#        print(result)
    
    
    
    df1,df2,df3 = result[0].stats(),result[1].stats(),result[2].stats()
    
    m_d1d2 = merged_df(df1,df2)
    m_d1d2d3 = merged_df(m_d1d2,df3)
    