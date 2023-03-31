import random
import matplotlib.pyplot as plt
import numpy as np

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


def generateTable(items, genomstable):
    num_items = len(items)
    table = []
    table.append(np.arange(1, num_items+1))
    table.append([item["weight"] for item in items])
    table.append([item["value"] for item in items])
    table.append(['' for i in items])
    for i in range(populationNb):
        table.append(genomstable[i])
    return table


def createPlot(genoms1, genoms2, best_values, avg_values, plotGenomValues, iterationsArr, stringOnPlot):
    fig, axs = plt.subplots(nrows=2, ncols=3, figsize=(20, 12))
    plt.subplots_adjust(left=None, bottom=None, right=None,
                        top=0.9, wspace=0.85, hspace=0.314)
    plt.rcParams['axes.titlepad'] = 40

    table1 = generateTable(items, genoms1)
    table2 = generateTable(items, genoms2)
    rows = ['Items Index', 'Weight', 'Value', ''] + \
        ['Genom ' + str(i) for i in range(0, 20)]

    axs[0, 0].set_title("1st. Iteration Table")
    axs[0, 0].axis('off')
    table = axs[0, 0].table(cellText=table1, cellLoc='center',
                            loc='center', rowLabels=rows)

    for i in range(0, 24):
        cell = table[i, -1].get_text()
        cell.set_fontweight('bold')

    for j in range(3):
        for i in range(10):
            cell = table[j, i].get_text()
            cell.set_fontweight('bold')

    axs[0, 1].set_title("2nd. Iteration Table")
    axs[0, 1].axis('off')
    table = axs[0, 1].table(cellText=table2, cellLoc='center',
                            loc='center', rowLabels=rows)

    for i in range(0, 24):
        cell = table[i, -1].get_text()
        cell.set_fontweight('bold')

    for j in range(3):
        for i in range(10):
            cell = table[j, i].get_text()
            cell.set_fontweight('bold')

    axs[0, 2].axis('off')
    axs[0, 2].set_visible(False)

    axs[1, 2].axhline(y=max(best_values), xmin=0, xmax=0.95, color='gray',
                      linestyle="dashed", linewidth=1, label=max(best_values))
    axs[1, 2].plot(iterationsArr, best_values, label='Best')
    axs[1, 2].plot(iterationsArr, avg_values, label='Average')
    axs[1, 2].set_position([0.7, 0.35, 0.228, 0.343])
    plt.xlabel(
        f'Generation\n \n \n {stringOnPlot[0]} \n {stringOnPlot[1]}', fontsize=12)
    plt.ylabel('Values')
    plt.title('Evolution of genoms using Genetic Algorithm')
    plt.legend()

    plot1 = list(filter(lambda obj: obj['object'] > 0, map(lambda x, i: {
                 'object': x, 'index': i}, plotGenomValues[0], range(len(plotGenomValues[0])))))
    plot1Values = [obj['object'] for obj in plot1]
    plot1Indexes = [obj['index'] for obj in plot1]
    plot2 = list(filter(lambda obj: obj['object'] > 0, map(lambda x, i: {
                 'object': x, 'index': i}, plotGenomValues[1], range(len(plotGenomValues[1])))))
    plot2Values = [obj['object'] for obj in plot2]
    plot2Indexes = [obj['index'] for obj in plot2]

    axs[1, 0].set_title("1st. Iteration Roulette", y=1.2)
    axs[1, 0].pie(
        plot1Values, labels=[i for i in plot1Indexes], autopct='%1.2f%%', radius=1.8, frame=False, pctdistance=0.8)

    axs[1, 1].set_title("2nd. Iteration Roulette", y=1.2)
    axs[1, 1].pie(
        plot2Values, labels=[i for i in plot2Indexes], autopct='%1.2f%%', radius=1.8, frame=False, pctdistance=0.8)
    plt.show()


def main():
    best_values = []
    avg_values = []
    iterationCopies = []
    stringOnPlot = []
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
        stringOnPlot.append(str("Best genom of " + str(iteration+1) +
                            " iteration: " + str(genomsValues.index(max(genomsValues)))))
        best_values.append(max(genomsValues))
        avg_values.append(sum(genomsValues) / len(genomsValues))
        print(stringOnPlot[iteration])

    iterationsArr = range(iterations)
    createPlot(iterationCopies[0]['genoms'], iterationCopies[1]['genoms'], best_values, avg_values,
               [iterationCopies[0]['values'], iterationCopies[1]['values']], iterationsArr, stringOnPlot)


main()
