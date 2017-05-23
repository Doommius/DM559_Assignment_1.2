from gurobipy import *
from collections import OrderedDict
import tsputil
import math



# Callback - use lazy constraints to eliminate sub-tours

def subtourelim(model, where):
  if where == GRB.callback.MIPSOL:
    selected = []

    # make a list of edges selected in the solution
    for i in range(n):
      sol = model.cbGetSolution([model._vars[i,j] for j in range(n)])
      selected += [(i,j) for j in range(n) if sol[j] > 0.5]
    # find the shortest cycle in the selected edge list
    tour = subtour(selected)
    if len(tour) < n:
      # add a subtour elimination constraint
      expr = 0
      for i in range(len(tour)):
        for j in range(i+1, len(tour)):
          expr += model._vars[tour[i], tour[j]]
      model.cbLazy(expr <= len(tour)-1)


# Given a list of edges, finds the shortest subtour

def subtour(edges):
  visited = [False]*n
  cycles = []
  lengths = []
  selected = [[] for i in range(n)]
  for x,y in edges:
    selected[x].append(y)
  while True:
    current = visited.index(False)
    thiscycle = [current]
    while True:
      visited[current] = True
      neighbors = [x for x in selected[current] if not visited[x]]
      if len(neighbors) == 0:
        break
      current = neighbors[0]
      thiscycle.append(current)
    cycles.append(thiscycle)
    lengths.append(len(thiscycle))
    if sum(lengths) == n:
      break
  return cycles[lengths.index(min(lengths))]

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
            vars[i, j] = m.addVar(obj=tsputil.distance(points[i], points[j]),
                                  vtype=GRB.BINARY,
                                  name='edge_' +str(i) + '_' + str(j))
            vars[j, i] = vars[i, j]
        m.update()

    # Add degree-2 constraint, and forbid loops

    for i in range(len(points)):
        m.addConstr(quicksum(vars[i, j] for j in range(len(points))) == 2)
        vars[i, i].ub = 0

    # obj = quicksum(
    #     edges[i, j]
    #     for i in range(len(edges))
    #     for j in range(len(edges)+1)
        # for j in range(len(edges[i]))
    # )

    obj = quicksum(model.getVars())

    # Add degree-2 constraint, and forbid loops

    for i in range(n):
        m.addConstr(
            quicksum(
                edges[i, j]
                for j in range(n)) == 2)
    edges[i, i].ub = 0

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

