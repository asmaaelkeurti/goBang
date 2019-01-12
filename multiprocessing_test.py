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
    mcts.running(1,500)
    return mcts

if __name__ == '__main__':
    a = go_bang(13)

    a.go([0,2],-1)
    a.go([0,3],-1)
    a.go([0,4],-1)
    
    a.go([9,2],1)
    a.go([9,3],1)
    a.go([9,4],1)
    
    root = node(a,a.who_is_next(),True,0,[])
    mcts = MCTS(root)
    
    n_process = 7
    
    mcts_list = [copy.deepcopy(mcts) for i in range(n_process)]
#    
    with Pool(processes=n_process) as pool:
        result = pool.map(mcts_running, mcts_list)

    
    m = merged_df(result[0].stats(),result[1].stats())
    for i in range(2,n_process):
        m = merged_df(m,result[i].stats())
    