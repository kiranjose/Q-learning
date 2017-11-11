__author__ = 'philippe'
import World
import threading
import time

discount = 0.3
actions = World.actions
states = []
Q = {}
#initialising all possible states
for i in range(World.x):
    for j in range(World.y):
        states.append((i, j))
#defaulting all possible Q[state] value to 0.1
for state in states:
    temp = {}
    for action in actions:
        temp[action] = 0.1
        World.set_cell_score(state, action, temp[action])
    Q[state] = temp
    #printing default Q table values
    print 'Q',state,'->',Q[state]
#updating special Q[states]s with reward and penality
for (i, j, c, w) in World.specials:
    for action in actions:
        Q[(i, j)][action] = w
        #printing updated values of Q table
        print 'Q(',i,',',j,')',action,'->',w
        World.set_cell_score((i, j), action, w)

#printing out entire Q table after updation
for i in range(World.x):
    for j in range(World.y):
        print Q[i,j]

def do_action(action):
    s = World.player
    r = -World.score
    print 'World.score bef mov',World.score
    print 'reward before move',r
    if action == actions[0]:
        World.try_move(0, -1)
    elif action == actions[1]:
        World.try_move(0, 1)
    elif action == actions[2]:
        World.try_move(-1, 0)
    elif action == actions[3]:
        World.try_move(1, 0)
    else:
        return
    s2 = World.player
    r += World.score
    print 'reward after move',r
    return s, action, r, s2


def max_Q(s):
    val = None
    act = None
    for a, q in Q[s].items():
        if val is None or (q > val):
            val = q
            act = a
    return act, val


def inc_Q(s, a, alpha, inc):
    Q[s][a] *= 1 - alpha
    Q[s][a] += alpha * inc
    World.set_cell_score(s, a, Q[s][a])


def run():
    global discount
    time.sleep(0.1)
    alpha = 1
    t = 1
    print 'Start run()'
    while True:
        # Pick the right action
        s = World.player
        max_act, max_val = max_Q(s)
        print 'max act->',max_act,' max_val=> ',max_val
        (s, a, r, s2) = do_action(max_act)
        print 'currentstate-> ',s,' action-> ',a,' reward-> ',r,' nextstate-> ',s2
        print 'QbeforeS(',s,')',Q[s]
        print 'QbeforeS2(',s2,')',Q[s2]
        # Update Q
        max_act, max_val = max_Q(s2)
        inc_Q(s, a, alpha, r + discount * max_val)
        print 'QafterS(',s,')',Q[s]
        print 'QafterS2(',s2,')',Q[s2]
        # Check if the game has restarted
        t += 1.0
        if World.has_restarted():
            World.restart_game()
            time.sleep(0.01)
            t = 1.0
            

        # Update the learning rate
        alpha = pow(t, -0.1)

        # MODIFY THIS SLEEP IF THE GAME IS GOING TOO FAST.
        time.sleep(.005)


t = threading.Thread(target=run)
t.daemon = True
t.start()
World.start_game()
