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

    ######### BEGIN: Write here your model for Task 1
    x = {}
    for i in V:
        for j in range(i + 1):
            x[i, j] = m.addVar(obj=tsputil.distance(points[i], points[j]),
                               vtype=GRB.BINARY)
            x[j, i] = x[i, j]
        m.update()

    # 1.
    for i in V:
        m.addConstr(quicksum(x[i, j] for j in V) +
                    quicksum(x[j, i] for j in V) == 2)
        x[i, i].ub = 0

    m.update()

    # 2.
    for s in subtours:
        m.addConstr(quicksum(x[i, j] for i, j in E if i in s if j in s) <= len(s) - 1)

    obj = quicksum(m.getVars())

    m.setObjective(obj, GRB.MAXIMIZE)

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

    ######### BEGIN: Write here your model for Task 4

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
    points = tsputil.Cities(n=12, seed=12)
    # tsputil.plot_situation(points)

    # points = tsputil.read_instance("dantzig42.dat")
    subtours = list(powerset(range(len(points))))
    # The first element of the list is the empty set and the last element is the full set, hence we remove them.
    subtours = subtours[1:(len(subtours) - 1)]

    # task 2
    tsplp0 = solve_tsp(points, [])
    tsputil.plot_situation(points, tsplp0)

    task
    4


if __name__ == "__main__":
    main(sys.argv[1:])
