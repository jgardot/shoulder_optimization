from fonctions import *
import time
from platypus import NSGAII,Problem,Real

t1 = time.time()

class Muscle_opti(Problem):
    def __init__(self):
        super(Muscle_opti, self).__init__(2,1) # (variables,objectifs)
        self.types[:] = [Real(1.2e-9,1.5e-9) ,Real(0,0.499)]

    def evaluate(self, solution):
        param_mat = solution.variables[:]
        solution.objectives[:] = eloignement(param_mat)


algorithm = NSGAII(Muscle_opti())
algorithm.run(1000)

t2 = time.time()
print("Temps de calcul (s) :",t2-t1)
print("Algorithm result :",algorithm.result)