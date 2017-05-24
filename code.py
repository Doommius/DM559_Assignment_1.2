from gurobipy import *
from collections import OrderedDict
import tsputil
import math

from itertools import chain, combinations


def solve_tsp(points1, subtours):
    points = list(points1)

    V = range(len(points))
    E = [(i, j) for i in V for j in V if i < j]
    E = tuplelist(E)

    m = Model("TSP0")
    m.setParam(GRB.param.Presolve, 0)
    m.setParam(GRB.param.Method, 0)
    m.setParam(GRB.param.MIPGap, 1e-7)

    '''
    ######### BEGIN: Write here your model for Task 1
    x = {}
    for i,j in E:
        x[i, j] = m.addVar(vtype=GRB.BINARY)

    m.update()

    # 1.
    for i in V:
        m.addConstr(quicksum(x[i, j] for j in V if i < j) +
                    quicksum(x[j, i] for j in V if j < i) == 2)

    m.update()

    # 2.
    for s in subtours:
        m.addConstr(quicksum(x[i, j] for i, j in E if i in s if j in s) <= len(s)-1 )

    obj = quicksum(tsputil.distance(points[i], points[j]) * x[i,j] for i in V for j in V if i < j)

    m.setObjective(obj, GRB.MINIMIZE)

    m.update()

    ######### END
    '''

    '''
    ######### BEGIN: Write here your model for Task 2
    x = {}
    for i, j in E:
        x[i, j] = m.addVar(vtype=GRB.CONTINUOUS)
        x[i, j].lb = 0
        x[i, j].ub = 1

    m.update()

    # 1.
    for i in V:
        m.addConstr(quicksum(x[i, j] for j in V if i < j) +
                    quicksum(x[j, i] for j in V if j < i) == 2)

    m.update()

    obj = quicksum(tsputil.distance(points[i], points[j]) * x[i, j] for i in V for j in V if i < j)

    m.setObjective(obj, GRB.MINIMIZE)

    m.update()

    ######### END
    '''

    ######### BEGIN: Write here your model for Task 3
    x = {}
    for i,j in E:
        x[i, j] = m.addVar(vtype=GRB.BINARY)

    m.update()

    # 1.
    for i in V:
        m.addConstr(quicksum(x[i, j] for j in V if i < j) +
                    quicksum(x[j, i] for j in V if j < i) == 2)

    m.update()

    # 2.
    for s in subtours:
        m.addConstr(quicksum(x[i, j] for i, j in E if i in s if j in s) <= len(s)-1 )

    obj = quicksum(tsputil.distance(points[i], points[j]) * x[i,j] for i in V for j in V if i < j)

    m.setObjective(obj, GRB.MINIMIZE)

    m.update()

    ######### END

    m.optimize()
    m.write("tsplp.lp")

    if m.status == GRB.status.OPTIMAL:
        print('The optimal objective is %g' % m.objVal)
        m.write("tsplp.sol")  # write the solution
        return {(i, j): x[i, j].x for i, j in x}
    else:
        print
        "Something wrong in solve_tsplp"
        exit(0)




    return 0



# task 5
def solve_separation(points, x_star, k):
    points = list(points)
    V = range(len(points))
    Vprime = range(1, len(points))
    E = [(i, j) for i in V for j in V if i < j]
    Eprime = [(i, j) for i in Vprime for j in Vprime if i < j]
    E = tuplelist(E)
    Eprime = tuplelist(Eprime)

    m = Model("SEP")
    m.setParam(GRB.param.OutputFlag, 0)

    ######### BEGIN: Write here your model for Task 5
    z = {}
    for i in range(len(points)):
        z[i] = m.addVar(vtype=GRB.BINARY)
    y = m.addVar(vtype=GRB.BINARY)
    m.update()

    m.addConstr(y >= z[i] + z[j] - 1)
    m.addConstr(y <= z[i])
    m.addConstr(y <= z[j])

    obj = quicksum(x_star[i,j] * y for i,j in Eprime if i < j) - quicksum(z[i] for i in Vprime if i != k)

    m.setObjective(obj, GRB.MAXIMIZE)

    ######### END
    m.optimize()
    m.write("sep.lp")

    if m.status == GRB.status.OPTIMAL:
        print('Separation problem solved for k=%d, solution value %g' % (k, m.objVal))
        m.write("sep.sol")  # write the solution
        subtour = filter(lambda i: z[i].x >= 0.99, z)
        return m.objVal, subtour
    else:
        print
        "Something wrong in solve_tsplp"
        exit(0)


        # return 0



#task 6
def cutting_plane_alg(points):
    Vprime = range(1,len(points))
    subtours = []
    found = True
    while found:
        lpsol = solve_tsp(points,subtours)
        tsputil.plot_situation(points, lpsol)
        found = False
        tmp_subtours = []
        best_val = float('-inf')
        for k in Vprime:
            value, subtour = solve_separation(points,lpsol,k)
            best_val = value if value > best_val else best_val
            ######### BEGIN: write here the condition. Include a tollerance
            if False:
            ######### END
                found = True
                tmp_subtours += [subtour]
        subtours += tmp_subtours
        print ('*'*60)
        print ("********** Subtours found: ",tmp_subtours," with best value : ",best_val)
        print ('*'*60)
    tsputil.plot_situation(points, lpsol)

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def main(argv):
    n = 20
    seed = 1200
    points = tsputil.Cities(n, seed)

    #task 1
    #subtours = list(powerset(range(len(points))))
    # The first element of the list is the empty set and the last element is the full set, hence we remove them.
    #subtours = subtours[1:(len(subtours) - 1)]
    # tsplp = solve_tsp(points, subtours)
    #print tsplp

    #task 2
    tsplp_0 = solve_tsp(points, [])
    print (tsplp_0)
    #tsputil.plot_situation(points, tsplp_0)

    '''
    #task 3
    subtours = [[1,2,6,19, 14, 3, 10, 8, 11, 4, 7, 18],[0,16,17],[5,13,9,12,15]]
    
    subtours = [[1,2,6,19, 14, 3, 10, 8, 11, 4, 7, 18],[0,16,17],[5,13,9,12,15],
                    [1,2,6,19,14,3,10,8,11,4,0,17,16,7,18], [5,13,9,12,15]]

    subtours = [[1,2,6,19, 14, 3, 10, 8, 11, 4, 7, 18],[0,16,17],[5,13,9,12,15],
                    [1,2,6,19,14,3,10,8,11,4,0,17,16,7,18], [5,13,9,12,15],
                        [0,7,18,1,16,17], [4,8,11], [2,3,14,19,6], [5,10,13,9,12,15]]

    tsplp_1 = solve_tsp(points, subtours)
    print tsplp_1
    tsputil.plot_situation(points, tsplp_1)
    '''

    #task 4
    # modelling..

    #task 5
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"
    print "jens\n"

    print solve_separation(points, tsplp_0, 1)
    tsputil.plot_situation(points, tsplp_0)

if __name__ == "__main__":
    main(sys.argv[1:])
