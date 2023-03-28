import random
import matplotlib.pyplot as plt


items = [
    {'weight': 3, "value": 5},
    {'weight': 12, "value": 9},
    {'weight': 8, "value": 1},
    {'weight': 11, "value": 14},
    {'weight': 10, "value": 8},
    {'weight': 7, "value": 12},
    {'weight': 6, "value": 5},
    {'weight': 2, "value": 6},
    {'weight': 14, "value": 3},
    {'weight': 2, "value": 7},
]

populationNb = 20
iterations = 2
crossingProbability = 0.8
mutationProbability = 0.1
maxBackpackCapacityWeight = 53


def generateGenom():
    return [random.randint(0, 1) for _ in range(len(items))]


def crossover(parentGenom1, parentGenom2):
    child = []
    for i in range(len(parentGenom1)):
        if random.random() < crossingProbability:
            child.append(parentGenom1[i])
        else:
            child.append(parentGenom2[i])
    return child


def getWeightAndValue(genom):
    total_weight = 0
    total_value = 0
    for i in range(len(genom)):
        if genom[i] == 1:
            total_weight += items[i]['weight']
            total_value += items[i]['value']
    if total_weight > maxBackpackCapacityWeight:
        return (0, total_weight)
    else:
        return (total_value, total_weight)


def mutation(genom):
    for i in range(len(genom)):
        if random.random() < mutationProbability:
            genom[i] = 1 - genom[i]
    return genom


def main():
    best_values = []
    avg_values = []
    iterationCopies = []
    genoms = [generateGenom() for _ in range(populationNb)]
    for iteration in range(iterations):
        genomsValues = []
        genomsWeights = []
        for (value, weight) in [getWeightAndValue(genom) for genom in genoms]:
            genomsValues.append(value)
            genomsWeights.append(weight)
        iterationCopies.append(
            {'genoms': genoms, 'values': genomsValues, 'weights': genomsWeights})
        parents = random.choices(genoms, weights=genomsValues, k=2)
        children = []
        for _ in range(populationNb):
            parents = random.choices(genoms, weights=genomsValues, k=2)
            children.append(mutation(crossover(parents[0], parents[1])))
        genoms = children
        best_values.append(max(genomsValues))
        avg_values.append(sum(genomsValues) / len(genomsValues))

    iterationsArr = range(iterations)
    print(max(best_values))
    print(iterationCopies)
    plt.plot(iterationsArr, best_values, label='Best')
    plt.plot(iterationsArr, avg_values, label='Average')
    plt.xlabel('Generation')
    plt.ylabel('Values')
    plt.title('Evolution of genoms using Genetic Algorithm')
    plt.legend()
    plt.show()


main()
