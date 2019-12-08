import random
import numpy

from deap import base
from deap import creator
from deap import tools
from deap import algorithms

import generated as formula
import plotly.graph_objects as go

chromosome_length = formula.variable_count
population_size = 200
mate_rate = 0.5
mutation_rate = 0.01
n_of_generations = 500


creator.create("FitnessSAT", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessSAT)

toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_bool, chromosome_length)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


def fitness(chromosome):
    clauses_satisfied = 0
    for clause in formula.clauses:
        if clause(chromosome):
            clauses_satisfied += 1
    return [clauses_satisfied]


toolbox.register("evaluate", fitness)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=mutation_rate)
toolbox.register("select", tools.selBest)

pop = toolbox.population(n=population_size)

best = tools.HallOfFame(1)
stats = tools.Statistics(lambda ind: ind.fitness.values)
stats.register("avg", numpy.mean)
stats.register("std", numpy.std)
stats.register("min", numpy.min)
stats.register("max", numpy.max)

pop, log = algorithms.eaSimple(pop, toolbox, cxpb=mate_rate, mutpb=mutation_rate, ngen=n_of_generations,
                               stats=stats, halloffame=best, verbose=True)

print("Clause count: " + str(formula.clause_count))

generations = [i['gen'] for i in log]
bests = [i['max'] for i in log]
averages = [i['avg'] for i in log]

fig = go.Figure()
fig.add_trace(go.Scatter(x=tuple(generations),y=tuple(bests),mode='lines+markers',name='Max'))
fig.add_trace(go.Scatter(x=tuple(generations),y=tuple(averages),mode='lines+markers',name='Avg'))
fig.update_layout(
    title = "SAT",
    xaxis=go.layout.XAxis(title=go.layout.xaxis.Title(text="Generations")),
    yaxis=go.layout.YAxis(title=go.layout.yaxis.Title(text="Clauses satisfied")),
)
fig.show()