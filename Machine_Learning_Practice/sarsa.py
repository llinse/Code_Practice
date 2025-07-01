#徐潇涵 201800820149 数据科学与人工智能班

#打印结果包含：每100个episode的平均steps ； q_value ; 最小steps ；程序所用时间
#epsilon取值为0.1, alpha为增强训练效果修改为0.5, gamma取值为1

import numpy as np
import matplotlib
matplotlib.use('Agg')
import time

WORLD_HEIGHT = 9
WORLD_WIDTH = 7
WIND = [0, 1, 0, 2, 2, 1, 2, 0, 1]
ACTION_N = 0
ACTION_S = 1
ACTION_W = 2
ACTION_E = 3
EPSILON = 0.1
ALPHA = 0.5
REWARD = -1.0
START = [0, 3]
GOAL = [5, 3]
ACTIONS = [ACTION_N, ACTION_S, ACTION_W, ACTION_E]

def step(state, action):
    i, j = state
    if action == ACTION_N and j+1+WIND[i]>6:
        return [i,min(j+1+WIND[i],6),-5]
    elif action == ACTION_N and j+1+WIND[i]<6:
        return [i, min(j + 1 + WIND[i], 6), -1]

    elif action == ACTION_S and [j-1+WIND[i]<0 or j-1+WIND[i]>6]:
        return [i,max(min(j-1+WIND[i],6),0),-5]
    elif action == ACTION_S and [j-1+WIND[i]>0 and j-1+WIND[i]<6]:
        return [i,max(min(j-1+WIND[i],6),0),-1]

    elif action == ACTION_W and [i-1<0 or j+WIND[i]>6]:
        return [max(i-1,0), min(j+WIND[i],6),-5]
    elif action == ACTION_W and [i-1>0 and j+WIND[i]<6]:
        return [i-1, min(j+WIND[i],6),-1]

    elif action == ACTION_E and [i+1>8 or j+WIND[i]>6]:
        return [8,6,-5]
    elif action == ACTION_E and [i+1<8 and j+WIND[i]<6]:
        return [i+1,j+WIND[i],-1]

    elif i==5 and j==3:
        return [5,3,0]

def episode(q_value):
    time = 0
    state = START

    # choose an action based on epsilon-greedy algorithm
    if np.random.binomial(1, EPSILON) == 1:
        action = np.random.choice(ACTIONS)
    else:
        values_ = q_value[state[0], state[1], :]
        action = np.random.choice([action_ for action_, value_ in enumerate(values_) if value_ == np.max(values_)])

    # keep going until get to the goal state
    while state != GOAL:
        #next = step(state, action)
        next_state = step(state, action)[:2]
        REWARD = step(state, action)[2:]
        if np.random.binomial(1, EPSILON) == 1:
            next_action = np.random.choice(ACTIONS)
        else:
            values_ = q_value[next_state[0], next_state[1], :]
            next_action = np.random.choice([action_ for action_, value_ in enumerate(values_) if value_ == np.max(values_)])

        # Sarsa update
        q_value[state[0], state[1], action] += \
            ALPHA * (REWARD + q_value[next_state[0], next_state[1], next_action] -
                     q_value[state[0], state[1], action])
        state = next_state
        action = next_action
        time += 1
    return time

def sarsa():
    q_value = np.zeros((WORLD_HEIGHT, WORLD_WIDTH, 4))
    episode_limit = 10000

    steps = []
    steps2 = []
    ep = 0
    ep1 = []
    while ep < episode_limit:
        steps.append(episode(q_value))
        # time = episode(q_value)
        # episodes.extend([ep] * time)
        ep += 1
        if ep%10==0:
            steps1 = np.add.reduce(steps[-10:])
            steps2.append(steps1)
            ep1.append(ep)
            print("episode = %d ; steps in last 100 episodes = %d ,average steps per episode = %d" %(ep,steps1,steps1/10))
    print(q_value)
    end = time.time()
    mi1=min(steps2)
    m=ep1[steps2.index(min(steps2))]
    n=m-99
    print("From episode %d to episode %d, the minimum of total steps is reached at %d" %(n,m,mi1))
    #print("Total time (in seconds) is:\n%f" %(end - start))

if __name__ == '__main__':
    sarsa()