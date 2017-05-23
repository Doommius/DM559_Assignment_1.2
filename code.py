from gurobipy import *
from collections import OrderedDict
import tsputil
import math



def solve_tsp(points1, subtours=[]):
    points = list(points1)

    V = range(len(points))
    E = [(i, j) for i in V for j in V if i < j]
    E = tuplelist(E)

    m = Model("TSP0")
    m.setParam(GRB.param.Presolve, 0)
    m.setParam(GRB.param.Method, 0)
    m.setParam(GRB.param.MIPGap, 1e-7)

    ######### BEGIN: Write here your model for Task 1
    edges = {}
    for i in range(len(points)):
        for j in range(i + 1):
            #if (i != j):
                edges[i, j] = m.addVar(obj=tsputil.distance(points[i], points[j]),
                                  name='edge_' +str(i) + '_' + str(j))
                edges[j, i] = edges[i, j]
        m.update()

    # Add degree-2 constraint, and forbid loops

    for i in range(len(points)):
        m.addConstr(quicksum(edges[i, j] for j in range(len(points))) == 2)
        edges[i, i].ub = 0



    obj = quicksum(m.getVars())


    m.update()

    m.setObjective(obj, GRB.MAXIMIZE)
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

def main(argv):

    # points = tsputil.Cities(n=20, seed=12)
    # tsputil.plot_situation(points)

    points = tsputil.read_instance("dantzig42.dat")

    print(list(points))

    plotlist = solve_tsp(points,[])

    tsputil.plot_situation(plotlist)
    print("test")




if __name__ == "__main__":
    main(sys.argv[1:])

